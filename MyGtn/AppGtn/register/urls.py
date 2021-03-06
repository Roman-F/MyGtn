__author__ = 'sss'
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
#from . import models
from AppGtn import models


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^fl/', 'AppGtn.views.appgtn_register', {'model': models.EntityNaturalPerson}),
    url(r'^base_form_register/', 'AppGtn.views.appgtn_form_register'),
    url(r'^tech/', 'AppGtn.views.appgtn_register', {'model': models.EntityVehicle}),
    url(r'^vehiclebrand/', 'AppGtn.views.appgtn_register', {'model': models.VehicleBrand}),
    url(r'^vehiclecolor/', 'AppGtn.views.appgtn_register', {'model': models.VehicleColor}),
    url(r'^country/', 'AppGtn.views.appgtn_register', {'model': models.Country}),
    url(r'^template_import/', 'AppGtn.views.appgtn_upload_file_import'),
    url(r'^import_in_system/get_file_with_error/', 'AppGtn.views.appgtn_unload_file_with_import_errors'),
    url(r'^import_in_system/back_in_the_register/', 'AppGtn.views.appgtn_del_file_and_redirect'),
    url(r'^import_in_system/', 'AppGtn.views.appgtn_import_in_system'),
    # url(r'^import_in_system/', 'AppGtn.views.test_multiprocessor_import'),
    url(r'^', 'AppGtn.views.appgtn_main'),

) + static(settings.STATIC_URL)