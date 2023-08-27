
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView
from .models import Article, Comment, Category, Tag
from .forms import CommentForm, SubscribeForm, FeedbackForm
from .search import search
from manager.tasks import add_email, add_feedback


def feedback_form(request):
    """
    Получает заполненную форму обратной связи и передаёт данные из неё в задачу,
    отвечающую за добавление их в базу данных.
    """
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            message = form.cleaned_data.get('message')
            add_feedback.delay(name, email, message)
    return render(request, 'blog/feedback_success.html')


def subscribe_form(request):
    """
    Получает заполненную форму подписки на блог и передаёт данные из неё в задачу,
    отвечающую за добавление email в базу данных.
    """
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            add_email.delay(email)
    return render(request, 'blog/subscribe_success.html')


class ArticleView(ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'articles'
    paginate_by = 5
    paginate_orphans = 5
    
    def get_ordering(self):
        sort = self.kwargs.get('sort')
        if sort == 'views':
            return ('-views', '-created_date')
        return ('-created_date')
    

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/article_detail.html'
    context_object_name = 'article'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['comments'] = Comment.objects.filter(article=self.get_object())
        context['comments_number'] = context['comments'].count()
        context['form'] = CommentForm()
        return context

    def post(self, request , *args , **kwargs):
        if self.request.method == 'POST':
            comment_form = CommentForm(self.request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                if self.request.user.is_authenticated:
                    new_comment.author = self.request.user
                    new_comment.email = self.request.user.email
                else:
                    guest = comment_form.cleaned_data.get('guest')
                    if guest:
                        new_comment.guest = comment_form.cleaned_data.get('guest')
                    else:
                        new_comment.guest = 'Безымянный'
                    new_comment.email = comment_form.cleaned_data.get('email')
                new_comment.article = self.get_object()
                new_comment.save()
            return redirect(self.request.path_info)
        
    def dispatch(self, request, slug, *args, **kwargs):
        obj = self.get_object()
        obj.views += 1
        obj.save()
        return super().dispatch(request, *args, **kwargs)
        
        
class CategoryView(ListView):
    model = Article
    template_name = 'blog/category.html'
    context_object_name = 'articles'
    paginate_by = 2
    paginate_orphans = 2

    def get_ordering(self):
        sort = self.kwargs.get('sort')
        if sort == 'views':
            return ('-views', '-created_date')
        return ('-created_date')

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset()
        category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        return queryset.filter(category=category)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        context_data['category'] = category
        return context_data
    
    
class TagView(ListView):
    model = Article
    template_name = 'blog/tag.html'
    context_object_name = 'articles'
    paginate_by = 2
    paginate_orphans = 2
    
    def get_ordering(self):
        sort = self.kwargs.get('sort')
        if sort == 'views':
            return ('-views', '-created_date')
        return ('-created_date')

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset()
        tag = get_object_or_404(Tag, slug=self.kwargs.get('slug'))
        return queryset.filter(tags=tag)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        tag = get_object_or_404(Tag, slug=self.kwargs.get('slug'))
        context_data['tag'] = tag
        return context_data


class SearchView(ListView):
    model = Article
    template_name = 'blog/search.html'
    paginate_by = 10
    paginate_orphans = 5
    context_object_name = 'articles'
    
    def get_queryset(self):
        query = self.request.GET.get('query')
        if query is not None:
            return search(query)
        return
   