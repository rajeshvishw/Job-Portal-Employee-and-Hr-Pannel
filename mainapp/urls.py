from django.urls import path
from mainapp import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("",views.signupView,name="signupview"),
    path("login/",views.loginView,name="login"),
    path("otp/",views.otpveryfyView,name="otp"),
    path("jobprofile/",views.jobprofileView,name="jobprofile"),
    path("userprofile/",views.userprofileView,name="userprofile"),
    path("companyprofile/",views.companyprofileView,name="companyprofile"),
    path("companyupdatep/",views.companyupdatepView, name=""),
    path("jobpost/",views.jobpostView, name="jobpost"),
    path("postedjobsee/",views.postedjobseeView, name="postedjobsee"),
    path("logout/",views.logoutView,name="logout"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
