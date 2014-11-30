from django.contrib import admin
from about.models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.
#for Srna
class staticticsModelResource(resources.ModelResource):
    class Meta:
        model = staticticsModel

class staticticsModelAdmin(ImportExportModelAdmin):
    list_display = ('tableName','itemNumber','source','notes')
    search_fields = ['tableName']
    change_list_template = 'smuggler/change_list.html'
    resource_class = staticticsModelResource
    pass

# register the admin class
admin.site.register(staticticsModel,staticticsModelAdmin)