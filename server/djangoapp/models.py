from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        return self.name

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer = models.IntegerField()
    name = models.CharField(max_length=150)
    CAR_CHOICES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'WAGON'),
    ]
    car_choice = models.CharField(max_length=10, choices=CAR_CHOICES)
    year = models.DateField()

    def __str__(self):
        return self.name

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer(models.Model):
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    full_name = models.CharField(max_length=255)
    id = models.AutoField(primary_key=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    long = models.DecimalField(max_digits=9, decimal_places=6)
    short_name = models.CharField(max_length=100)
    st = models.CharField(max_length=2)
    zip = models.CharField(max_length=10)

    def __str__(self):
        return f"Dealer name: {self.full_name}"

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview(models.Model):
    dealership = models.CharField(max_length=150)
    name = models.CharField(max_length=150)
    purchase = models.DateField()
    review = models.TextField()
    purchase_date = models.DateField()
    car_dealer = models.ForeignKey(CarDealer, on_delete=models.CASCADE)
    car_make = models.CharField(max_length=150)
    car_model = models.CharField(max_length=150)
    car_year = models.IntegerField()
    sentiment = models.CharField(max_length=50)
    id = models.IntegerField(primary_key=True)

    def __str__(self):
        return self.name