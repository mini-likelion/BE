"""
URL configuration for mini project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from mainpage.views import *
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from movies.views import movie_detail

schema_view = get_schema_view(
    openapi.Info(
        title="MiniHack API",
        default_version='v1',
        description="영화 API 문서입니다",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


app_names = [
    'accounts',
    'detailpage',
    'mainpage',
    'movies',
    'mini',
]

urlpatterns = [
    path('', include('mainpage.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),#sujin
    path('dj/', include('dj_rest_auth.urls')), #sujin
    path('dj/registration/', include('dj_rest_auth.registration.urls')),
    path('mainpage/', include('mainpage.urls')),
    path('movies/', movie_list, name='movie-list'),
    path('movies/<int:movie_id>/', movie_detail, name='movie-detail'),
    path('init_db/', init_db, name='init-db'),
    path('detailpage/',include('detailpage.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
]

for app in app_names:
    schema_name = f'schema-{app}'
    docs_name   = f'swagger-ui-{app}'

    # OpenAPI 스키마 (JSON/YAML)
    urlpatterns.append(
        path(
            f'api/schema/{app}/',
            SpectacularAPIView.as_view(
                patterns=[
                    # 각 앱의 urls.py 에 정의된 엔드포인트만 문서화
                    path(f'api/{app}/', include((f'{app}.urls', app), namespace=app))
                ]
            ),
            name=schema_name
        )
    )

    # Swagger UI
    urlpatterns.append(
        path(
            f'api/docs/{app}/',
            SpectacularSwaggerView.as_view(
                url_name=schema_name,
                title=f'{app.capitalize()} API 문서'
            ),
            name=docs_name
        )
    )
