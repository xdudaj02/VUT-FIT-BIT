from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

# list of working urls
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('register/', views.register, name='register'),
    path('genres/', views.genre_list, name='genre_list'),
    path('genres/add/', views.genre_add, name='genre_add'),
    path('genres/<slug:genre_id>', views.genre_detail, name='genre_detail'),
    path('authors/', views.author_list, name='author_list'),
    path('authors/add', views.author_add, name='author_add'),
    path('authors/edit/<slug:author_id>', views.author_edit, name='author_edit'),
    path('authors/<slug:author_id>', views.author_detail, name='author_detail'),
    path('titles/', views.title_list, name='title_list'),
    path('titles/add', views.title_add, name='title_add'),
    path('titles/edit/<slug:title_isbn>', views.title_edit, name='title_edit'),
    path('titles/<slug:title_isbn>', views.title_detail, name='title_detail'),
    path('libraries/', views.library_list, name='library_list'),
    path('libraries/add', views.library_add, name='library_add'),
    path('libraries/edit/<slug:library_id>', views.library_edit, name='library_edit'),
    path('libraries/<slug:library_id>', views.library_detail, name='library_detail'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/add', views.order_add, name='order_add'),
    path('orders/add/<slug:order_id>', views.order_add_more, name='order_add_more'),
    path('orders/<slug:order_id>', views.order_detail, name='order_detail'),
    path('borrowings/', views.borrowing_list, name='borrowing_list'),
    path('borrowings/add', views.borrowing_add, name='borrowing_add'),
    path('borrowings/add/<slug:borrowing_id>', views.borrowing_add_more, name='borrowing_add_more'),
    path('borrowings/<slug:borrowing_id>', views.borrowing_detail, name='borrowing_detail'),
    path('reservations/', views.reservation_list, name='reservation_list'),
    path('reservations/add/', views.reservation_add, name='reservation_add'),
    path('reservations/<slug:reservation_id>', views.reservation_detail, name='reservation_detail'),
    path('votes/', views.vote_list, name='vote_list'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.employee_add, name='employee_add'),
    path('employees/edit/<slug:employee_id>', views.employee_edit, name='employee_edit'),
    path('employees/<slug:employee_id>', views.employee_detail, name='employee_detail'),
    path('distributors/', views.distributor_list, name='distributor_list'),
    path('distributors/add/', views.distributor_add, name='distributor_add'),
    path('distributors/edit/<slug:distributor_id>', views.distributor_edit, name='distributor_edit'),
    path('distributors/<slug:distributor_id>', views.distributor_detail, name='distributor_detail'),
    path('users/', views.user_list, name='user_list'),
    path('users/edit/<slug:user_id>', views.user_edit, name='user_edit'),
    path('users/<slug:user_id>', views.user_detail, name='user_detail')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# todo: decide on actions after deletion (employee - what to do with his orders, borrowings - not delete?)
#       fix the styles go missing error, probably caused by the 404 page ?
#       permissions - groups?
