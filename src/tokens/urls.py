from django.conf.urls import url
from .views import (
	UserTokenView,
	BuyTokenView,
	BuyTokenConfirmView,
    )

urlpatterns = [
    url(r'^(?P<username>[\w.@+-]+)/$', UserTokenView.as_view(), name='token'),
    url(r'^(?P<username>[\w.@+-]+)/buy/$', BuyTokenView.as_view(), name='buy'),
    url(r'^(?P<username>[\w.@+-]+)/buy/confirm$', BuyTokenConfirmView.as_view(), name='buy_confirm'),
    # url(r'^buy/$', BuyTokenView.as_view(), name='buy')
]
