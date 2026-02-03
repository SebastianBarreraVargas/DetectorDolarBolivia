class Controller:
    def __init__(self, scraper, url_utils):
        self.scraper = scraper
        self.url_utils = url_utils

    def get_precio_compra(self, url: str) -> str:
        cleaned = self.url_utils.clean_url(url)
        return self.scraper.fetch_precio_compra(cleaned)