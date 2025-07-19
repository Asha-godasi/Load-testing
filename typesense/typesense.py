from locust import HttpUser, task, between

class RozanaTypesenseUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        self.headers = {
            "Content-Type": "application/json",
            "X-TYPESENSE-API-KEY": "key"
        }
        self.store_id = "936164"
        self.product_id = "673439"

    @task
    def health_check(self):
        response = self.client.get("/health", headers=self.headers)
        print("✅ Health check passed." if response.status_code == 200 else f"❌ Health check failed: {response.status_code}")

    @task
    def get_categories(self):
        params = {
            "q": "*",
            "filter_by": f"store_id:={self.store_id}&&parent_id:=0&&status:=true",
            "per_page": 25
        }
        response = self.client.get("/collections/store_categories/documents/search", headers=self.headers, params=params)
        print("✅ Categories fetched." if response.status_code == 200 else f"❌ Failed to fetch categories: {response.status_code}")

    @task
    def get_product_by_id(self):
        response = self.client.get(f"/collections/store_products/documents/{self.product_id}", headers=self.headers)
        print("✅ Product fetched." if response.status_code == 200 else f"❌ Failed to fetch product: {response.status_code}")

    @task
    def get_home_subcategories(self):
        params = {
            "q": "*",
            "filter_by": f"store_id:={self.store_id}&&parent_id:=0",
            "sort_by": "position:asc",
            "per_page": 6
        }
        response = self.client.get("/collections/store_categories/documents/search", headers=self.headers, params=params)
        print("✅ Home subcategories fetched." if response.status_code == 200 else f"❌ Failed to fetch home subcategories: {response.status_code}")

    @task
    def get_home_subcategories_latest(self):
        params = {
            "q": "*",
            "filter_by": f"store_id:={self.store_id}&&level:=sub_category",
            "sort_by": "position:asc",
            "page": 1,
            "per_page": 6
        }
        response = self.client.get("/collections/store_categories/documents/search", headers=self.headers, params=params)
        print("✅ Latest home subcategories fetched." if response.status_code == 200 else f"❌ Failed to fetch latest subcategories: {response.status_code}")

    @task
    def get_best_selling_products(self):
        params = {
            "q": "*",
            "filter_by": "store_id:=1081793"
        }
        response = self.client.get("/collections/bestSellingProducts/documents/search", headers=self.headers, params=params)
        print("✅ Best selling products fetched." if response.status_code == 200 else f"❌ Failed to fetch best sellers: {response.status_code}")

    @task
    def get_multiple_product_details(self):
        params = {
            "q": "*",
            "filter_by": "id:=[12345,67890,45678]"
        }
        response = self.client.get("/collections/products/documents/search", headers=self.headers, params=params)
        print("✅ Multiple product details fetched." if response.status_code == 200 else f"❌ Failed to fetch product details: {response.status_code}")

    @task
    def get_search_results(self):
        params = {
            "q": "sunfeast",
            "query_by": "name",
            "filter_by": f"store_id:={self.store_id}",
            "page": 1,
            "per_page": 10,
            "exhaustive_search": "true"
        }
        response = self.client.get("/collections/store_products/documents/search", headers=self.headers, params=params)
        print("✅ Search results fetched." if response.status_code == 200 else f"❌ Failed to fetch search results: {response.status_code}")

    @task
    def get_search_suggestions(self):
        params = {
            "q": "lays",
            "query_by": "name,display_name,category_name,subcategory_name,brand_name",
            "prefix": "true",
            "per_page": 10,
            "num_typos": 2,
            "include_fields": "name,display_name,brand_name,thumbnail_image"
        }
        response = self.client.get("/collections/products/documents/search", headers=self.headers, params=params)
        print("✅ Suggestions fetched." if response.status_code == 200 else f"❌ Failed to fetch suggestions: {response.status_code}")

    @task
    def get_sliders(self):
        params = {
            "q": "*",
            "filter_by": f"store_id:={self.store_id}&&language:=english",
            "include_fields": "banner,position,sub_category_id"
        }
        response = self.client.get("/collections/sliders/documents/search", headers=self.headers, params=params)
        print("✅ Sliders fetched." if response.status_code == 200 else f"❌ Failed to fetch sliders: {response.status_code}")

    @task
    def get_banners(self):
        params = {
            "q": "*",
            "filter_by": "store_id:=826440",
            "per_page": 10
        }
        response = self.client.get("/collections/banners/documents/search", headers=self.headers, params=params)
        print("✅ Banners fetched." if response.status_code == 200 else f"❌ Failed to fetch banners: {response.status_code}")

    @task
    def get_promotions_bsp(self):
        params = {
            "q": "*",
            "filter_by": f"store_id:={self.store_id}&&section_type:=bsp"
        }
        response = self.client.get("/collections/top_products/documents/search", headers=self.headers, params=params)
        print("✅ BSP promotions fetched." if response.status_code == 200 else f"❌ Failed to fetch BSP promotions: {response.status_code}")

    @task
    def get_promotions_trp(self):
        params = {
            "q": "*",
            "filter_by": f"store_id:={self.store_id}&&section_type:=trp"
        }
        response = self.client.get("/collections/top_products/documents/search", headers=self.headers, params=params)
        print("✅ TRP promotions fetched." if response.status_code == 200 else f"❌ Failed to fetch TRP promotions: {response.status_code}")

    @task
    def get_product_detail_bsp_trp(self):
        params = {
            "q": "*",
            "filter_by": "id:=371473"
        }
        response = self.client.get("/collections/store_products/documents/search", headers=self.headers, params=params)
        print("✅ BSP/TRP product detail fetched." if response.status_code == 200 else f"❌ Failed to fetch product: {response.status_code}")

    @task
    def get_all_products_of_store(self):
        params = {
            "q": "*",
            "filter_by": f"store_id:={self.store_id}",
            "group_by": "name",
            "group_limit": 1,
            "per_page": 250
        }
        response = self.client.get("/collections/store_categories/documents/search", headers=self.headers, params=params)
        print("✅ All store products fetched." if response.status_code == 200 else f"❌ Failed to fetch all store products: {response.status_code}")

    @task
    def get_store_by_polygon(self):
        params = {
            "q": "*",
            "filter_by": "polygon_coords:(26.770123,80.878481)"
        }
        response = self.client.get("/collections/stores/documents/search", headers=self.headers, params=params)
        print("✅ Store fetched." if response.status_code == 200 else f"❌ Failed to fetch store: {response.status_code}")

    @task
    def get_subcategories(self):
        params = {
            "q": "*",
            "filter_by": f"store_id:={self.store_id}&&parent_id:=11&&status:=true",
            "per_page": 50
        }
        response = self.client.get("/collections/store_categories/documents/search", headers=self.headers, params=params)
        print("✅ Subcategories fetched." if response.status_code == 200 else f"❌ Failed to fetch subcategories: {response.status_code}")

    @task
    def get_subsubcategories(self):
        params = {
            "q": "*",
            "filter_by": "store_id:=994258&&parent_id:=11&&status:=true&&level:=sub_sub_category",
            "per_page": 50
        }
        response = self.client.get("/collections/store_categories/documents/search", headers=self.headers, params=params)
        print("✅ Sub-subcategories fetched." if response.status_code == 200 else f"❌ Failed to fetch sub-subcategories: {response.status_code}")

    @task
    def get_product_by_subsubcategory(self):
        params = {
            "q": "*",
            "filter_by": "store_id:=960979&&category_id:=108"
        }
        response = self.client.get("/collections/store_products/documents/search", headers=self.headers, params=params)
        print("✅ Products by sub-subcategory fetched." if response.status_code == 200 else f"❌ Failed to fetch products: {response.status_code}")