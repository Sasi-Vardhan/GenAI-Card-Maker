import openai
import requests
import os
import time
import threading
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
from config import OPENAI_API_KEY1, OPENAI_API_KEY2

class ImageAgent:
    def __init__(self, output_dir="output/images", max_retries=3):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        self.api_keys = [OPENAI_API_KEY1, OPENAI_API_KEY2]
        self.key_usage = {key: 0 for key in self.api_keys}
        self.current_key_index = 0
        self.lock = threading.Lock()
        self.max_retries = max_retries

        logging.basicConfig(
            filename='image_generation.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def _get_next_api_key(self):
        with self.lock:
            key = self.api_keys[self.current_key_index]
            self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
            self.key_usage[key] += 1
            return key

    def _save_image(self, url: str, filename: str):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            with open(filename, "wb") as f:
                f.write(response.content)
            return True
        except Exception as e:
            logging.error(f"[DOWNLOAD ERROR] {e}")
            return False

    def generate_image(self, prompt: str, scene_id: str):
        for attempt in range(self.max_retries):
            api_key = self._get_next_api_key()
            openai.api_key = api_key
            try:
                logging.info(f"[TRY] Key: {api_key[:6]}..., Scene: {scene_id}, Attempt: {attempt+1}")
                response = openai.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1
                )
                image_url = response.data[0].url
                filename = os.path.join(self.output_dir, f"{scene_id}.png")

                if self._save_image(image_url, filename):
                    logging.info(f"[SUCCESS] Image saved: {filename}")
                    return filename
            except Exception as e:
                logging.warning(f"[FAILURE] Key: {api_key[:6]}..., Scene: {scene_id}, Error: {e}")
                time.sleep(2 ** attempt)

        logging.error(f"[FAILURE] All keys failed for Scene: {scene_id}")
        return None
