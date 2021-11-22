from django.shortcuts import render, get_object_or_404
from .models import Post
from .forms import CommentForm
from django.views.generic import ListView
from taggit.models import Tag
from django.db.models import Count
# from django.core.mail import send_mail
# from .forms import EmailPostForm


class PostListView(ListView):
    queryset = Post.objects.filter(status='published').all()
    tag = None
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

    def get_queryset(self):  # переопределяем получение объектов
        tag_slug = self.kwargs.get('tag_slug', None)  # получаем аргумент из ссылки
        if tag_slug is not None:  # если аргумент существует
            tag = get_object_or_404(Tag, slug=tag_slug)
            self.tag = tag
            return Post.objects.filter(status='published', tags__in=[tag])  # фильтруем по нему посты
        return Post.objects.filter(status='published').all()

    def get_context_data(self, **kwargs):
        context = {
            'tag': self.tag
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post, slug=slug, status='published', publish__year=year, publish__month=month,
                             publish__day=day)
    comments = post.comments.filter(active=True)
    new_comment = False
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(status='published', tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
            new_comment = True
    else:
        comment_form = CommentForm()
    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'comment_form': comment_form,
                   'similar_posts': similar_posts})


# def post_share(request, post_id):
#     # Retrieve post by id
#     post = get_object_or_404(Post, id=post_id, status='published')
#     sent = False
#     if request.method == 'POST':
#         # Form was submitted
#         form = EmailPostForm(request.POST)
#         if form.is_valid():
#             # Form fields passed validation
#             cd = form.cleaned_data
#             post_url = request.build_absolute_uri(post.get_absolute_url())
#             subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
#             message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
#             send_mail(subject, message, 'admin@myblog.com', [cd['to']])
#             sent = True
#     else:
#         form = EmailPostForm()
#     return render(request, 'blog/post/share.html', {'post': post,
#                                                     'form': form,
#                                                     'sent': sent})