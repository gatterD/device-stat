from locust import HttpUser, task, between
import random

class DeviceStatsUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        user_resp = self.client.post("/users/", json={"name": "Test User"})
        if user_resp.status_code == 200:
            self.user_id = user_resp.json()["id"]
        else:
            self.user_id = None
        dev_resp = self.client.post("/devices/", json={"name": f"locust-device-{random.randint(1,10000)}", "user_id": self.user_id})
        if dev_resp.status_code == 200:
            self.device_id = dev_resp.json()["id"]
        else:
            self.device_id = None

    @task(3)
    def post_stats(self):
        if self.device_id:
            payload = {
                "x": random.uniform(-100, 100),
                "y": random.uniform(-100, 100),
                "z": random.uniform(-100, 100)
            }
            self.client.post(f"/devices/{self.device_id}/stats", json=payload)

    @task(1)
    def get_analysis(self):
        if self.device_id:
            self.client.get(f"/analysis/devices/{self.device_id}")