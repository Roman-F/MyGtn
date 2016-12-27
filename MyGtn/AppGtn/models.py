# coding=utf-8
from django.db import models
from django.forms import ModelForm
from django.conf import settings
from register.functionality.imort_data import ImportDataInSystem

import openpyxl
import random

# Create your models here.


# """абстрактная модель для физ лиц и юр лиц"""
class AbstractEntityPerson (models.Model):

    class Meta:
        abstract = True

    # id = models.AutoField(primary_key=True)
    created_date=models.DateField(auto_now_add=True)
    modifided_date=models.DateField(auto_now=True)
    deleted_date=models.DateField (null=True,blank=True)

    # #блок полей для юридического адреса или адерса регистрации
    # legal_locality=
    # legal_street=
    # legal_house=
    # legal_corps=
    # legal_apartment=
    #
    #
    # #блок полей для юридического адреса или адерса регистрации
    # actual_locality=
    # actual_street=
    # actual_house=
    # actual_corps=
    # actual_apartment=

    comment=models.CharField(max_length=1000,blank=True)

    FIELD_FOR_FORM=None
    EXCLUDE_FIELD_FOR_FORM=None

    FIELD_FOR_IMPORT = 'all'

    FIELD_NOT_FOR_IMPORT = ['id','created_date','modifided_date','deleted_date']

    @classmethod
    def get_class_model_form (cls,field_form=None, exclude_field=None):

        """
        Метод возвращает КЛАСС модельной формы,
        Выводимые и исключаемые поля либо задаются при вызове метода, либо беруться из констант FIELD_FOR_FORM
        и EXCLUDE_FIELD_FOR_FORM , которые определены в cls
        поэтому значение по умолчанию, указанные в определении метода, по сути не используются
        """

        if not field_form:
            field_form=cls.FIELD_FOR_FORM

        if not exclude_field:
            exclude_field=cls.EXCLUDE_FIELD_FOR_FORM

        class FormEntityPerson(ModelForm):
            class Meta:
                model=cls
                fields=field_form
                exclude = exclude_field

        return FormEntityPerson


    @classmethod
    def do_import_in_system (cls,data_file):

        """
        :param data_file: файл с данными для импорта
        :return: HTTPResponse с результатами импорта

        Метод осуществляет вызов метода импорта данных в Систему и обрабатывает результат импорта, в данной реализации
        вернет HTTPResponse с результатом импорта:
        * Положительный - скажет что все ок
        * Отрицательный - скажет сколько ошибочных записей, сколько загрузилось и даст ссылку на файл с ошибками.

        Метод не предполагает вызова из абстрактного класса, только из конкретной модели, имеющую свою таблицу
        """

        ImportDataInSystem.do_import(cls,data_file)




    @classmethod
    def get_file_template_for_import(cls):

        """
        # Метод возвращает полный путь к динамически сформированному xlsx файлу, в котором перечислены поля модели как
        #  заголовки столбцов.
        # Полученный файл предполагается использовать как шаблон файла импорта данных в выбранную модель
        # """
        return ImportDataInSystem.get_file_template_for_import(cls)




    @classmethod
    def import_in_system (cls, data_file):

        """  Метод из полученного файла загружает данные в систему;
             При этом проводит проверки на соответствие:
             - расширению
             - формату
             - отсутствию дублей (можно заменить на свою функцию поиска дублей)
             - корректности значений полей файла (необходимо настраивать для каждого реестра отдельно)

             В результате возвращается словарь с итогами импорта и ссылкой на файл с ошибками
        """

        # wb = openpyxl.load_workbook(data_file,read_only=False)
        # ws = wb.active
        #
        # # Проверяем файл на совпадение количества колонок с количеством допустимым к загрузке
        # data_file_max_column = ws.max_column
        # if cls.FIELD_FOR_IMPORT == 'all' :
        #     max_column_in_template = cls._meta.fields.__len__()
        #     format_is_true = (max_column_in_template == data_file_max_column)
        #
        # else:
        #     max_column_in_template = cls.FIELD_FOR_IMPORT.__len__()
        #     format_is_true = (max_column_in_template == data_file_max_column)
        #
        # if not format_is_true:
        #     raise RuntimeError ('Количество колонок в импортируемом файле(%s) не соответствует количеству в шаблоне(%s)'
        #                         % (data_file_max_column, max_column_in_template) )
        #
        #
        # #читаем файл и сохраняем данные в БД
        #
        # dict_data = []
        # for row in ws.rows:
        #     model_for_save = cls()
        #     if row[0].coordinate == 'A1':
        #         continue
        #     i = 0
        #     for cell in row:
        #         setattr(model_for_save,cls.FIELD_FOR_IMPORT[i],cell.value)
        #         i = i +1
        #     model_for_save.save()
        # #--------------------------------------------
        #
        # return str(dict_data)
        return ImportDataInSystem.do_import(cls,data_file)


class EntityNaturalPerson (AbstractEntityPerson):

    """ Описание сущности филического лица"""

    FIELD_FOR_FORM=['surname','name','middlename','inn','date_of_birth','place_of_birth','serial_dul','number_dul',
                'date_issue_dul']
    # FIELD_FOR_FORM='all'
    EXCLUDE_FIELD_FOR_FORM=None

    FIELD_FOR_IMPORT = ['surname','name','middlename','inn','date_of_birth','place_of_birth','serial_dul','number_dul',
                'date_issue_dul']

    surname=models.CharField(verbose_name='Фамилия',max_length=30)
    name = models.CharField (verbose_name= 'Имя', max_length= 20)
    middlename=models.CharField(verbose_name='Отчество',max_length=30)

    inn = models.PositiveIntegerField(max_length=12,blank=True,null=True)

    date_of_birth=models.DateField()
    place_of_birth=models.CharField(max_length=200, blank=False)

    serial_dul=models.CharField(max_length=4)
    number_dul=models.CharField(max_length=6)
    date_issue_dul=models.DateField()
    #issuing_authority_dul=

    GROUP_FL_VARIANT = (
        ('NP', 'Частное лицо'),
        ('PF', 'Глава КФХ'),
        ('IP', 'Индивидуальный предприниматель'),
    )
    groupfl = models.CharField(max_length=20, choices=GROUP_FL_VARIANT)

    def my_field(self):
        return self.surname.verbose_name

    @classmethod
    def check_import_data_files (file_to_import, file_to_error = None):

        """
        Метод выполняет проверку содержимого импортируемого файла (file_to_import) и возвращает словарь.
        который содержит:
            - путь к файлу с ошибками
            - кортеж с номерами корректных строк в импортируемом файле
            - количество ошибочных записей

        В данном методе реализованы специфические проверки для сущности "Физическое лицо"
        surname= не проверяется
        name = не проверяется
        middlename= не проверяется

        inn = только цифры, только 12 знаков

        date_of_birth= форматы даты, не может быть больше date_issue_dul
        place_of_birth= не проверяется

        serial_dul= только цифры, только 4 цифры
        number_dul= только цифры, только 6 цифры
        date_issue_dul= форматы даты, не может быть больше текущей даты
        """

        tuple_valid_entries =()
        count_error_entries = 0

        wb = openpyxl.load_workbook(file_to_import)
        ws = wb.active

        for row in ws.rows:
            if row[0].coordinate == 'A1':
                continue



        return 'пока еще пишется метод'

# """ Описание сущности юридического лица"""
class EntityLegalPerson (AbstractEntityPerson):
    pass


# """ Описание сущности технического средства"""
class EntityVehicle (AbstractEntityPerson):

    brand=models.ForeignKey('VehicleBrand', verbose_name=u'Марка техники')
    color=models.ForeignKey('VehicleColor',verbose_name=u'Цвет техники')
    country_of_origin=models.ForeignKey('Country',verbose_name=u'Страна происхождения')

    year_of_issue=models.PositiveSmallIntegerField (verbose_name=u'Год выпуска', max_length=4)
    serial_psm=models.CharField(verbose_name=u'Серия ПСМ',max_length=2,blank=True)
    number_psm=models.PositiveIntegerField(verbose_name=u'Номер ПСМ',max_length=6,blank=True)
    date_of_issue_psm=models.DateField(verbose_name=u'Дата выдачи ПСМ',blank=True)
    #issued_organization_psm=

    serial_number=models.CharField(verbose_name=u'Заводской номер',max_length=200,blank=True)
    engine_number=models.CharField(verbose_name=u'Номер двигателя',max_length=500,blank=True)
    transmission_number=models.CharField(verbose_name=u'Номер коробки передач',max_length=500,blank=True)
    bridge_number=models.CharField(verbose_name=u'Номер моста',max_length=500,blank=True)

    # текущая регистрация
    # статус ТС



class FormEntityNaturalPerson(ModelForm):
    class Meta:
        model = EntityNaturalPerson
        fields = ['surname','name', 'middlename', 'inn', 'date_of_birth',
                  'place_of_birth', 'serial_dul', 'number_dul', 'date_issue_dul']


# class FormEntityAppGtn(ModelForm):
#
#     def __init__(self, model_entity, entity_fields=None, exclude_entity_fields=None ):
#
#         self._meta.model= model_entity
#         self._meta.fields= entity_fields
#         self._meta.exclude= exclude_entity_fields
#
#         self.Meta.model= model_entity
#         self.Meta.fields= entity_fields
#         self.Meta.exclude= exclude_entity_fields
#
#         FormEntityAppGtn.Meta.model=model_entity
#         FormEntityAppGtn.Meta.fields=entity_fields
#         FormEntityAppGtn.Meta.exclude=exclude_entity_fields
#
#         super(FormEntityAppGtn,self).__init__()
#
#     class Meta:
#       model = None
#       fields = None
#       exclude = None


#############
#СПРАВОЧНИКИ#
#############
class VehicleColor (AbstractEntityPerson):
    color_name=models.CharField(verbose_name=u'Наименование цвета',max_length=200,unique=True)

class BrandEngine (AbstractEntityPerson):
    name=models.CharField(verbose_name=u'Марка двигателя',max_length=200,unique=True)

class OrganizationIssue(AbstractEntityPerson):
    name=models.CharField(verbose_name=u'Выдавшая организация',max_length=300,unique=True)
    addr=models.CharField(verbose_name=u'Адрес организации',max_length=300)

class Country(AbstractEntityPerson):
    full_name=models.CharField(verbose_name=u'Полное наименование',max_length=200,unique=True)
    short_name=models.CharField(verbose_name=u'Краткое наименование',max_length=100,unique=True)
    code=models.IntegerField(verbose_name=u'Код страны',max_length=3,unique=True)
    alpha_2=models.CharField(verbose_name=u'Код альфа-2',max_length=2,unique=True)
    alpha_3=models.CharField(verbose_name=u'Код альфа-2',max_length=3,unique=True)

class Manufacturer(AbstractEntityPerson):
    country=models.ForeignKey(Country,verbose_name=u'Страна производителя')
    name=models.CharField(verbose_name=u'Выдавшая организация',max_length=300,unique=True)
    addr=models.CharField(verbose_name=u'Адрес производителя', max_length=300)


class KindVehicle (AbstractEntityPerson):
    code= models.PositiveSmallIntegerField(verbose_name= u'Код вида', max_length=3, unique=True)
    name= models.CharField(verbose_name=u'Вид транспортного средства', max_length=100, unique=True)

class TypeProp (AbstractEntityPerson):
    name=models.CharField(verbose_name=u'Тип движителя',max_length=100,unique=True)

class TypeAndGroupVehicle(AbstractEntityPerson):
    parent_id=models.PositiveIntegerField(verbose_name=u'ID родителя')
    name=models.CharField(verbose_name=u'Наименование', max_length=300)
    level=models.PositiveSmallIntegerField(verbose_name=u'Уровень записи', max_length=1)

class VehicleEngine(AbstractEntityPerson):
    brand_engine=models.ForeignKey(BrandEngine,verbose_name=u'Maрка двигателя')
    power_kwt=models.DecimalField(verbose_name=u'Мощность двигателя(кВт)', max_digits=8, decimal_places=2)
    power_hp=models.DecimalField(verbose_name=u'Мощность двигателя(Л.с.)', max_digits=8, decimal_places=2)
    working_voluem=models.PositiveIntegerField(verbose_name=u'Рабочий объем',max_length=10,default=0)

    TYPE_ENGINE=(
        ('0','двигатель внутреннего сгорания'),
        ('1','электрический двигатель'),
    )

    type_engine=models.CharField(verbose_name='Тип двигателя',max_length=30,choices=TYPE_ENGINE)

    brand_vehicle=models.ManyToManyField('VehicleBrand',verbose_name=u'Марка теники',blank=True)


class VehicleBrand(AbstractEntityPerson):
    name=models.CharField(verbose_name=u'Марка',max_length=200)
    type_brand=models.ForeignKey(TypeAndGroupVehicle,verbose_name=u'Тип(наименование) марки')
    manufacturer=models.ForeignKey(Manufacturer,verbose_name=u'Производитель')

    BRAND_CATEGORY=(
        ('0','AI'),
        ('1','AII'),
        ('2','AIII'),
        ('3','AIV'),
        ('4','B'),
        ('5','C'),
        ('6','D'),
        ('7','E'),
        ('8','F'),
        ('9','Отсутствует'),
    )

    brand_category=models.CharField(verbose_name=u'',max_length=11,choices=BRAND_CATEGORY)

    weight=models.DecimalField(verbose_name='Масса', max_digits=10, decimal_places=2)
    max_speed=models.DecimalField(verbose_name='Макс. скорость', max_digits=10, decimal_places=2)
    length=models.DecimalField(verbose_name='Длина', max_digits=10, decimal_places=2)
    width=models.DecimalField(verbose_name='Ширина', max_digits=10, decimal_places=2)
    heigth=models.DecimalField(verbose_name='Высота', max_digits=10, decimal_places=2)

    sertificate_number=models.CharField(verbose_name='Номер сертификата',max_length=30, blank=True)
    sertificate_data=models.DateField(verbose_name='Дата выдачи', blank=True)
    sirtificate_issue=models.ForeignKey(OrganizationIssue,verbose_name='Выдавшая организация', blank=True)

    kind_vihicle=models.ForeignKey(KindVehicle,verbose_name='Вид транспортного средства')
    type_prop=models.ForeignKey(TypeProp,verbose_name='Тип движителя')

    brand_engine=models.ManyToManyField(VehicleEngine,verbose_name=u'Двигатель',blank=True)

#СПРАВОЧНИКИ КОНЕЦ#
###################