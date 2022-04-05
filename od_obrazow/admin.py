from django.contrib import admin
from .models import MultiMedia

class MultiMedia_Admin(admin.ModelAdmin):
    list_display = ('title', 'when')

admin.site.register(MultiMedia, MultiMedia_Admin)
# Register your models here.
