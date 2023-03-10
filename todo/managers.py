from django.db.models import Manager

class TodoManager(Manager):

    def get_or_none(self, pk=None):
        try:
            return self.get_queryset().get(pk=pk)
        except self.model.DoesNotExist:
            return None

    def get_completed(self):
        return self.get_queryset().filter(date_completed=True)

    def get_deleted(self):
        return self.get_queryset().filter(date_deleted=True)

    def get_all(self):
        return self.get_queryset().filter(date_completed=False)


