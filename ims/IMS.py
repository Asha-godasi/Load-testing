from locust import HttpUser, task, between

class IMSUser(HttpUser):
    wait_time = between(1, 3)  # Simulates realistic user wait time between requests

    @task
    def health_check(self):
        self.client.get("/api/health/", name="Health Check")

    @task
    def single_sku_stock(self):
        self.client.get("/api/stock/SKU-0014/?facility=WH-1", name="Single SKU Stock")

    @task
    def multi_sku_stock(self):
        self.client.get("/api/stock/multi/?facility=WH-1&skus=SKU-0014,SKU-0011", name="Multi SKU Stock")
