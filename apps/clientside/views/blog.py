from django import forms
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.views.generic import FormView, ListView, DetailView

from apps.comment.models import Comment
from apps.post.models import Post


class BlogComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = 'name', 'message', 'parent',
        widgets = {'parent': forms.HiddenInput()}


class BlogList(ListView):
    template_name = 'front/blog-list.html'
    paginate_by = 6
    context_object_name = 'blogs'

    def get_queryset(self):
        return Post.objects.all()


class BlogDetail(DetailView, FormView):
    template_name = 'front/single-blog.html'

    context_object_name = 'blog'

    def get_queryset(self):
        return Post.objects.filter(slug=self.kwargs['slug'])

    form_class = BlogComment

    def form_valid(self, form):
        print(form, '----------')
        if form.is_valid():
            blog = Post.objects.get(slug=self.kwargs['slug'])
            obj = form.save(commit=False)

            if self.request.user.is_authenticated:
                obj.user = self.request.user

            obj.commentable_id = blog.pk
            obj.content_type = ContentType.objects.get_for_model(blog)
            obj.save()

        return HttpResponseRedirect(self.request.build_absolute_uri())

    def get_context_data(self, **kwargs):
        kwargs['comments'] = Comment.objects.all()
        return super(BlogDetail, self).get_context_data(**kwargs)
