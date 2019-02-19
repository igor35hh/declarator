from django.views.generic import ListView
from declarators.models import Document, DocumentFile, Office


class OfficeListView(ListView):
    model = Office
    context_object_name = 'offises'
    paginate_by = 5
    template_name = 'declarator/list.html'

    def get_sql_query(self, id=False):
        # for postgresql database

        sql_query = '''

            with current_all_years as (
                select income_year
                from declarators_document
                group by income_year 
                order by income_year desc
            )
            
            select id, parent_id, tree_id, lft, rght, level, sort_order, name,
            array(
            select array[current_all_years.income_year,
            coalesce(docs_year.documentall::integer,0), 
            coalesce(docs_year.documentfilesnull::integer,0), 
            coalesce(docs_year.documentfiles::integer,0)] 
            from current_all_years
            
            left join
            (select income_year,
            count(id) as documentall,
            coalesce(sum(files.null_count), 0) as documentfilesnull,
            coalesce(sum(files.not_null_count), 0) as documentfiles 
            from declarators_document as docs
            
            left join (
            select document_id,
            count(id) filter (where file='') as null_count,
            count(id) filter (where file!='') as not_null_count 
            from declarators_documentfile
            group by document_id
            ) as files on docs.id=files.document_id
            
            where office_id=declarators_office.id
            group by docs.income_year
            ) as docs_year on current_all_years.income_year=docs_year.income_year
            
            ) as document_related
            from declarators_office'''

        if id:
            sql_query += '''
                 where {} = %(where_id)s 
                ''' 

        sql_query += '''
            order by tree_id asc, lft asc
            '''
        return sql_query

    def get_set_of_years(self):
        if not hasattr(self, "set_of_years"):
            qs_documents=Document.objects.all()
            set_of_years=set(item.income_year for item in qs_documents)
            self.set_of_years = sorted(set_of_years, reverse=True)

        return self.set_of_years

    def get(self, request, *args, **kwargs):

        office_id = kwargs.get('office_id', '')
        parent_id = kwargs.get('parent_id', 0)
        if office_id:

            sql_query = self.get_sql_query(True)

            if int(parent_id) != 0:
                qs =Office.objects.raw(\
                    sql_query.format('parent_id'), params={'where_id': office_id})
            else:
                qs =Office.objects.raw(\
                    sql_query.format('id'), params={'where_id': office_id})
  
                # print('here show documents and their files')

            self.object_list = qs
            context = self.get_context_data()
            return self.render_to_response(context)

        return super(OfficeListView, self).get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        context['set_of_years'] = self.get_set_of_years()
        return super().get_context_data(**context)

    def get_queryset(self):

        sql_query = self.get_sql_query()

        qs =Office.objects.raw(sql_query)

        return qs
