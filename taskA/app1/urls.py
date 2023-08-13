
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),

    # path('loginS',views.show_login_page),  
    # path('register',views.register),
    # path('success',views.success),
    path('login',views.login),
    path('logout',views.logout),
    path('dashboard',views.dashboard),

    path('addCustomerPage',views.addCustomerPage),
    path('addCustomer',views.addCustomer),
    path('deleteCustomer/<int:custId>',views.deleteCustomer),

    path('updateCustomerPage/<int:custId>',views.updateCustomerPage),
    path('updateCustomer/<int:custId>',views.updateCustomer),

    path('addServicePage',views.addServicePage),
    path('addService',views.addService),

    path('activation/<int:ActiveID>/<int:custId>',views.activation),

    path('search', views.search), #search bar
    path('result',views.result),

    path('addServiceToCus/<int:servId>/<int:custId>',views.addServiceToCus),



    # هون ضيف باث جديد للريدايركت
]