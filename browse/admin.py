from django.contrib import admin
from browse.models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin

#for allele
class AlleleResource(resources.ModelResource):
    class Meta:
        model = Allele

class AlleleAdmin(ImportExportModelAdmin):
    list_display = ('id_uuid','type','genomerefno1','strain1','locus1','genomerefno2','strain2','locus2')
    list_filter = ['type']
    search_fields = ['id_uuid','type','genomerefno1','genomerefno2']
    change_list_template = 'smuggler/change_list.html'
    resource_class = AlleleResource
    pass

#for AlleleStatistics
class AlleleStatisticsResource(resources.ModelResource):
    class Meta:
        model = AlleleStatistics

class AlleleStatisticsAdmin(ImportExportModelAdmin):
    list_display = ('id_uuid','genomerefno','strain','locus','allelelist','alleletypeno')
    search_fields = ['id_uuid','genomerefno']
    change_list_template = 'smuggler/change_list.html'
    resource_class = AlleleStatisticsResource
    pass

#for Fragment
class FragmentResource(resources.ModelResource):
    class Meta:
        model = Fragment

class FragmentAdmin(ImportExportModelAdmin):
    list_display = ('id','locus','gino','type','genomerefno')
    search_fields = ['id','locus']
    change_list_template = 'smuggler/change_list.html'
    resource_class = FragmentResource
    pass

#for Genome
class GenomeResource(resources.ModelResource):
    class Meta:
        model = Genome

class GenomeAdmin(ImportExportModelAdmin):
    list_display = ('genomerefno','genometype','genenum','gino','uidno','genomename')
    search_fields = ['genomerefno','genometype','gino','genomename']
    change_list_template = 'smuggler/change_list.html'
    resource_class = GenomeResource
    pass

#for homology
class HomologyResource(resources.ModelResource):
    class Meta:
        model = Homology

class HomologyAdmin(ImportExportModelAdmin):
    list_display = ('id','genomerefno','strain','type','locus','homotype')
    search_fields = ['id','genomerefno','strain']
    change_list_template = 'smuggler/change_list.html'
    resource_class = HomologyResource
    pass

#for Protein
class ProteinResource(resources.ModelResource):
    class Meta:
        model = Protein

class ProteinAdmin(ImportExportModelAdmin):
    list_display = ('id_uuid','id_fragment','genomerefno','strain','locus','pid')
    search_fields = ['id_uuid','id_fragment','genomerefno']
    change_list_template = 'smuggler/change_list.html'
    resource_class = ProteinResource
    pass

#for Reanno
class ReannoResource(resources.ModelResource):
    class Meta:
        model = Reanno

class ReannoAdmin(ImportExportModelAdmin):
    list_display = ('id_uuid','id','type','id_original','genomerefno','strain')
    search_fields = ['id_uuid','id','type']
    change_list_template = 'smuggler/change_list.html'
    resource_class = ReannoResource
    pass

#for Repeat
class RepeatResource(resources.ModelResource):
    class Meta:
        model = Repeat

class RepeatAdmin(ImportExportModelAdmin):
    list_display = ('id_uuid','id','type','id_original','genomerefno','strain')
    search_fields = ['id_uuid','id','type']
    change_list_template = 'smuggler/change_list.html'
    resource_class = RepeatResource
    pass

#for expression profile
class ExpressionProfileResource(resources.ModelResource):
    class Meta:
        model = ExpressionProfile

class ExpressionProfileAdmin(ImportExportModelAdmin):
    list_display = ('locus','genomerefno','genename','classnum','number_37_vs_26celsius','cold_shock','heat_shock')
    search_fields = ['locus','genomerefno','genename']
    change_list_template = 'smuggler/change_list.html'
    resource_class = ExpressionProfileResource
    pass


# register the admin class
admin.site.register(Allele,AlleleAdmin)
admin.site.register(AlleleStatistics,AlleleStatisticsAdmin)
admin.site.register(Fragment,FragmentAdmin)
admin.site.register(Genome,GenomeAdmin)
admin.site.register(Homology,HomologyAdmin)
admin.site.register(Protein,ProteinAdmin)
admin.site.register(Reanno,ReannoAdmin)
admin.site.register(Repeat,RepeatAdmin)
admin.site.register(ExpressionProfile,ExpressionProfileAdmin)
