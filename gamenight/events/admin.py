from django.contrib import admin

from .models import Message, Event, Question, Choice
# Register your models here.
admin.site.register(Message)
admin.site.register(Event)
admin.site.register(Question)
admin.site.register(Choice)
