from tortoise.models import Model
from tortoise import fields


class Address(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50,
                            null=False)
    country = fields.CharField(max_length=50,
                               null=False)
    region = fields.CharField(max_length=20,
                              null=False)
    province = fields.CharField(max_length=20,
                                null=False)
    city = fields.CharField(max_length=20,
                            null=False)
    street = fields.CharField(max_length=50,
                              null=False)
    unit_name = fields.CharField(max_length=50,
                                 null=False)
    zipcode = fields.IntField(null=False)
    longtitude = fields.DecimalField(max_digits=5,
                                     decimal_places=6,
                                     null=False)
    latitude = fields.DecimalField(max_digits=5,
                                   decimal_places=6,
                                   null=False)
