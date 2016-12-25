from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MyGtn.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^register/',include('AppGtn.register.urls')),
    #url(r'^formfl/','AppGtn.views.appgtn_form_register_natural_person'),
    url(r'^in_file/','AppGtn.views.appgtn_in_file_register_natural_person'),
) + static(settings.STATIC_URL)
