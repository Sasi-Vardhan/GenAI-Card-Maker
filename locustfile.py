from locust import HttpUser, task, between

class IndieUser(HttpUser):
    wait_time = between(1, 2.5)

    @task
    def load_homepage(self):
        self.client.get("/")
