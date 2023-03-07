from django.db import models
from django.contrib.auth.models import User
from django.db.models import TextChoices

class StatusChoice(TextChoices):
    NEW = 'NEW', 'Новый'
    IN_PROGRESS = 'IN_PROGRESS', 'В процессе'
    DONE = 'DONE', 'Выполнено'

class TaskTypeChoice(TextChoices):
    TASK = 'TASK', 'Задача'
    BUG = 'BUG', 'Ошибка'
    Enhancement = 'Enhancement', 'Улучшение'

class Ticket(models.Model):
    title = models.CharField(max_length=128)
    text = models.TextField()
    created = models.DateTimeField(auto_now=True)
    closed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, verbose_name='Статус', choices=StatusChoice.choices,
                              default=StatusChoice.NEW)
    task_type = models.CharField(max_length=20, verbose_name='Тип задачи', choices=TaskTypeChoice.choices,
                                 default=TaskTypeChoice.TASK)

    def __unicode__(self):
        return self.title

