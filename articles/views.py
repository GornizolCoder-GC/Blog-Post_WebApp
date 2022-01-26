from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from .models import Articles


# Create your views here.
class ArticleListView(ListView):
    model = Articles
    template_name = 'posts/article_list.html'

class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Articles
    template_name = 'posts/article_detail.html'

class ArticleEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Articles
    fields = ('title', 'summary','body', 'photo',)
    template_name = 'posts/article_edit.html'


    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    # foydalanuvchi admin ekanligini tekshirish
    # def test_func(self):
    #     return self.request.user.is_superuser

class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Articles
    template_name = 'posts/article_delete.html'
    success_url = reverse_lazy('article_list')

    # def test_func(self):
    #     obj = self.get_object()
    #     return obj.author == self.request.user

    # foydalanuvchi admin ekanligini tekshirish
    def test_func(self):
        return self.request.user.is_superuser

class ArticleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Articles
    template_name = 'posts/article_new.html'
    fields = ('title', 'summary', 'body', 'photo',)
    # success_url = reverse_lazy('article_list')

    # muallif(Articles modelidagi author)ni foydalanuvchi nomi bilan yaratish
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # foydalanuvchi admin ekanligini tekshirish
    def test_func(self):
        return self.request.user.is_superuser