"""
URL configuration for todo_everything project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from accounts import api as accounts_api
from django.contrib import admin
from django.urls import include, path
from organizations import api as organizations_api
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
)
from todos import api as todos_api

router = routers.DefaultRouter()
router.register(r"account", accounts_api.AccountViewSet)
router.register(r"organization", organizations_api.OrganizationViewSet)
router.register(r"organization-invite", organizations_api.OrganizationInviteViewSet)
router.register(r"profile", accounts_api.AccountProfileViewSet)
router.register(r"todo", todos_api.TodoViewSet)

urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/blacklist/", TokenBlacklistView.as_view(), name="token_blacklist"),
    path(
        "api/register/",
        accounts_api.AccountRegisterView.as_view(),
        name="account_register",
    ),
    path("api/", include(router.urls)),
    path("api/dashboard/", accounts_api.AccountDashboardView.as_view()),
    path("api/todo-overview/", todos_api.TodoOverviewView.as_view()),
    path("admin/", admin.site.urls),
]
