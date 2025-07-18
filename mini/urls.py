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
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

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
    path('movies/',include('movies.urls')),
    path('detailpage/',include('detailpage.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
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
