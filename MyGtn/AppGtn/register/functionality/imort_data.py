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
            Метод формирует файл-шаблон для дальнейшего заполнения.
            В файл пишуться заголовки столбцов, название которых берется из verbose_name

            :param cls_for_template: класс модели для которйо осуществляется формирвоания файла
            :return: полный путь к сформированному файлу
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


    @staticmethod
    def get_true_vlues (cls_for_import, names_check_fields, check_values):

        """
        Метод находит связанные поля в модели, для которой осуществляется импорт.
        Далее метод определяет для найденных связанных полей, по импортируемым данным,
            действительные ("Истинные") значения (в данном случае экземпляр связаной модели целиком)
        Решаемая задача (на примере технического средства (далее - ТС)):
            Импортируется запись о ТС.
            Модель ТС содержит связанное поле "Цвет", которое ссылается на справочник "Цвет ТС".
            В БД, в таблице ТС в колонке "Цвет" хранится ID цвета из справочника "Цвет ТС".
            В тоже время, в импортируемом файле указывается значение цвета, а не его ID (что естетственно, т.к.
                пользователь не знает ID цветов)
            Т.к. типы имортируемых значений для связанных полей и типы связанных полей в БД не совпадают,
                то действовать "в лоб" нельзя.
            Т.о. предварительно необходимо найти по импортируемым значениям соответствующие им экземпляры связанных моделей
                и уже после этого проводить дальнейшую обработку (искать дубли, сохранять данные в БД)

        Нюансы реализации:
            1) Т.к. заренее не известно по какой модели будет проводится импорт, то необходимо проверять все поля модели
               на "связанность"
            2) Аналогично и для связанных моделей:
                т.к. заранее не известна связанная модель, то нельзя определить по какому полю нужно искать
                    импортируемое значение.
                соответственно, необходимо искать импортируемое значение по всем полям модели.
            3) Для корректно сравнения значений проверяемых полей с искомым значением осуществлятся приведение типа:
                приведение типа и сравнение осуществляется на стороне БД, т.к. это менее ресурсоемко чем в Приложении;
            4) Для пустых импортируемых значений (None) поиск не проводится
            5) В результат берем экземпляр связанной модели целиком, т.к. этот экземпляр необходимо указывать при сохранении
                экземпляра импортируемой модели.
            6) Т.к. нет механизма разрешения ситуации когда найденно несколько разных записей с искомым значением,
                то берем первое попавшееся, поэтому в запросе устанавливается ограничеие LIMIT 1

        :param cls_for_import: класс модели для которой осуществляется импорт
        :param names_check_fields: наименование полей модели по которым проводится импорт
        :param check_values: импортируемые значения
        :return: список импортируемых значений, в котором значения для связанных полей заменены соответствующими им
            экземплярами3
        """
        #TODO: https://docs.djangoproject.com/en/1.10/ref/models/meta/ - анализ на упрощение текущего кода
        check_related_generator = (cls_for_import._meta.get_field_by_name(name)[0].rel.to
                                   if cls_for_import._meta.get_field_by_name(name)[0].rel else False
                                   for name in names_check_fields)

        true_check_values=[]

        for related_class, value in zip(check_related_generator,check_values):

            true_value = False

            if related_class and value != None:

                str_column = ','.join(field[0].column for field in related_class._meta.get_fields_with_model())
                str_cast_func = "CAST((%s) as text)" % str_column

                #Ищем связанный объект в связанной модели
                '''
                    Дефолтный, но не рабочий вариант:
                    related_class.objects.extra(where=['CAST((%s) as text) ~ %s'],params=[str_column,value])
                    Дефолтный вариант не заработал, т.к. в итоговом запросе str_column обернут в дополнительные кавычки,
                       отчего SQL воспринимает str_column как одну строку, а не перечнь наименований колонок.
                       В результате получаем пустой результат.
                       Поэтому функцию приведения типа на стороне БД CAST() оформляем стандартно (str_cast_func)
                '''
                true_value = related_class.objects.extra(where=[str_cast_func +' ~ %s']
                                                         ,params=[value])[:1]

            if true_value:
                true_check_values.append(true_value[0])
            else:
                true_check_values.append(value)

        return true_check_values

    @staticmethod
    def check_row_data (class_check, fields_name, check_values):

        """
            Метод проводит проверку данных (check_values) на корректность (согласно логике классов проверки)

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
            Метод проверки на дублирование записи (check_values) в системе

            :param cls_for_import: класс модели, в которую осуществляется импорт
            :param fields_name: список имен полей, по которым будет проводится поиск дублей
            :param check_values: список значений для полей (fields_name), по которым будет проводится поиск дублей
            :return: True - если дубль, иначе False
        """

        param_for_filter = {key:datetime.date(value) if isinstance(value,datetime) else value
                                        for key,value in zip (fields_name, check_values) if value}

        return True if cls_for_import.objects.filter(**param_for_filter)[:1].exists() else False



    @classmethod
    def do_import (cls, cls_for_import, data_file):

        """
            Метод из полученного файла загружает данные в систему;
             При этом проводит проверки на соответствие:
             - расширению
             - формату
             - отсутствию дублей (можно заменить на свою функцию поиска дублей)
             - корректности значений полей файла (необходимо настраивать для каждого реестра отдельно)

             В результате возвращается cловарь с итогами импорта и путем к файлу с ошибками

            :param cls_for_import: класс модели, для которой осуществляется импорт
            :param data_file: файл с данными для импорта
            :return: cловарь с итогами импорта и путем к файлу с ошибками
        """
        #TODO: метод большой - нужно уменьшить

        def write_to_file_errors ():
            for idx_column, check_cell in enumerate(check_row):
                        cell_error = ws_error.cell(row= idx_file_errors, column= idx_column+1, value= check_cell.value)
                        cell_error.font = check_cell.font

                        if result_check and result_check[idx_column]:
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

        #TODO: https://docs.djangoproject.com/en/1.10/ref/models/meta/ - анализ на упрощение текущего кода
        for field in field_for_import:
            pre_key = cls_for_import._meta.get_field_by_name(field)[0]

            if type(pre_key).__name__ != 'RelatedObject':
                key = pre_key.verbose_name
                verbose_name_to_import[key] = field
            else:
                continue

        for cell in ws.rows[0]:

            if cell.value in field_for_import:
                matching_column_import_with_field_model[cell.value] = cell.value
                names_check_methods.append(cell.value)

            elif cell.value in verbose_name_to_import:
                matching_column_import_with_field_model[cell.value] = verbose_name_to_import[cell.value]
                names_check_methods.append(verbose_name_to_import[cell.value])
            else:
                error_column.append(cell.value)

        if error_column:

            import_status = 'Fatal error'

            error_message = (u'Импорт невозможен. Не удалось идентифициоровать все колонки в импортируемом файле.'
                             u' Перечень не идентифицирвоанных колонок: ')

            for error in error_column:
                error_message += error + ','

            dict_result.update({
                'status': import_status,
                'message': error_message
            })

            return dict_result

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


        if (count_error or count_duplicates) and count_correct_records:
            import_status = 'Error'
            error_message = (u'Данные загружены частично.'
                             u' В импортируемых данных обнаружены записи с ошибками или дубликаты.')

        elif (count_error or count_duplicates) and not count_correct_records:
            import_status = 'Error'
            error_message = (u'Нет данных для загрузки.'
                             u' В импортируемых данных обнаружены записи с ошибками или дубликаты.')
        else:
            import_status = u'Успех.'
            error_message = u'Загружены все записи.'

        dict_result.update({
            'status': import_status,
            'message': error_message,
            'number_of_records': len(ws.rows) - 1,
            'number_of_imported': count_correct_records,
            'number_of_errors': count_error,
            'number_of_duplicates': count_duplicates,
            'link_to_file_errors': path_file_error
        })

        return dict_result


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

class CheckImportEntityVehicle ():

    """
        Класс, который отвечает за проверку полей класса о юридических лицах
    """
    pass


#TODO добавить """ Класс, который отвечает за проверку полей класса о технических средствах """

class CheckImportVehicleColor ():
    """
        Класс, который отвечает за проверку полей класса о цветах техники
    """
    pass


#TODO добавить """ Класс, который отвечает за проверку полей класса о марках двигателя """

#TODO добавить """ Класс, который отвечает за проверку полей класса о марках технических средств """

#TODO добавить """ Класс, который отвечает за проверку полей класса о выдавшей организации """


# Глобавльный словарь который сопоставляет какой класс, какую модель проверяет
DICT_MATCHING_CLASS_IMPORT_WITH_CLASS_CHECK = {'EntityNaturalPerson' : CheckImportEntityNaturalPerson,
                                               'VehicleColor' : CheckImportVehicleColor,
                                               'EntityVehicle' : CheckImportEntityVehicle}