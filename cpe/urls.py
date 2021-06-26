"""cpe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from blogs import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from blogs.views import VerificationView,LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.hello,name="index"),
    #path('page1',views.page1,name = "page1"),
    path('page1',views.testlogin,name = "page1"),
    path('page2',views.page2),
    path('page3',views.page3),
    path('adduseradmin',views.adduser_admin),
    path('resualt',views.resualt),
    path('appsend',views.appsend,name="appsend"),
    #path('appsend',views.checklicense,name="appsend"),
    path('account/logout',views.signOutView,name="signout"),
    #path('license',views.checklicense,name="license"),
    path('license',views.license,name="license"),
    path('final/<int:myid>/<int:idsendto>',views.final,name="final"),
    #path('testlogin',views.testlogin,name="testlogin"),
    #path('confirmlic',views.checklicense,name = "confirmlic"),
    path('confirmlic',views.confirmlicn,name = "confirmlic"),

    path('confirmsend/<int:oder_id>',views.confirmsend,name="confirmsend"),

    path('error',views.error,name="error"),
    path('findstd',views.findstd,name="findstd"),
    path('setpassword',views.setpassword),
    path('admincheckinput',views.admincheckinput),
    path('admincheck',views.admincheck),
    path('checklicense',views.checklicense),
    path('adminchecklicense/<int:userid>',views.adminchecklicense,name="adminchecklicense"),
    path('removeodercheck/<str:oder_id>',views.removeodercheck,name="removeodercheck"),
    path('removeoder/<int:oder_id>',views.removeoder,name="removeoder"),
    #path('order/<int:oder_id',views.viewOrder,name="oder")
    path('setting',views.setting,name="setting"),
    
    
   # path('reset_password/',auth_views.PasswordResetView.as_view(template_name="password_reset.html")
    #     ,name="reset_password"),
    #path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),
    #path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(), name ="password_reset_confirm"),
    #path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),    
    
    
    path('activate/<uidb64>/<token>',VerificationView.as_view(),name="activate"),
    
    path('forget/<uidb64>/<token>',views.forget,name="forget"),
    
    
    path('setup',views.setup,name="setup"),
    
    path('page4',views.page4,name="page4"),

    
    
    #like system
    path('like_s/<int:oder_id>',views.like_s,name="likes"),
    path('like_d/<int:oder_id>',views.like_d,name="liked"),
    
    
    #test
    
    
    
]

urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)