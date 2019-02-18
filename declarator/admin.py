from django.contrib import admin
from declarator.models import Document, DocumentFile, Office
from mptt.admin import MPTTModelAdmin
from django.db.models import Count, Q, Prefetch


@admin.register(Office)
class OfficeAdmin(MPTTModelAdmin):
    list_display = ('name', 'related_documents_count',
                    'documents_null', 'documents_not_null')
    # list_display_links = ('indented_title',)

    def get_queryset(self, request):
    
        qs = super().get_queryset(request)

        qs = Office.objects.add_related_count(qs,
                 Document,
                 'office',
                 'documents_count',
                 cumulative=False).annotate(
                    documents_null=Count('document__documentfile',\
                                filter=Q(document__documentfile__file='')),
                    documents_not_null=Count('document__documentfile',\
                                filter=~Q(document__documentfile__file=''))
                    )
        return qs

    def related_documents_count(self, instance):
        return instance.documents_count
    related_documents_count.short_description = 'Related documents (for this specific office)'

    def documents_null(self, instance):
        return instance.documents_null
    documents_null.short_description = 'Related files which are null'

    def documents_not_null(self, instance):
        return instance.documents_not_null
    documents_not_null.short_description = 'Related files which are not null'


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    pass


@admin.register(DocumentFile)
class DocumentFileAdmin(admin.ModelAdmin):
    pass
