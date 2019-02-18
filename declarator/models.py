from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

make_doc_path='./documentfiles'


class Office(MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    name = models.TextField(verbose_name='full name')
    sort_order = models.IntegerField(default=0, verbose_name='sort order')
 
    def __str__(self):
        return self.name


class Document(models.Model):
    office = TreeForeignKey(Office, on_delete=models.CASCADE, verbose_name="authority")
    income_year = models.IntegerField(verbose_name="year of income")
   
    def __str__(self):
        return '{} {} {}'.format(str(self.income_year), self.office,'Anti-corruption declaration')


class DocumentFile(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, verbose_name="declaration")
    file = models.FileField(blank=True, max_length=255, null=True,
                        upload_to=make_doc_path, verbose_name="file")

    def __str__(self):
        return '{} {}'.format(self.document, self.file.name)
