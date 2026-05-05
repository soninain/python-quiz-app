from django.contrib import admin
from .models import *

# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
    list_display =("id","question", 'course')
    search_fields = ("question",)


class ContactAdmin(admin.ModelAdmin):
    list_display =("id","name", 'email','message')
    search_fields = ("name",)
admin.site.register(ContactForm,ContactAdmin)

admin.site.register(UserInfo)
admin.site.register(Course)
admin.site.register(Questions,QuestionAdmin)




