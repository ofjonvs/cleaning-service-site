from django.contrib import admin
from .models import Question, Response

# Register your models here.

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('order', 'prompt', 'answers')
    list_display_links = ('prompt',)
    list_editable = ('order',)


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('answer', 'no_attempts', 'created_at')
    readonly_fields = ('answer', 'no_attempts', 'created_at')
