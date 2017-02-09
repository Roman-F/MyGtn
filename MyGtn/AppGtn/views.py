# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import get_model
from django.conf import settings

from AppGtn.register import urls

import random
import os

# Create your views here.
PATH_NATURAL_PERSON = 'AppGtn/register/templates/'

# Словарь соответствия имени модели шаблону отображения реестра
DICT_TEMPLATES_FOR_REGISTER_DISPLAY = {'EntityNaturalPerson': 'register_natural_person.html',
                                       'EntityVehicle': 'register_vehicles.html',
                                       'VehicleColor': 'vehicle_color.html',
                                       'VehicleBrand': 'vehicle_brand.html/',
                                       'Country': 'country.html'
                                       }

# Словарь соответствия имени модели и адресу реестра, ее отображающего
#TODO: придумать как использовать \register\urls.py , там эта информация уже есть (нарушен принцип DRY)
DICT_URL_PATH_TO_REGISTER = {'EntityNaturalPerson': '/register/fl/',
                             'EntityVehicle': '/register/tech/',
                             'VehicleColor': '/register/vehiclecolor/',
                             'VehicleBrand': '/register/vehiclebrand/',
                             'Country': '/register/country/'
                             }


def get_response_to_unload_file (path_to_file, name_file_for_user = '', remove_file = False):

    '''
        Функция читает полученный файл в двоичном режиме.
        По прочитанным данным формирует и возвращает объект HttpResponse.
        Удаляет прочитанный файл, если remove_file = True

        :param path_to_file: Путь к файлу, по которому нужно сформровать HttpResponse.
        :param name_file_for_user: Имя файла, которое будет отображаться пользователю при скачивании
        :param remove_file: если True - то прочитаный файл будет удален
        :return: объект HttpResponse
    '''

    if name_file_for_user == '':
        name_file_for_user = os.path.basename(path_to_file)

    # формируем response с файлом для отдачи пользователю
    with open(path_to_file, 'rb') as myfile:
        response = HttpResponse(myfile.read(), content_type='application')
        response['Content-Disposition'] = 'attachment; filename= ' + name_file_for_user

    if remove_file:
        os.remove(myfile.name)

    return response


def appgtn_register(request,model):
    """
        Общее представление для реестров и справочников
    """
    #TODO: обработать случай когда модель не получена (model is None)
    #TODO: обработать случай когда в БД нет данных

    test = urls.urlpatterns

    NAMES_NO_DISPLAYED_FIELDS = ['id','created_date','modifided_date','deleted_date']

    list_fields  = tuple(field[0] for field in model._meta.get_fields_with_model()
                                            if field[0].name not in NAMES_NO_DISPLAYED_FIELDS)

    #TODO: доработать получение значения, чтобы для связанных полей в место ID выводились нужные значения
    list_dict_values = model.objects.all().values(*(map(lambda x: x.name, list_fields)))

    table_headers = tuple(x.verbose_name for x in list_fields)

    # Формируем кортеж кортежей со значениями из БД, в порядке следования полей в
    tuple_tuples_values = tuple(tuple(dict_values[x.name] for x in list_fields) for dict_values in list_dict_values)

    path_to_template = "base_register.html"

    return render(request, path_to_template, {"table_headers": table_headers
                                                ,"tuple_tuples_values": tuple_tuples_values
                                                ,"model": model.__name__})

def appgtn_form_register(request):
    """
        Общая вьюха добавления новой или изменения имеющейся записи реестра (справочника)
    """
    #TODO: для изменения записей необходимо определить как пользователь будет выбирать нужную запись

    name_model = request.POST.get('NameRegisterModel', 'Модель не найдена')
    model_used = get_model('AppGtn', name_model)
    id_record = request.POST.get('id_record', '')

    if request.POST.get('save', ''):

        if id_record:
            data_model = model_used.objects.get(pk=int(id_record))
            form = model_used.get_class_model_form()(request.POST, instance=data_model)
        else:
            form = model_used.get_class_model_form()(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(DICT_URL_PATH_TO_REGISTER[name_model])

    elif id_record:

        data_model = model_used.objects.get(pk=int(id_record))
        meta = model_used._meta
        dict_to_json = {fields.name: data_model.__getattribute__(fields.name) for fields in meta.fields}
        form = model_used.get_class_model_form()(initial=dict_to_json)

    else:
         form=model_used.get_class_model_form()()

    # path_to_template = DICT_TEMPLATES_FOR_FORMS_CHANGES[name_model]
    path_to_template = 'base_form_register.html'

    return render(request, path_to_template, {'form': form
                                              ,'id_record': id_record
                                              ,'path_back':DICT_URL_PATH_TO_REGISTER[name_model]
                                              ,'model': request.POST.get('NameRegisterModel',
                                                                        'Модель не передана')})


def appgtn_upload_file_import (request):

    '''
        Вьюха выгружает пользователю файл шаблона импорта.
        Шаблон формируется по модели полученной из запроса.
        Т.к. вьюха общая для всех моделей, то файлы генерируются каждый раз при запросе, а не берутся готовые шаблоны.
        Соответственно, файл шаблона, после выгрузки удаляется
    '''

    name_model = request.POST.get('NameRegisterModel', 'Модель не найдена')
    model_for_file = get_model('AppGtn', name_model)

    path_to_template_import = model_for_file.get_file_template_for_import()

    filename = name_model + str(random.randint(1000, 9999)) + '.xlsx'

    return get_response_to_unload_file(path_to_template_import, name_file_for_user=filename, remove_file=True)

def appgtn_import_in_system(request):

    """
        Вьюха берет данные из файла, опеделяет модель для импорта и импортирует данные в систему
    """

    name_model = request.POST.get('NameRegisterModel', 'Модель не найдена')
    model_for_file = get_model('AppGtn', name_model)

    file_data = request.FILES['file_to_import']

    path_work_file = settings.MEDIA_ROOT+file_data.name
    with open(path_work_file, 'wb') as work_file:
        for chunk in file_data.chunks():
            work_file.write(chunk)

    try:
        # result_import = model_for_file.import_in_system(path_work_file)
        result_import = model_for_file.multiprocessor_import_in_system(path_work_file)
    except RuntimeError as result_import:
        return render(request, 'template_test.html', {'parametr': result_import})
    finally:
        os.remove(path_work_file)

    return  render(request, 'result_import.html',
                   {'status_import': result_import['message'],
                    'number_of_records': result_import['number_of_records'],
                    'number_of_imported': result_import['number_of_imported'],
                    'number_of_errors': result_import['number_of_errors'],
                    'number_of_duplicates': result_import['number_of_duplicates'],
                    'link_to_file_errors': result_import['link_to_file_errors'],
                    'path_back': DICT_URL_PATH_TO_REGISTER[name_model]
                    })


def appgtn_unload_file_with_import_errors (request):

    """
        Вьюха отадает пользователю файл с ошибками импорта данных в Систему.
        Нужный файл определяется по значению "PathToFileError" из запроса.

        :param request: поступивший запрос
        :return: объект HttpResponse содержащий запрашиваемый файл в двоичном режиме
    """
    return get_response_to_unload_file(request.POST['PathToFileError'])


def appgtn_del_file_and_redirect (request):

    """
        Вюха удаляет файл на сервере (путь определяется по параметру запроса "PathToFileError").
        Далее вьюха переадресовывает пользователя на страницу указанную в параметре "PathBack"

        :param request: поступивший запрос
        :return: Перенаправление на на страницу указанную в параметре "PathBack"
    """

    os.remove(request.POST['PathToFileError'])

    return HttpResponseRedirect(request.POST['PathBack'])


def appgtn_main (request):

    """
        Вьюха выводит главную страницу для выбора реестров или справочников

        :param request: поступивший запрос
        :return: объект HttpResponse с данными главной страницы
    """

    return  render(request,'main.html')


def test_multiprocessor_import(request):

    '''
        Вьюха для тестирования и отладки импорта через много процессорность
    :param request:
    :return:
    '''

    name_model = request.POST.get('NameRegisterModel', 'Модель не найдена')
    model_for_file = get_model('AppGtn', name_model)

    file_data = request.FILES['file_to_import']

    path_work_file = settings.MEDIA_ROOT+file_data.name
    with open (path_work_file,'wb') as work_file:
        for chunk in file_data.chunks():
            work_file.write(chunk)

    try:
        result_import = model_for_file.multiprocessor_import_in_system(path_work_file)
    except RuntimeError as result_import:
        return render(request,'template_test.html',{'parametr':result_import})
    finally:
        os.remove(path_work_file)

    return render(request,'template_test.html',{'parametr':result_import})


    # #####Попытки переименовать временный файл######
    # # получаем абсолютный путь к файлу
    # abs_file_data = file_data.file.name
    # # f = open (abs_file_data.replace('\\','\\'))
    # # получаем расширение загруженного файла (именно которого грузили, а не которого сохранила Система)
    # file_name,file_extension = file_data.name.rpartition('.')[::2]
    #
    # abs_file_data_path = abs_file_data.rpartition('.')[0]
    #
    # # меняем у загруженного файла расширение с ".upload" на исходный
    # # os.rename(abs_file_data.replace('\\',"/"),str(abs_file_data_path.replace('\\',"/") + '.' + file_extension))
    #
    # os.replace(abs_file_data,abs_file_data_path + '.' + file_extension)
    # #как ни странно, но для получения абсолютного пути к файлу необходимо обратится к атриббуту "file", а затем к "name"
    #
    #
    # result_import = model_for_file.import_in_system(abs_file_data)
    #
    # # result_import = request.FILES['file_to_import'].temporary_file_path
    # # result_import = openpyxl.load_workbook(r'c:\users\sss\appdata\local\temp\krakec.upload'.replace('\\',"/"))
    #
    # ###############################################