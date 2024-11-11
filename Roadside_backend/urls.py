from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/v1/client/auth/', include("authentication.urls.client_urls")),
    # path('api/v1/admin/auth/', include("authentication.urls.admin_urls")),
    
    path('api/v1/admin/food-items/', include("food_items.urls.admin_urls")),
    path('api/v1/client/food-items/', include("food_items.urls.client_urls")),
    
    path('api/v1/client/users/', include("users.urls.client_urls")),
    path('api/v1/admin/users/', include("users.urls.admin_urls")),
    
    path('api/v1/admin/vendor/', include("vendor.urls.admin_urls")),
    path('api/v1/client/vendor/', include("vendor.urls.client_urls")),
    
    # path('api/v1/admin/notifications/', include("notifications.urls.admin_urls")),
    # path('api/v1/client/notifications/', include("notifications.urls.client_urls")),
    
    path('api/v1/admin/support/', include("support.urls.admin_urls")),
    path('api/v1/client/support/', include("support.urls.client_urls")),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



