from django.contrib import admin

# Register your models here.
from polls.models import Poll

class PollAdmin(admin.ModelAdmin):
	fields = ['pub_date', 'question']

admin.site.register(Poll, PollAdmin)