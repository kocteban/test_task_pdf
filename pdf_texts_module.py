# -*- coding: utf-8 -*-
from pdfminer.converter import PDFPageAggregator
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LAParams, LTTextBox
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage


# get_pdf_text и get_pdf_elements_location по хорошему надо бы объединить
# в один, но тогда получается совсем не красиво

def get_pdf_text(path: str) -> dict:
    """
    Вытаскивает текст из PDF файла
    """
    dictionary = {}
    for page_layout in extract_pages(path):
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                text = element.get_text()
                if ":" in text:
                    double_dots_index = text.find(':')
                    next_string_index = text.find('\\n')
                    dictionary[text[:double_dots_index]] = \
                        text[double_dots_index + 1:next_string_index]
                else:
                    next_string_index = text.find('\\n')
                    dictionary.setdefault(text[:next_string_index])
    dictionary.pop(" ")
    return dictionary


def get_pdf_elements_location(path: str) -> list:
    """
    Вытаскивает тест и координаты текстовых блоков из pdf
    :param path: путь до файла, str
    :return: list
    """
    fp = open(path, 'rb')
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    pages = PDFPage.get_pages(fp)

    coordinate_list = []
    for page in pages:
        interpreter.process_page(page)
        layout = device.get_result()

        for lobj in layout:
            tuple_sample = []
            if isinstance(lobj, LTTextBox):
                tuple_sample += lobj.bbox[0], lobj.bbox[3], lobj.get_text()
                coordinate_list.append(tuple_sample)

    return coordinate_list


def compare_two_pdf_files(sample_dict: dict, check_dict: dict) -> tuple:
    """
    Сравнивает ключи существующих полей
    :param sample_dict:
    :param check_dict:
    :return: поля, которые отличаются
    """
    keys_one = set(sample_dict.keys())
    keys_two = set(check_dict.keys())
    comparing = list(keys_one.difference(keys_two))
    reverse_comparing = list(keys_two.difference(keys_one))

    return comparing, reverse_comparing


def compare_fields_difference(sample_value: dict,
                              compared_value: dict) -> None:
    compared_values, reversed_compared_values = \
        compare_two_pdf_files(sample_value, compared_value)
    if compared_values:
        print(f"Поля, которые есть в шаблоне, но которых нет в "
              f"проверяемом файле: {compared_values}", "\n")
    if reversed_compared_values:
        print(f"Поля, которых нет в шаблоне, но которые есть в "
              f"проверяемом файле: {reversed_compared_values}", "\n")


def compare_elements_coordinates(sample_list: list,
                                 compared_list: list) -> None:
    """
    На входе два списка, на выходе вывод элементов, которые отличаются
    :param sample_list:
    :param compared_list:
    :return: None
    """
    res = []
    res2 = []
    for i, j in zip(sample_list, compared_list):
        if i != j:
            res.append(i)

    for i, j in zip(compared_list, sample_list):
        if i != j:
            res2.append(i)

    if res or res2:
        print(f"Поля, местоположение которых отличается от "
              f"шаблона: {res, res2}")