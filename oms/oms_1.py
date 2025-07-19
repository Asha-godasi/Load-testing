from locust import HttpUser, task, between
from urllib.parse import quote

ORDER_PAYLOAD = {
    "customer_id": "2CN3aYJnaGXpaguuctWAubZnKKp1",
    "customer_name": "nithin",
    "facility_id": "1",
    "facility_name": "demo",
    "status": "pending",
    "total_amount": 2276.4,
    "address": {
        "full_name": "Nithin",
        "phone_number": "9123456789",
        "address_line1": "123 Main Street",
        "address_line2": "Apt 4B",
        "city": "Bangalore",
        "state": "Karnataka",
        "postal_code": "56001",
        "country": "INDIA",
        "type_of_address": "work"
    },
    "items": [
        {
            "sku": "SKU-FQGAJLOTIV-10578-3328",
            "quantity": 1,
            "unit_price": 781,
            "sale_price": 781
        },
        {
            "sku": "APPLE-1",
            "quantity": 1,
            "unit_price": 1387,
            "sale_price": 1387
        }
    ]
}

class OMSUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        self.headers = {
            "Authorization": "token"
            }

        # Optional health check
        resp = self.client.get("/health", headers=self.headers)
        if resp.status_code == 200:
            print("✅ Health check passed")
        else:
            print(f"❌ Health check failed: {resp.status_code} {resp.text}")

        self.order_ids = {
            "web": None,
            "app": None,
            "pos": None
        }

    @task
    def app_flow(self):
        self.create_and_fetch_order("app")

    @task
    def pos_flow(self):
        self.create_and_fetch_order("pos")

    @task
    def web_flow(self):
        self.create_and_fetch_order("web")

    def create_and_fetch_order(self, channel):
        base_url = f"/{channel}/v1"

        # Create Order
        with self.client.post(f"{base_url}/create_order", json=ORDER_PAYLOAD, headers=self.headers, catch_response=True, name=f"[{channel.upper()}] Create Order") as resp:
            if resp.status_code == 200:
                data = resp.json()
                self.order_ids[channel] = data.get("order_id")
                if self.order_ids[channel]:
                    print(f"✅ [{channel.upper()}] Created Order ID: {self.order_ids[channel]}")
                    resp.success()
                else:
                    resp.failure(f"❌ [{channel.upper()}] No order_id returned")
            else:
                resp.failure(f"❌ [{channel.upper()}] Create Order Failed: {resp.status_code} {resp.text}")

        # Get Order Details
        if self.order_ids[channel]:
            order_id = quote(self.order_ids[channel], safe='')
            details_url = f"{base_url}/order_details?order_id={order_id}"
            if channel in ["web", "pos"]:
                details_url += "&facility_name=demo"

            with self.client.get(details_url, headers=self.headers, catch_response=True, name=f"[{channel.upper()}] Order Details") as resp:
                if resp is not None and resp.status_code == 200:
                    resp.success()
                else:
                    resp.failure(f"❌ [{channel.upper()}] Get Order Details: {resp.status_code if resp else 'No response'}")

        # Get Orders List
        with self.client.get(f"{base_url}/orders?limit=1&offset=10", headers=self.headers, name=f"[{channel.upper()}] Orders List", catch_response=True) as resp:
            if resp is not None and resp.status_code == 200:
                resp.success()
            else:
                resp.failure(f"❌ [{channel.upper()}] Orders List: {resp.status_code if resp else 'No response'}")
