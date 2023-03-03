from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic import DetailView, CreateView
from .models import Ticket


class CommentListView(ListView):
    model = Ticket
    template_name = 'issue_tracker/list.html'


class CommentDetailView(DetailView):
        model = Ticket
        template_name = 'issue_tracker/detail_view.html'


class CommentCreateView(CreateView):
    model = Ticket
    template_name = 'issue_tracker/add_ticket.html'
    fields = ['title', 'text', 'status', 'task_type']
    success_url = reverse_lazy('list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CommentCreateView, self).form_valid(form)