from django.db import models
from django.contrib.auth.models import User
from django.db.models import TextChoices

class TodoStatusChoice(TextChoices):
    ACTIVE = 'ACTIV', 'Активный'
    NOT_ACTIVE = 'NOT_ACTIVE', 'Не активный'

class Todolist(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    memo = models.TextField(blank=True,verbose_name='Текст дела')
    date_created = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False, verbose_name='Важность дела для вас')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, verbose_name='Статус', choices=TodoStatusChoice.choices, default=TodoStatusChoice.ACTIVE)

    def __str__(self):
        return self.title


class StatusChoice(TextChoices):
    NEW = 'NEW', 'Новый'
    IN_PROGRESS = 'IN_PROGRESS', 'В процессе'
    DONE = 'DONE', 'Выполнено'

class TaskTypeChoice(TextChoices):
    TASK = 'TASK', 'Задача'
    BUG = 'BUG', 'Ошибка'
    Enhancement = 'Enhancement', 'Улучшение'

class Tag(models.Model):
    name = models.CharField(max_length=31, verbose_name='Тег')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    def __str__(self):
        return self.name

class ArticleTag(models.Model):
    article = models.ForeignKey('todo.Comment', related_name='article_tags', on_delete=models.CASCADE, verbose_name='Комментарий')
    tag = models.ForeignKey('todo.Tag', related_name='tag_articles', on_delete=models.CASCADE, verbose_name='Тег')

    def __str__(self):
        return "{} | {}".format(self.article, self.tag)

class Comment(models.Model):
   status = models.CharField(max_length=20, verbose_name='Статус', choices=StatusChoice.choices,default=StatusChoice.NEW)
   task_type = models.CharField(max_length=20, verbose_name='Тип задачи', choices=TaskTypeChoice.choices,default=TaskTypeChoice.TASK)
   article = models.ForeignKey(to=Todolist, related_name='comments', on_delete=models.CASCADE, verbose_name='Дело')
   text = models.TextField(max_length=400, verbose_name='Комментарий')
   author = models.CharField(max_length=40, null=True, blank=True, default='Аноним', verbose_name='Автор')
   created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
   updated_at = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
   tags = models.ManyToManyField('todo.Tag', related_name='articles', through='todo.ArticleTag',
                                 through_fields=('article', 'tag'), blank=True)

   def __str__(self):
       return self.text[:20]



