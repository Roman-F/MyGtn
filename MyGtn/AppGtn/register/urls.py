__author__ = 'sss'
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
#from . import models
from AppGtn import models


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MyGtn.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^fl/','AppGtn.views.appgtn_register',{'model':models.EntityNaturalPerson}),
    url(r'^formfl/','AppGtn.views.appgtn_form_register'),
    url(r'^tech/','AppGtn.views.appgtn_register',{'model':models.EntityVehicle}),
    url(r'^template_import/','AppGtn.views.appgtn_upload_file_import'),
    url(r'^import_in_system/','AppGtn.views.appgtn_import_in_system'),

    #url(r'fl_in_file/','AppGtn.views.appgtn_in_file_register_natural_person'),
) + static(settings.STATIC_URL)