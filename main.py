from pdf_texts_module import get_pdf_text, get_pdf_elements_location, \
    compare_fields_difference, compare_elements_coordinates
from barcodes_module import cut_out_barcodes, compare_first_barcode_value,\
    compare_second_barcode_value, barcode_reader

# Получение путей до сравниваемых файлов
sample_pdf_path = input("Пожалуйста, введите путь до файла PDF, "
                        "который будет использоваться как шаблон: ")
new_pdf_path = input("Пожалуйста, введите путь до файла PDF, "
                     "который будет проверяться: ")
print()

# Получение текста из пдф, разбивка его в словари и сравнение
sample_dict_values = get_pdf_text(sample_pdf_path)
new_dict_values = get_pdf_text(new_pdf_path)
compare_fields_difference(sample_dict_values, new_dict_values)

# Сравнение координат элементов
list_sample = get_pdf_elements_location(sample_pdf_path)
list_sample2 = get_pdf_elements_location(new_pdf_path)
compare_elements_coordinates(list_sample, list_sample2)

# Штрих коды
cut_out_barcodes(sample_pdf_path)
first_barcode_value = barcode_reader('barcodes/first_bar_code.jpg')
second_barcode_value = barcode_reader('barcodes/second_bar_code.jpg')
compare_first_barcode_value(first_barcode_value, new_dict_values)
compare_second_barcode_value(second_barcode_value, new_dict_values)


# Можно сделать, чтобы после одной неудачной проверки у нас
# дальше проверки не проходили, но сомневаюсь, что это правильно
