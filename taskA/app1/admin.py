from django.contrib import admin

  # THIS SECTION IS NEW!
  # ********************
from app1.models import User as U, Customer, Service, Active
class UAdmin(admin.ModelAdmin):
    pass
admin.site.register(U, UAdmin)
class CustomerAdmin(admin.ModelAdmin):
    pass
admin.site.register(Customer, CustomerAdmin)
class ServiceAdmin(admin.ModelAdmin):
    pass
admin.site.register(Service, ServiceAdmin)
class ActiveAdmin(admin.ModelAdmin):
    pass
admin.site.register(Active, ActiveAdmin)
