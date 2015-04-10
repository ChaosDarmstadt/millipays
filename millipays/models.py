from django.db import models

#  1 mate 4029764001807
#  2 cola 4029764001883
#  3 icet 4029764001814
# matemagier 4029764001807

class Product(models.Model):
    barcode = models.CharField(max_length=13)
    price = models.FloatField()
    stock= models.IntegerField()
    name = models.CharField(max_length=20)
    member_discount = models.FloatField(default=0.5)

    def __str__(self):
        return self.name

# Die Barkasse ist auch ein Member
class Member(models.Model):
    nick = models.CharField(max_length=20)
    number = models.CharField(max_length=13)
    balance = models.FloatField()
    addPrepaid = models.FloatField(default=0)
    consume = models.IntegerField(default=0)

    def __str__(self):
        return self.nick

# Alle Käufe im CashLog müssen schlüssig mit dem aktuellen Stand an Products.stock und Member.balance sein
# Member x kaufte Produkt y
class CashLog(models.Model):
    member = models.ForeignKey(Member)
    product = models.ForeignKey(Product)
    count = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    purchase_date = models.DateTimeField('date purchased')

