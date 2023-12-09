from django.contrib import admin
from .models import Task, Tag
from django.utils import timezone

class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'timestamp', 'due_date', 'status']
    list_filter = ['status', 'due_date']
    search_fields = ['title', 'description']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'due_date', 'status')
        }),
        ('Tags', {
            'fields': ('tags',),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # If it's a new entry
            obj.timestamp = timezone.now()
        obj.save()

class TagAdmin(admin.ModelAdmin):
    list_display = ['value']
    search_fields = ['value']

admin.site.register(Task, TaskAdmin)
admin.site.register(Tag, TagAdmin)
