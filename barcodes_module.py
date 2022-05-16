# -*- coding: utf-8 -*-
import cv2
from pyzbar.pyzbar import decode
from pdf2image import convert_from_path
from PIL import Image


def cut_out_barcodes(path_to_file: str) -> None:
    pages = convert_from_path(path_to_file,
                              poppler_path=r"poppler-22.04.0/Library/bin")
    for page in pages:
        page.save('barcodes/out.jpg', 'JPEG')

    cut_bar_codes()


def cut_bar_codes():
    im = Image.open("barcodes/out.jpg")

    left = 16
    top = 48
    right = 750
    bottom = 109

    im1 = im.crop((left, top, right, bottom))
    im1.save('barcodes/first_bar_code.jpg')

    left = 47
    top = 429
    right = 241
    bottom = 514

    im1 = im.crop((left, top, right, bottom))
    im1.save('barcodes/second_bar_code.jpg')


def barcode_reader(image_path: str) -> str:
    img = cv2.imread(image_path)
    detected_barcode = decode(img)

    if not detected_barcode:
        print("Штрихкод не обнаружен!")
    else:
        (x, y, w, h) = detected_barcode.rect
        cv2.rectangle(img, (x - 10, y - 10),
                      (x + w + 10, y + h + 10),
                      (255, 0, 0), 2)

        if detected_barcode.data != "":
            return detected_barcode.data.decode('UTF-8')


def compare_first_barcode_value(barcode_value, pdf_value) -> None:
    pn_value = pdf_value.get("PN").strip()
    if pn_value != barcode_value:
        print(f"Значение Pn не соответствует штрих коду. Значение поля 'Pn': "
              f"{pn_value}, значение в штрих коде: {barcode_value}")


def compare_second_barcode_value(barcode_value, pdf_value) -> None:
    qty_value = pdf_value.get("Qty").strip()
    if qty_value != barcode_value:
        print(f"Значение Qty не соответствует штрих коду. Значение "
              f"поля 'Qty': {qty_value}, "
              f"значение в штрих коде: {barcode_value}")
