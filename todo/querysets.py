from django.db.models import QuerySet

class TodoQuerySet(QuerySet):
    def get_older_todo(self):
        return self.order_by('date_created').first()

