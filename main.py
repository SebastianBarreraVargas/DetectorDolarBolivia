from view.vista import Vista
from controller.controlador import Controlador
from model.DetectorSebasCMS import CMSDetector, RequestHandler, URLUtils
from model.PriceDetector import PriceDetector

def main():
    request_handler = RequestHandler()

    # Detectores
    cms_detector   = CMSDetector(request_handler)
    price_detector = PriceDetector(request_handler)

    controlador = Controlador(cms_detector, price_detector, URLUtils)
    vista = Vista(controlador)
    vista.iniciar()

if __name__ == "__main__":
    main()