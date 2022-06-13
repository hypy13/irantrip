from django.shortcuts import render
from django.urls import path


# from .views.blog import BlogList, BlogDetail
# from .views.contactus import ContactUsView
# from .views.course import CourseListView, CourseDetailView, CoursePaymentView
# from .views.faq import FaqView
# from .views.gallery import GalleryListView, GalleryDetailView

def tour(request):
    return render(request, 'single-tour.html')


urlpatterns = [
    path('', tour)
    # path('', HomePage.as_view(), name='home'),
    # path('tours/', TourList.as_view(), name='tour-list'),
    # path('tours/<str:slug>/', TourDetail.as_view(), name='tour-detail'),

    # path('categories/<str:slug>/', CategoryTourList.as_view(), name='category-detail'),
    #
    # path('blogs/', BlogList.as_view(), name='blog-list'),
    # path('blogs/<str:slug>/', BlogDetail.as_view(), name='blog-detail'),

    # path('iran-visa/', IranVisa.as_view(), name='iran-visa'),
    # path('services/', Services.as_view(), name='services'),
    # path('about/', About.as_view(), name='about'),
    #
    # path('faq/', FaqView.as_view(), name='faq'),
    #
    # path('galleries/', GalleryListView.as_view(), name='galleries'),
    # path('gallery/single/', GalleryDetailView.as_view(), name='single-gallery'),

]
