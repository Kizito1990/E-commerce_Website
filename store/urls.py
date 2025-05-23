from django.urls import path
from .import views
from .views import contact_view

urlpatterns = [
    path("", views.index, name = "index"),
    path("about/", views.about, name = "about"),
    path("picture/", views.picture, name = "picture"),
    path("grades/", views.grades, name = "grades"),
    path("shop/", views.shop, name = "shop"),
    path("video/", views.video, name = "video"),
    path("service/", views.services, name = "service"),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('update_password/', views.update_password, name='update_password'),
    path('update_user/', views.update_user, name='update_user'),
    path('update_info/', views.update_info, name='update_info'),
    path('product/<int:pk>', views.product, name='product'),
    path('category/<str:foo>', views.category, name='category'),
    path('category_summary/', views.category_summary, name='category_summary'),
    path('raw/', views.raw, name='raw'),
    path('admin_contact/', views.site_contact, name='admin_contact'),
    path('contact/', contact_view, name='contact'),
    path('export/', views.export, name='export'),
    path('sales/', views.sales, name='sales'),
    path('processing/', views.processing, name='processing'),
    path('processed/', views.processed, name='processed'),
    path('finished/', views.finish, name='finished'),
    path('groundnut/', views.groundnut, name='groundnut'),
    path('kuli/', views.kuli, name='kuli'),
    path('plantain/', views.plantain, name='plantain'),
    path('honey/', views.honey, name='honey'),
]