from django.contrib import admin

from uploads.models import Upload

class UploadAdmin(admin.ModelAdmin):

    list_display = ('model_name', 'uploaded_at')

admin.site.register(Upload, UploadAdmin)
