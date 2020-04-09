from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from Main.models import Manufacturer, Equipment_type

class ManufAdmin(admin.ModelAdmin):
    pass
admin.site.register(Manufacturer, ManufAdmin)


# class ManufInline(admin.StackedInline):
#     model = Manufacturer
#     can_delete = False
#     verbose_name_plural = 'manufacturer'

# class EqInline(admin.StackedInline):
#     model = Equipment_type
#     can_delete = False
#     verbose_name_plural = 'manufacturer'

# class UserAdmin(BaseUserAdmin):
#     inlines = (ManufInline, EqInline)

# # Re-register UserAdmin
# admin.site.register(ManufInline, UserAdmin)
# admin.site.register(EqInline, UserAdmin)