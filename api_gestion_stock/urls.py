from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls import handler404

from api_gestion_stock.router import OptionalSlashRouter

from stock.views import SupplierViewSet, ArticleFamilyViewSet, ArticleViewSet, StockViewSet, EntryVoucherViewSet, ExitRequestViewSet, ExitVoucherViewSet, ReturnRequestViewSet, ReturnVoucherViewSet


router = OptionalSlashRouter()
router.register(r'suppliers', SupplierViewSet, basename='suppliers')
router.register(r'fam_articles', ArticleFamilyViewSet, basename='fam-articles')
router.register(r'articles', ArticleViewSet, basename='articles')
router.register(r'stocks', StockViewSet, basename='stocks')
router.register(r'entry_vouchers', EntryVoucherViewSet, basename='entry-vouchers')
router.register(r'exit_requests', ExitRequestViewSet, basename='exit-requests')
router.register(r'exit_vouchers', ExitVoucherViewSet, basename='exit-vouchers')
router.register(r'return_requests', ReturnRequestViewSet, basename='return-request')
router.register(r'return_vouchers', ReturnVoucherViewSet, basename='return-vouchers')

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include(router.urls)),

    # path('suppliers/', SupplierViewSetAPIView.as_view(), name="supplier_api_views")
]


# def custom_404(request, exception):
#     return TemplateView.as_view(template_name='index.html')(request)


# handler404 = custom_404
