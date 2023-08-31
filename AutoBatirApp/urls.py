from django.urls import path
from .import  views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    
    # path('', views.index, name='index'),
    path('', views.landingpage, name ='landingpage'),
    # path('homepage/', views.homepage, name ='homepage'),
    # path('client_registration/', views.client_registration.as_view(), name='client_registration'),
    # path('login/',views.login_request, name='login'),
    path('footer/', views.footer, name ='footer'),
    path('about/', views.about, name ='about'),
    path('navbar/', views.navbar, name ='navbar'),
    path('approve_permit/<str:UUID>', views.approve_permit, name='approve_permit' ),
    path('decline_permit/<str:UUID>', views.decline_permit, name='decline_permit' ),

    path('signin/', views.signin, name='signin' ),
    path('logout/', views.logout_view, name='logout' ),
    # The new lines
    path('homepage/', views.homepage, name='homepage' ),
    path('archivedpermit/', views.archivedpermit, name='archivedpermit' ),
    path('dashboard/', views.eng_dashboard, name='dashboard' ),
    path('signup/', views.signup.as_view(), name='signup'),
    path('request_permitForm/', views.request_permit, name='request_permitForm' ),

    path('report/', views.permiting, name='report' ),
    path('pdf-report/', views.pdf_report_create, name='pdf-report' ),
    path('permit_csv_report/', views.permit_list_csv, name='permit_csv_report' ),
    path('archive_csv_report/', views.archive_list_csv, name='archive_csv_report' ),

    # Comment
    path('save-comment/<uuid:permit_id>/', views.save_comment, name='save_comment'),

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)