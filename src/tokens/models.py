from django.db import models
from django.conf import settings

# Create your models here.

class TokenBoard(models.Model):
	"""売り買い板
	"""
	master 		= models.ForeignKey(settings.AUTH_USER_MODEL, default=None)
	price_now 	= models.FloatField(null=True, blank=True, default=None)
	timestamp   = models.DateTimeField(auto_now_add=True)

class Token(models.Model):
	"""持っているtoken
	"""
	token_board 	= models.ForeignKey(TokenBoard)
	owner			= models.ForeignKey(settings.AUTH_USER_MODEL, default=None)
	latest_price 	= models.FloatField(null=True, blank=True, default=None)
	updated			= models.DateTimeField(auto_now=True)
	timestamp		= models.DateTimeField(auto_now_add=True)

class BuyOrderManager(models.Manager):
	def get_summed_lot(self, master):
		buys = self.get_queryset().filter(master=master).order_by('-price')
		total_buys = []
		previous_price = None
		obj = BuyOrder()
		for i in buys:
			if not previous_price:
				obj = BuyOrder(
					master = i.master,
					buyer = i.buyer,
					price = i.price,
					lot = i.lot,
					)
			else:
				if not previous_price == i.price:
					total_buys.append(obj)
					obj = BuyOrder(
						master = i.master,
						buyer = i.buyer,
						price = i.price,
						lot = i.lot,
						)
				else:
					obj.lot += i.lot
			previous_price = i.price
		total_buys.append(obj)
		return total_buys

class BuyOrder(models.Model):
	"""注文
	"""
	master 		= models.ForeignKey(settings.AUTH_USER_MODEL, related_name='master')
	buyer 		= models.ForeignKey(settings.AUTH_USER_MODEL, related_name='buyer')
	price 		= models.FloatField(null=True, blank=True, default=None)
	token_board = models.ForeignKey(TokenBoard, blank=True, null=True)
	lot			= models.IntegerField(default=0)
	timestamp   = models.DateTimeField(auto_now_add=True)

	objects = BuyOrderManager()

	def __str__(self):
		message = 'order_by:'+ str(self.master) + '\n at:'+ str(self.timestamp)
		return str(message)

	class Meta:
		ordering = ('price',)
