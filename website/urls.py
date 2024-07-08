from django.urls import path, include


from .views import *
from .views import connect, connect, deconnect, create, signup
from django.contrib.auth import views as auth_views 
from .views import connect, connect, deconnect, create, signup
urlpatterns =[
  
  
    
     path('', connxeion, name='home'),
     path('Connected/', connect, name='Connected'),
     path('deconnect/', deconnect, name='deconnect'),
     path('create/', create, name='create'),
     path('created/', signup, name='created'),
     path('password_reset/',auth_views.PasswordResetView.as_view(template_name='dashboard/password_reset_form.html', email_template_name='dashboard/password_reset_email.html'),name='password_reset'),

     
     path('mail_envoye/', auth_views.PasswordResetDoneView.as_view( template_name='dashboard/password_reset_done.html'
    ), name='password_reset_done'),
     
   path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='dashboard/password_reset_confirm.html'), name='password_reset_confirm'),
     
     path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='dashboard/password_reset_complete.html'
    ), name='password_reset_complete'),

    path('changepass/', change_password, name='changepass'),
    path('pass_changer', password_success, name='pass_changer'),
     
      
    

     
     
     
     
     
     path('test-media/', test_media, name='test_media'),
     
     
      # Publisher URL's
     path('client/', client, name='client'),
     path('menu/', Menu, name='menu'),
     path('trans/', Transport, name='trans'),
     path('finance/', Finance, name='finance'),

     path('profile/<slug:slug>/', view_profile, name='profile'),
     path('edit/profil//<slug:slug>/', update_profile, name='edit_profile'),
     path('update-profile-picture/<slug:slug>/', update_profile_picture, name='update_profile_picture'),
     path('modifier', login_or_edit_profile, name='modifier'),
      path('building', PageBuilding, name='building'),
     path('fonctionnalite', login_or_functions, name='fonctionnalite'),
     path('checkpass', check_password_for_fonctionnalite, name='checkpass'),
     path('checkmenu', check_password_for_menu, name='checkmenu'),
     path('testify', check_pass, name='testify'),
     
     path('dowload/<slug:slug>/', download_vcard, name='dowload'),

     
     
     path('aabook_form/', aabook_form, name='aabook_form'),
     path('aabook/', aabook, name='aabook'),
     path('albook/', ABookListView.as_view(), name='albook'),
     path('aepro/<int:pk>', AeditView.as_view(), name='aepro'),
     path('ambook/', AManageBook.as_view(), name='ambook'),
     path('adbook/<int:pk>', ADeleteBook.as_view(), name='adbook'),
     path('aedoc/<int:pk>', AeditDocView.as_view(), name='aedoc'),

    #admin
    path('admin/', dashboard, name='admin'),
    #path('create_user_form/', views.create_user_form, name='create_user_form'),
    path('create_user/', CreateUserView.as_view(), name='create_user'),
    path('wluser/', ListUserView.as_view(), name='wluser'),
    path('aeuser/<int:pk>', AEditUser.as_view(), name='aeuser'),
     path('aduser/<int:pk>', ADeleteUser.as_view(), name='aduser'),
     path('contact/', contact, name='contact'),
     
     
      path('profile-views/', profile_views, name='profile_views')



]



