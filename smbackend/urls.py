from django.contrib import admin
from django.urls import include, re_path
from django.utils.translation import gettext_lazy as _
from munigeo.api import all_views as munigeo_views
from rest_framework import routers

from observations.api import views as observations_views
from observations.views import obtain_auth_token
from services import views
from services.api import all_views as services_views
from services.unit_redirect_viewset import UnitRedirectViewSet
from shortcutter import urls as shortcutter_urls

admin.site.site_header = _("Servicemap administration")
admin.site.index_title = _("Application management")

router = routers.DefaultRouter()

registered_api_views = set()

for view in services_views + munigeo_views + observations_views:
    kwargs = {}
    if view["name"] in registered_api_views:
        continue
    else:
        registered_api_views.add(view["name"])

    if "basename" in view:
        kwargs["basename"] = view["basename"]
    router.register(view["name"], view["class"], **kwargs)


urlpatterns = [
    # Examples:
    # url(r'^$', 'smbackend.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^', include(v1_api.urls)),
    # url(r'^admin/', include(admin.site.urls)),
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^open311/", views.post_service_request, name="services"),
    re_path(r"^v2/", include(router.urls)),
    re_path(r"^v2/api-token-auth/", obtain_auth_token, name="api-auth-token"),
    re_path(r"^v2/redirect/unit/", UnitRedirectViewSet.as_view({"get": "list"})),
    re_path(r"^v2/suggestion/", views.suggestion, name="suggestion"),
    re_path(r"", include(shortcutter_urls)),
]
