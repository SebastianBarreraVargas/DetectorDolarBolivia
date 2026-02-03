class URLUtils:
    @staticmethod
    def clean_url(url: str) -> str:
        url = url.strip()
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        parts = url.split('/')
        return f"{parts[0]}//{parts[2]}"