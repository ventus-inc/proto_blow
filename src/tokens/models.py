from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


# Create your models here.

class TokenBoard(models.Model):
    """売り買い板"""
    master = models.ForeignKey(settings.AUTH_USER_MODEL, default=None)
    price_now = models.FloatField(null=True, blank=True, default=None)
    timestamp = models.DateTimeField(auto_now_add=True)


class Token(models.Model):
    """持っているtoken"""
    token_board = models.ForeignKey(TokenBoard, null=True, blank=True)  # 暫定的にblank=True
    publisher = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, related_name='publisher')
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, related_name='owner')
    bought_price = models.FloatField(
        null=True,
        blank=True,
        default=None,
        validators=[MinValueValidator(0.0)])
    latest_price = models.FloatField(
        null=True,
        blank=True,
        default=None,
        validators=[MinValueValidator(0.0)])
    lot = models.PositiveIntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class BuyOrderManager(models.Manager):
    def get_summed_lot(self, master):
        buys = self.get_queryset().filter(master=master).order_by('-price')
        total_buys = []
        previous_price = None
        obj = BuyOrder()
        for i in buys:
            if not previous_price:
                obj = BuyOrder(
                    master=i.master,
                    buyer=i.buyer,
                    price=i.price,
                    lot=i.lot,
                )
            else:
                if not previous_price == i.price:
                    total_buys.append(obj)
                    obj = BuyOrder(
                        master=i.master,
                        buyer=i.buyer,
                        price=i.price,
                        lot=i.lot,
                    )
                else:
                    obj.lot += i.lot
            previous_price = i.price
        total_buys.append(obj)
        return total_buys

    def get_summed_list(self, master):
        buys = self.get_queryset().filter(master=master).order_by('-price')
        total_price = []
        total_lot = []
        previous_price = None
        for i in buys:
            if not previous_price:
                price = i.price
                lot = i.lot
            else:
                if not previous_price == i.price:
                    total_price.append(price)
                    total_lot.append(lot)
                    price = i.price
                    lot = i.lot
                else:
                    lot += i.lot
                    obj.lot += i.lot
            previous_price = i.price
        total_price.append(price)
        total_lot.append(lot)
        print("totalprices")
        print(total_price)
        print(total_lot)
        return [total_price,total_lot]


class BuyOrder(models.Model):
    """注文
	"""
    master = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='origin_buy')
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='buyer')
    price = models.FloatField(
        null=True,
        blank=True,
        default=None,
        validators=[MinValueValidator(0.0)])
    token_board = models.ForeignKey(TokenBoard, blank=True, null=True)
    lot = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = BuyOrderManager()

    def __str__(self):
        message = 'order_by:' + str(self.buyer) + '\n at:' + str(self.timestamp)
        return str(message)

    class Meta:
        ordering = ('price',)


class SellOrderManager(models.Manager):
    def get_summed_lot(self, master):
        sells = self.get_queryset().filter(master=master).order_by('-price')
        total_sells = []
        previous_price = None
        obj = SellOrder()
        for i in sells:
            if not previous_price:
                obj = SellOrder(
                    master=i.master,
                    seller=i.seller,
                    price=i.price,
                    lot=i.lot,
                )
            else:
                if not previous_price == i.price:
                    total_sells.append(obj)
                    obj = SellOrder(
                        master=i.master,
                        seller=i.seller,
                        price=i.price,
                        lot=i.lot,
                    )
                else:
                    obj.lot += i.lot
            previous_price = i.price
        total_sells.append(obj)
        return total_sells

    def get_summed_list(self, master):
        sells = self.get_queryset().filter(master=master).order_by('-price')
        total_price = []
        total_lot = []
        previous_price = None
        for i in sells:
            if not previous_price:
                price = i.price
                lot = i.lot
            else:
                if not previous_price == i.price:
                    total_price.append(price)
                    total_lot.append(lot)
                    price = i.price
                    lot = i.lot
                else:
                    lot += i.lot
                    obj.lot += i.lot
            previous_price = i.price
        total_price.append(price)
        total_lot.append(lot)
        print("totalprices")
        print(total_price)
        print(total_lot)
        return [total_price,total_lot]


class SellOrder(models.Model):
    """注文
    """
    master = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='origin_sell')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='seller')
    price = models.FloatField(
        null=True,
        blank=True,
        default=None,
        validators=[MinValueValidator(0.0)])
    token_board = models.ForeignKey(TokenBoard, blank=True, null=True)
    lot = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = SellOrderManager()

    def __str__(self):
        message = 'order_by:' + str(self.master) + '\n at:' + str(self.timestamp)
        return str(message)

    class Meta:
        ordering = ('price',)
