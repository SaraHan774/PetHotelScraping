from peewee import *
import credentials


db = SqliteDatabase('pet_hotels.db')
sqlite_db = MySQLDatabase('my_petmily', user='root', password=credentials.MYSQL_PASSWORD,
                          host='localhost', port=3306)


class Hotel(Model):
    id = BigAutoField(primary_key=True)
    name = CharField(max_length=50, null=True, unique=True)
    address = CharField(max_length=255, null=True, unique=True)
    address_detail = CharField(max_length=255, null=True)
    website_link = CharField(max_length=127, null=True)
    zipcode = IntegerField(default=0, null=True)
    latitude = FloatField(default=0, null=True)
    longitude = FloatField(default=0, null=True)
    week_open_time = DateTimeField(null=True)
    week_close_time = DateTimeField(null=True)
    sat_open_time = DateTimeField(null=True)
    sat_close_time = DateTimeField(null=True)
    sun_open_time = DateTimeField(null=True)
    sun_close_time = DateTimeField(null=True)
    week_price = IntegerField(null=True)
    sat_price = IntegerField(null=True)
    sun_price = IntegerField(null=True)
    phone_number = CharField(null=True)
    is_monitored = BooleanField(null=True)
    is_neutered_only = BooleanField(null=True)
    supported_dog_size = IntegerField(null=True)
    user_rating = FloatField(null=True)
    star = IntegerField(null=True)
    created_at = DateTimeField(null=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        database = sqlite_db
        table_name = 'hotels'
        indexes = (
            (('name', 'address'), True)
        )

