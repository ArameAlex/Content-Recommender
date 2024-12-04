from django.contrib import admin
from .models import ContentModel, CategoryModel, ViewCountModel
# Register your models here.

admin.site.register(ContentModel)
admin.site.register(CategoryModel)
admin.site.register(ViewCountModel)
