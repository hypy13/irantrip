from categories.models import Category
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import FormView, ListView, DetailView

from apps.comment.models import Comment
from apps.tour.models import Tour


class CategoryTourList(ListView):
    template_name = 'front/category-list.html'
    context_object_name = 'tours'

    paginate_by = 1

    def get_queryset(self):
        cats = Category.objects.filter(slug=self.kwargs['slug']).first().get_ancestors(include_self=True)
        return Tour.objects.filter(categories__in=cats).all()


class TourComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = 'name', 'message', 'parent',
        widgets = {'parent': forms.HiddenInput()}


class TourList(ListView):
    template_name = 'front/pages/tours.html'
    paginate_by = 8


class TourDetail(DetailView, FormView):
    template_name = 'front/pages/single-tour.html'
    form_class = TourComment
    model = Tour
    slug_field = 'slug'

    def form_valid(self, form):
        if form.is_valid():
            tour = Tour.objects.get(slug=self.kwargs['slug'])
            obj = form.save(commit=False)
            obj.user = self.request.user
            obj.commentable_id = tour.pk
            obj.content_type = ContentType.objects.get_for_model(tour)
            messages.success(self.request, 'Your comment successfully submitted!')
            obj.save()

        return HttpResponseRedirect(self.request.build_absolute_uri())

    def get_context_data(self, **kwargs):
        content_type = ContentType.objects.get_for_model(Tour)
        kwargs['comments'] = Comment.objects.filter(
            content_type=content_type,
            status=Comment.CommentStatus.approved).all()
        kwargs['comment_form'] = TourComment()
        return super(TourDetail, self).get_context_data(**kwargs)

    def get_queryset(self):
        return Tour.objects.prefetch_related("photos", "days").filter(slug=self.kwargs['slug'])
