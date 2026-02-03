from view.vista import Vista
from controller.controlador import Controller
from model.scraper import WebScraper
from model.url_utils import URLUtils

def main():
    scraper = WebScraper(driver_path='./geckodriver')
    controller = Controller(scraper, URLUtils)
    vista = Vista(controller)
    vista.iniciar()

if __name__ == "__main__":
    main()