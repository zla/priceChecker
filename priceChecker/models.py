# # This is an auto-generated Django model module.
# # You'll have to do the following manually to clean this up:
# #   * Rearrange models' order
# #   * Make sure each model has one field with primary_key=True
# #   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
# #   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# # Feel free to rename the models, but don't rename db_table values or field names.
# from django.db import models
# from model_utils import Choices


# class Prices(models.Model):
#     product_id = models.ForeignKey(
#             Products, db_column='id', on_delete=models.PROTECT)
#     session_id = models.ForeignKey(
#             Sessions, db_column='id', on_delete=models.PROTECT)
#     price = models.FloatField(blank=True, null=True)  # This field type is a guess.

#     class Meta:
#         managed = True
#         db_table = 'prices'
#         unique_together = (('product_id', 'session_id'),)


# class Products(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.TextField()
#     url = models.TextField()
#     ACTIVITIES = Choices(
#         (0, 'inactive', 'Inactive'),
#         (1, 'active', 'Active'),
#     )
#     active = models.CharField(choices=ACTIVITIES, default=ACTIVITIES.active)
#     store_id = models.ForeignKey(
#             Stores, db_column='id', on_delete=models.PROTECT)
#     sheet = models.TextField(blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'products'


# class ProductsExtra(models.Model):
#     id = models.OneToOneField(
#             Products, primary_key=True, on_delete=models.PROTECT)
#     code = models.TextField(blank=True, null=True)
#     desc = models.TextField(blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'products_extra'


# class Sessions(models.Model):
#     id = models.AutoField(primary_key=True)
#     date = models.TextField(blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'sessions'


# class Stores(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.TextField()

#     class Meta:
#         managed = True
#         db_table = 'stores'
