superuser: admin   password: root

# Приложение issue_tracker для работы с Тикетами

На главной странице есть ссылка на просмотр дел через API 
http://127.0.0.1:8000/todoapi/

Для просмотра определенного дела доабвляется id
http://127.0.0.1:8000/todoapi/номер дела

Методом PUT криво настроен функционал обновления дела (правда потом остается на этой же странице)

Методом POST создаются новые дела

Методом DELETE удаляется выбранное дело, остается на той же странице и при попытке нового перехода на нее выдает не найдено
