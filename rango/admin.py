from django.contrib import admin
from rango.models import Category, Page, PageAdmin, UserProfile
# Register your models here.

admin.site.register(Category)
#admin.site.register(Page)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)