from django.urls import path

from . import views

# urlpatterns = [
#     path('', views.student_id_view, name='home'), 
#    # path('student_id.html', views.student_id_view, name='student_id'),
#     path('industrial_experience.html', views.industrial_experience_view, name='industrial_experience'),
#      path('company-details/', views.company_details_view, name='company_details'),
#     path('preference.html', views.preference_view, name='preference'),
#     path('success_page.html',views.successpage,name='successpage'),
#     # path('',views.home , name = 'home'),
    
#     # path('fillingpage.html',views.fillingpage, name = 'fillingpage')
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_id_view, name='home'), 
    path('industrial_experience.html', views.industrial_experience_view, name='industrial_experience'),
    path('company-details/', views.company_details_view, name='company_details'),
    path('preference.html', views.preference_view, name='preference'),  # For new preference entries
    path('preference/edit/', views.edit_preference_view, name='edit_preference'),  # For editing preferences
    path('success_page.html', views.successpage, name='successpage'),
]
