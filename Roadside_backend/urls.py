
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/v1/client/auth/', include("authentication.urls.client_urls")),
    path('api/v1/admin/auth/', include("authentication.urls.admin_urls")),
    
    path('api/v1/admin/food-items', include("food_items.urls.admin_urls")),
    path('api/v1/client/food-items', include("food_items.urls.client_urls")),
    
    path('api/v1/client/users/', include("users.urls.client_urls")),
    path('api/v1/admin/users/', include("users.urls.admin_urls")),
    
    path('api/v1/admin/vendor/', include("vendor.urls.admin_urls")),
    path('api/v1/client/vendor/', include("vendor.urls.client_urls")),
    
]
