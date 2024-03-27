from  django.urls import path
from . import views
urlpatterns = [
    path('register/',views.register,name='register'),
    path('signin/',views.signin,name='signin'),
    path('log_out/',views.log_out,name='log_out'),
    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(),name='activate'),
    path('profile/',views.profile,name='profile'),
    path('profileUpdate/', views.profileUpdate, name='profileUpdate'),
    path('forgotPassword/',views.forgotPassword,name='forgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>',views.resetpassword_validate,name='resetpassword_validate'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
    path('changePassword/', views.changePassword, name='changePassword'),
]