from django.views.generic import TemplateView


class GalleryListView(TemplateView):
    template_name = 'front/pages/gallery.html'


class GalleryDetailView(TemplateView):
    template_name = 'front/pages/single-gallery.html'
