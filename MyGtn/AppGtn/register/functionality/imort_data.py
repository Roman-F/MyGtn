# coding=utf-8
__author__ = 'sss'
# модуль содержит классы и методы выполняющие импорт данных в Систему
# Глобальные переменные объявлены в конце модуля, это сделано для того,
# чтобы в DICT_MATCHING_CLASS_IMPORT_WITH_CLASS_CHECK можно было хранить непосредственно ссылку на класс проверки,
# а не его имя (т.е. чтобы в последующем не проводить поиск по имени класса проверки, полученного из словаря)

from django.db.models import Q
from operator import __or__ as OR
from django.conf import settings
from datetime import datetime


import openpyxl
import inspect
import random
import re




class ImportDataInSystem ():

    """
        Класс, который занимается импортом данных и организует проверку данных
    """


    @classmethod
    def get_file_template_for_import(cls, cls_for_template):

        """
        """

        wb = openpyxl.Workbook()
        ws = wb.active

        j = 1
        for field in cls_for_template._meta.fields:

            if not (field.name in cls_for_template.FIELD_NOT_FOR_IMPORT):
                ws.cell(row = 1, column = j, value=field.verbose_name).font = openpyxl.styles.Font(bold=True)
                ws.column_dimensions[openpyxl.utils.get_column_letter(j)].width = len(field.verbose_name) + 1
                j += 1

        #Проводим сохранение файла с данными
        name_file = 'template_for_import_' + cls_for_template.__name__ + str(random.randint(1000, 9999)) + '.xlsx'
        full_name_file = settings.STATIC_ROOT + name_file

        wb.save(full_name_file)

        return full_name_file

    # @classmethod
    # def get_file_template_for_import(cls, cls_for_template):
    #
    #     """
    #     Метод возвращает полный путь к динамически сформированному xlsx файлу, в котором перечислены поля модели как
    #      заголовки столбцов.
    #     Полученный файл предполагается использовать как шаблон файла импорта данных в выбранную модель
    #     """
    #
    #     wb = openpyxl.Workbook()
    #     ws = wb.active
    #
    #     def customize_cell (field_for_cell, take_row = 1, take_column = 1):
    #         """
    #         Процедура,
    #         делает заголовок в файле жирным,
    #         а также определяем по заголовкам ширину колонок
    #
    #         :param field_for_cell: поле модели для получения заголовка столбца
    #         :return: ничего
    #         """
    #
    #         ws.cell(row=take_row, column=take_column, value=field_for_cell.verbose_name).font = openpyxl.styles.Font(bold=True)
    #         ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = len(field_for_cell.verbose_name) + 1
    #
    #
    #     #получаем список имен полей модели, для использования далее как заголовков столбцов
    #
    #     i = 1
    #     if cls_for_template.FIELD_FOR_IMPORT == 'all':
    #         for field in cls_for_template._meta.fields:
    #             customize_cell(field, 1, i)
    #             i = i + 1
    #
    #     else:
    #         for field_name in cls_for_template.FIELD_FOR_IMPORT:
    #             field = cls_for_template._meta.get_field(field_name)
    #             customize_cell(field, 1, i)
    #             i = i + 1
    #
    #     #Проводим сохранение файла с данными
    #     name_file = 'template_for_import_' + cls_for_template.__name__ + str(random.randint(1000, 9999)) + '.xlsx'
    #     full_name_file = settings.STATIC_ROOT + name_file
    #
    #     wb.save(full_name_file)
    #
    #     return full_name_file

    #######Методы импорта данных#######

    # @classmethod
    # def do_check_data (cls, import_data):
    #     """
    #     :param import_data: словарь содержащий данные о выгрузке (например класс проверки)
    #     :return: возвращает дозаполенный словрь import_data
    #     """
    #
    #     def write_to_file_errors ():
    #         for idx_column, check_cell in enumerate(check_row):
    #                     cell_error = ws_error.cell(row= idx_file_errors, column= idx_column+1, value= check_cell.value)
    #                     cell_error.font = check_cell.font
    #
    #                     if result[idx_column]:
    #                         cell_error.fill = redFill
    #
    #
    #     ws = import_data['data_import']
    #     number_of_errors = import_data['dict_result']['number_of_errors']
    #
    #     class_check = import_data['class_check']
    #     methods_check = class_check.__dict__
    #
    #     #Формируем имена методов для проверки, соответствующие колонкам в файле
    #     names_check_methods = ['do_check_' + import_data['dict_matching'][x.value] for x in ws.rows[0]]
    #
    #     #Формируем список полей модели в порядке соответствущим колонкам в файле
    #     fields_of_the_order = [import_data['dict_matching'][x.value] for x in ws.rows[0]]
    #
    #     #Создаем файл для хранения ошибочных записей + добавляем в него колонку "Описание ошибок"
    #     wb_error = openpyxl.load_workbook(cls.get_file_template_for_import(import_data['original_class'])
    #                                       ,read_only = False)
    #     ws_error = wb_error.active
    #     new_column = len(names_check_methods) + 1
    #     ws_error.cell(row = 1, column = new_column, value=u'Описание ошибок').font = openpyxl.styles.Font(bold=True)
    #
    #     #Определяем шаблон заливки ошибочных ячеек
    #     redFill = openpyxl.styles.PatternFill(start_color='FFFF0000', fill_type='solid')
    #
    #     #Построчно проводим проверку данных
    #     count_error = 0
    #     count_duplicates = 0
    #     count_correct_records = 0
    #     idx_file_errors = 2
    #     for check_row in ws.rows[1:]:
    #         result = []
    #         text_error = ''
    #         general_text_error = ''
    #         check_values = [x.value for x in check_row]
    #
    #         # вызываем для каждого элемента проверяемой строки свой метод проверки
    #         for name_method, check_value in zip(names_check_methods, check_values):
    #             # text_error += methods_check.get(name_method, lambda x:'')(check_value)
    #             text_error = getattr(class_check,name_method,lambda x:'')(str(check_value))
    #             general_text_error += text_error
    #             # text_error += methods_check[name_method].__func__(check_value) if name_method in methods_check else ''
    #             result.append(text_error)
    #             text_error = ''
    #
    #         # Смотрим наличие ошибок по итогам проверки, и если есть заполняем файл с ошибкамиб
    #         if general_text_error:
    #             # for idx_column, check_cell in enumerate(check_row):
    #             #     cell_error = ws_error.cell(row= idx_file_errors, column= idx_column, value= check_cell.value)
    #             #     cell_error.font = check_cell.font
    #             #
    #             #     if result[idx_column]:
    #             #         cell_error.fill = redFill
    #             write_to_file_errors()
    #
    #             count_error += 1
    #             ws_error.cell(row= idx_file_errors, column= len(check_row)+1,value= general_text_error)
    #             idx_file_errors += 1
    #
    #         #Иначе проводим проверку на дублирование
    #         else:
    #             query_set = import_data['original_class'].objects.all()
    #             param_for_filter = {key:value for key,value in zip(fields_of_the_order,check_values) if value}
    #             # pre_param = map(lambda x,y: datetime.datetime.date(param_for_filter[x])
    #             #                         if type(y) == type(datetime.datetime.today())
    #             #                         else param_for_filter[x], param_for_filter.items())
    #             #
    #
    #
    #             if import_data['original_class'].objects.filter(**param_for_filter):
    #                 # тоже самое, что и при записи в файл ошибки
    #                 # вынысти в отдельную функцию
    #                 # for idx_column, check_cell in enumerate(check_row):
    #                 #     cell_error = ws_error.cell(row= idx_file_errors, column= idx_column, value= check_cell.value)
    #                 #     cell_error.font = check_cell.font
    #                 #
    #                 #     if result[idx_column]:
    #                 #         cell_error.fill = redFill
    #                 write_to_file_errors()
    #
    #
    #                 count_duplicates += 1
    #                 ws_error.cell(row= idx_file_errors, column= len(check_row)+1,value= 'Дубль записи в Системе')
    #                 idx_file_errors += 1
    #
    #             else:
    #                 count_correct_records += 1
    #
    #     full_name_file = settings.STATIC_ROOT + 'error' + str(random.randint(1000, 9999)) + '.xlsx'
    #     wb_error.save(full_name_file)
    #
    #     return {
    #         'count_error' : count_error,
    #         'count_duplicates' : count_duplicates,
    #         'count_correct_records' : count_correct_records
    #     }


    @staticmethod
    def get_true_vlues (cls_for_import, names_check_fields, check_values):
        """
        Метод находит связанные поля в модели, для которой осуществляется импорт.
        Далее метод определяет для найденных связанных полей, по импортируемым данным,
            действительные ("Истинные") значения (т.е. значения внешних ключей)

        Решаемая задача (на примере технического средства (далее - ТС)):
            Импортируется запись о ТС.
            Модель ТС содержит связанное поле "Цвет", которое ссылается на справочник "Цвет ТС".
            В БД, в таблице ТС в колонке "Цвет" хранится ID цвета из справочника "Цвет ТС".
            В тоже время, в импортируемом файле указывается значение цвета, а не его ID (что естетственно, т.к.
                пользователь не знает ID цветов)
            Т.к. типы имортируемых значений для связанных полей и типы связанных полей в БД не совпадают,
                то действовать "в лоб" нельзя.
            Т.о. предварительно необходимо найти по импортируемым значениям соответствующие им ID в связанных моделях
                и уже после этого проводить дальнейшую обработку (искать дубли, сохранять данные в БД)

        Нюансы реализации:
            1) т.к. заренее не известно по какой модели будет проводится импорт, то необходимо проверять все поля модели
               на "связанность"
            2) аналогично и для связанных моделей:
                т.к. заранее не известна связанная модель, то нельзя определить по какому полю нужно искать
                    импортируемое значение.
                соответственно, необходимо искать импортируемое значение по всем полям модели.
            3) Для пустых импортируемых значений (None) поиск не проводится

            Примечаниие: хардкод как решение задачи не приемлем :)


        :param cls_for_import: класс модели для которйо осуществляется импорт
        :param names_check_fields: наименование полей модели по которым проводится импорт
        :param check_values: импортируемые значения
        :return: список импортируемых значений, в котором значения для связанных полей заменены соответствующими им
            ID (внещними ключами)
        """

        check_related_generator = (cls_for_import._meta.get_field_by_name(name)[0].rel.to
                                   if cls_for_import._meta.get_field_by_name(name)[0].rel else False
                                   for name in names_check_fields)

        agregated_Q = []
        true_check_values=[]

        for related_class, value in zip(check_related_generator,check_values):

            true_value = False

            if (related_class) and (value != None):
                rel_cls_fields = related_class._meta.get_all_field_names()
                for rel_cls_field in rel_cls_fields:
                    agregated_Q.append(Q(**{rel_cls_field:value}))

                true_value = related_class.objects.filter(OR(*agregated_Q))[:1]

            if true_value:
                true_check_values.append(true_value.pk)
            else:
                true_check_values.append(value)

        return true_check_values

    @staticmethod
    def check_row_data (class_check, fields_name, check_values):
        """
        :param check_row: проверяемая строка с данными
        :return: возвращает False если ошибок не найденно, иначе кортеж результатов проверки полей:
        * пустая строка - ошибок в поле нет
        * текст - поле ошибочно, а полученный текст описывает ошибку
        """

        result = tuple(getattr(class_check,'do_check_' + field_name,lambda x:'')(str(check_value))
                                            for field_name, check_value in zip (fields_name, check_values))

        return result if any(result) else False

    @staticmethod
    def check_duplicate (cls_for_import, fields_name, check_values):
        """
        :param cls_for_import: класс модели, в которую осуществляется импорт
        :param methods_and_check_values: наименования полей и значения, которые импортируются в поля
        :return: True - если дубль, иначе False
        """

        param_for_filter = {key:datetime.date(value) if isinstance(value,datetime) else value
                                        for key,value in zip (fields_name, check_values) if value}

        return True if cls_for_import.objects.filter(**param_for_filter)[:1] else False



    @classmethod
    def do_import (cls, cls_for_import, data_file):

        """
            Метод из полученного файла загружает данные в систему;
             При этом проводит проверки на соответствие:
             - расширению
             - формату
             - отсутствию дублей (можно заменить на свою функцию поиска дублей)
             - корректности значений полей файла (необходимо настраивать для каждого реестра отдельно)

             В результате возвращается словарь с итогами импорта и ссылкой на файл с ошибками
        """
        def write_to_file_errors ():
            for idx_column, check_cell in enumerate(check_row):
                        cell_error = ws_error.cell(row= idx_file_errors, column= idx_column+1, value= check_cell.value)
                        cell_error.font = check_cell.font

                        if result_check:
                            if result_check[idx_column]:
                                cell_error.fill = redFill

        dict_result = {
            'status': '',
            'message': '',
            'number_of_records': 0,
            'number_of_imported': 0,
            'number_of_errors': 0,
            'number_of_duplicates': 0,
            'link_to_file_errors': ''
        }

        wb = openpyxl.load_workbook(data_file,read_only=False)
        ws = wb.active

        names_check_methods = []
        class_check = DICT_MATCHING_CLASS_IMPORT_WITH_CLASS_CHECK[cls_for_import.__name__]

        # Проверяем файл на соответствие структуре импорта (есть ли нужные колонки)
        field_for_import = cls_for_import._meta.get_all_field_names()
        verbose_name_to_import = {}
        matching_column_import_with_field_model = {}
        error_column = []

        i = ''

        map(lambda x: field_for_import.remove(x), cls_for_import.FIELD_NOT_FOR_IMPORT)

        # import_data = {
        #     'data_import' : ws,
        #     'original_class': cls_for_import,
        #     'fields_for_import': field_for_import,
        #     'class_check' : DICT_MATCHING_CLASS_IMPORT_WITH_CLASS_CHECK[cls_for_import.__name__],
        #     'dict_matching': '',
        #     'dict_result' : dict_result
        # }

        for i in field_for_import:
            key = unicode(cls_for_import._meta.get_field_by_name(i)[0].verbose_name)
            verbose_name_to_import[key] = i

        for i in ws.rows[0]:

            if i.value in field_for_import:
                matching_column_import_with_field_model[i.value] = i.value
                names_check_methods.append(i.value)

            elif i.value in verbose_name_to_import:
                matching_column_import_with_field_model[i.value] = verbose_name_to_import[i.value]
                names_check_methods.append(verbose_name_to_import[i.value])
            else:
                error_column.append(i.value)

        if error_column:
            error_message = u'Не удалось идентифициоровать все колонки в импортируемом файле./n' \
                            'Перечень не идентифицирвоанных колонок:/n'

            for i in error_column:
                error_message += '- ' + i + '/n'

            dict_result.update({
                'status': 'error',
                'message': error_message
            })

            return dict_result

        # import_data['dict_matching'] = matching_column_import_with_field_model


        #Создаем файл для хранения ошибочных записей + добавляем в него колонку "Описание ошибок"
        path_file_error = cls.get_file_template_for_import(cls_for_import)
        wb_error = openpyxl.load_workbook(path_file_error, read_only = False)
        ws_error = wb_error.active
        new_column = len(names_check_methods) + 1
        ws_error.cell(row = 1, column = new_column, value=u'Описание ошибок').font = openpyxl.styles.Font(bold=True)

        #Определяем шаблон заливки ошибочных ячеек
        redFill = openpyxl.styles.PatternFill(start_color='FFFF0000', fill_type='solid')


        count_error = 0
        count_duplicates = 0
        count_correct_records = 0
        idx_file_errors = 2
        for check_row in ws.rows[1:]:

            # Проверям строку на ошибки в данных
            check_values = [x.value for x in check_row]
            result_check = cls.check_row_data(class_check, names_check_methods, check_values)

            if result_check:
                #пишем строку с ошибками в файл для ошибок
                write_to_file_errors()

                text_error = ''.join(result_check)
                ws_error.cell(row= idx_file_errors, column= len(check_row)+1,value= text_error)
                idx_file_errors += 1
                count_error += 1

            else:
                #Иначе проводим проверку на дублирование
                true_check_values = cls.get_true_vlues(cls_for_import, names_check_methods, check_values)
                if cls.check_duplicate(cls_for_import, names_check_methods, true_check_values):

                    write_to_file_errors()

                    ws_error.cell(row= idx_file_errors, column= len(check_row)+1,value= 'Дубль записи в Системе')
                    count_duplicates += 1
                    idx_file_errors += 1

                else:
                    #Иначе считаем запись корректной и сохраняем ее в БД
                    count_correct_records += 1

                    instance_for_save = cls_for_import()
                    for name_field, t_value in zip(names_check_methods, true_check_values):
                        if t_value:
                            setattr(instance_for_save,name_field,t_value)

                    instance_for_save.save()


        wb_error.save(path_file_error)


        # Проверяем данные файла на корректность
        return {
            'count_error' : count_error,
            'count_duplicates' : count_duplicates,
            'count_correct_records' : count_correct_records
            }

        return str(ws.columns[1][1:])


class CheckImportEntityNaturalPerson ():
    """
        Класс, который отвечает за проверку полей класса о физических лицах
    """

    @staticmethod
    def do_check_serial_dul (check_value):

        """
        Проверяем серию удостоверения личности - две проверки:
        1) проверка количества символов (должно быть 4)
        2) проверка типа символов - все должны быть цифрами
        """
        result_check = ''

        if len(check_value) != 4:
            result_check += 'Количество символов в серии ДУЛ отлично от 4;'

        if not check_value.isdigit():
            result_check += 'Серия ДУЛ содержит символы не являщиеся цифрами;'

        return result_check

    @staticmethod
    def do_check_number_dul (check_value):

        """
        Проверяем номер удостоверения личности - две проверки:
        1) проверка количества символов (должно быть 6)
        2) проверка типа символов - все должны быть цифрами
        """
        result_check = ''

        if len(check_value) != 6:
            result_check += 'Количество символов в номере ДУЛ отлично от 6;'

        if not check_value.isdigit():
            result_check += 'Номер ДУЛ содержит символы не являющиеся цифрами;'

        return result_check

    @staticmethod
    def do_check_date_issue_dul (check_value):
        """
        Проверяем дату выдачи удостоверения личности - две проверки:
        1) проверка количества символов (должно быть 10)
        2) проверка типа символов - должно удовлетворять двум шаблонам:
        ЦЦЦЦ-ЦЦ-ЦЦ
        ЦЦ.ЦЦ.ЦЦЦЦ
        """

        result_check = ''

        try:

            datetime.strptime(check_value,'%Y-%m-%d %H:%M:%S').date()

        except ValueError:
            result_check += ('Формат записи даты выдачи ДУЛ не соответствует одному из следующих шаблонов: ДД.ММ.ГГГГ '
                             'или ГГГГ-ММ-ДД;')

        return result_check
"""
    Класс, который отвечает за проверку полей класса о юридических лицах
"""

"""
    Класс, который отвечает за проверку полей класса о технических средствах
"""

"""
    Класс, который отвечает за проверку полей класса о цветах техники
"""

"""
    Класс, который отвечает за проверку полей класса о марках двигателя
"""

"""
    Класс, который отвечает за проверку полей класса о марках технических средств
"""

"""
    Класс, который отвечает за проверку полей класса о выдавшей организации
"""


# Глобавльный словарь который сопоставляет какой класс, какую модель проверяет
DICT_MATCHING_CLASS_IMPORT_WITH_CLASS_CHECK = {'EntityNaturalPerson' : CheckImportEntityNaturalPerson}