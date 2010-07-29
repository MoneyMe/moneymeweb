from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()
import settings

urlpatterns = patterns('',
    # Example:
    # (r'^moneymeweb/', include('moneymeweb.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^admin/', include(admin.site.urls)),
    (r'^api/', include('moneymeweb.api.urls')),
    (r'^public/(.*)$', 'django.views.static.serve',
        {'document_root' : settings.MEDIA_ROOT} ),
    url(r'^login/', 'django.contrib.auth.views.login', 
        {'template_name': 'login.html'},
        name="login_url"),
    url(r'^logout/', 'django.contrib.auth.views.logout_then_login', 
        {'template_name': 'logout.html'}, 
        name="logout_url"),
    url(r'^main/', 'expense.views.main', name="main"),
    url(r'^user/home', 'expense.views.user_home', name="user_home"),
    url(r'^supplier/home', 'expense.views.supplier_home', name="supplier_home"),

)
