from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, FormView
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


class TicketUpdateView(FormView):
    template_name = 'issue_tracker/update_ticket.html'
    form_class = Ticket

    def dispatch(self, request, *args, **kwargs):
        self.title = self.get_object()
        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.title
        return kwargs


    def form_valid(self, form):
        self.title = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('article_view', kwargs={'pk': self.title.pk})

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Ticket, pk=pk)