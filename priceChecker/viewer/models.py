from django.db import models
from django.utils import timezone
from model_utils import Choices


class Store(models.Model):
    store_id = models.AutoField(primary_key=True)
    name = models.TextField()
    currency = models.TextField()
    url = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'store'


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.TextField()
    url = models.TextField()
    ACTIVITIES = Choices(
        ('0', 'inactive', 'Inactive'),
        ('1', 'active', 'Active'),
    )
    active = models.CharField(max_length=1, choices=ACTIVITIES,
                              default=ACTIVITIES.active)
    store = models.ForeignKey(Store, db_column='store_id',
                              on_delete=models.PROTECT)
    sheet = models.TextField(blank=True, null=True)

    def __str__(self):
        return '%s. %s' % (self.product_id, self.name)

    class Meta:
        managed = True
        db_table = 'product'


class Session(models.Model):
    session_id = models.AutoField(primary_key=True)
    date = models.DateTimeField()

    def __str__(self):
        return '%s. %s' % (self.session_id, self.date)

    class Meta:
        managed = True
        db_table = 'session'


class Price(models.Model):
    product = models.ForeignKey(Product, db_column='product_id',
                                on_delete=models.PROTECT)
    session = models.ForeignKey(Session, db_column='session_id',
                                on_delete=models.PROTECT)
    amount = models.FloatField(blank=True, null=True)

    def __str__(self):
        return '%s. %s (%s)' % (self.product, self.amount, self.session)

    class Meta:
        managed = True
        db_table = 'price'
        unique_together = (('product', 'session'),)


class ProductExtra(models.Model):
    product = models.OneToOneField(Product, db_column='product_id',
                                   primary_key=True, on_delete=models.PROTECT)
    code = models.TextField(blank=True, null=True)
    desc = models.TextField(blank=True, null=True)

    def __str__(self):
        return '%s. %s (%s)' % (self.product, self.code, self.desc)

    class Meta:
        managed = True
        db_table = 'product_extra'


class Comment(models.Model):
    comm_id = models.AutoField(primary_key=True)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class ProdComm(Comment):
    product = models.ForeignKey(Product, db_column='product_id',
                                on_delete=models.PROTECT, related_name='comm')

    def __str__(self):
        return '%s. %s (%s)' % (self.comm_id, self.author, self.created_date)

    class Meta:
        managed = True
        db_table = 'product_comm'


class StoreComm(Comment):
    store = models.ForeignKey(Store, db_column='store_id',
                              on_delete=models.PROTECT, related_name='comm')

    def __str__(self):
        return '%s. %s (%s)' % (self.comm_id, self.author, self.created_date)

    class Meta:
        managed = True
        db_table = 'store_comm'
