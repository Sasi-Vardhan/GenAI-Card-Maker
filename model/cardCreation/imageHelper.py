import requests
import csv
import time

# ✅ Replace with your Unsplash API Access Key
ACCESS_KEY = "vDPBocfr-DE5DA2XFgdYkuI-MsvviTfsHE3cbRPGV4k"

# ✅ 50 useful 3-letter nouns
nouns = [
    "ant", "bee", "car", "cow", "egg", "fox", "hen", "jam", "key", "lip",
    "man", "nut", "owl", "pig", "rat", "rug", "sky", "toy", "van", "zip",
    "pan", "top", "can", "tap", "mop", "mud", "red", "tin", "yam", "wax",
    "win", "jar", "gum", "lid", "bar", "bat", "fin", "net", "sun", "web",
    "bed", "bag", "cat", "dog", "fan", "cup", "hat", "log", "map", "kit"
]



# ✅ Output file
output_file = "nouns_with_image_links.csv"

# ✅ Function to fetch image URL for a given noun


#main Fucntion which we are going to use for image require ment in the html code
def fetch_image_url(noun):
    url = f"https://api.unsplash.com/search/photos?query={noun}&per_page=1&client_id={ACCESS_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json().get('results')
        if results:
            return results[0]['urls']['regular']
    return "No image found"





# ✅ Write results to CSV
if(__name__ == '__main__'):
        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Noun", "Image URL"])
            
            for noun in nouns:
                image_url = fetch_image_url(noun)
                print(f"{noun} -> {image_url}")
                writer.writerow([noun, image_url])
                time.sleep(1.05)  # Respect API rate limits
