from django.db import models

# Create your models here.
class Student(models.Model):
    # id = models.AutoField() added automatically by django
    name = models.CharField(max_length=100)
    age = models.IntegerField()  # age = models.IntegerField(default=18)
    email = models.EmailField()
    address = models.TextField()
    image = models.ImageField()
    file = models.FileField()



class Car(models.Model):
    car_name = models.CharField(max_length=200)
    speed = models.IntegerField(default=100)

    def __str__(self) -> str:
        return self.car_name +" "+str(self.speed)




"""

>> from home.models import *
>>> student = Student(name="shubh",age="20",email="shubh@gmail.com", address ="Mandi")
>>> student
<Student: Student object (None)>
>>> student.save()
>>> student
<Student: Student object (1)>
>>> student
<Student: Student object (1)>

student = Student.objects.create(name="shubh2",age="22",email="shubh2@gmail.com", address ="Mandi2")
###Student is a model manager
"""



"""
CREATE

create car obj:
1. car = Car(car_name="Nexon",speed=110) # need to save using car.save()
2. car = Car.objects.create(car_name="Nexon",speed=110)  # auto save
3. car_obj = {'car_name':'alto','speed':120}
    car = Car.objects.create(**car_obj)
"""

"""
READ:
>>> cars = Car.objects.all()
>>> cars
<QuerySet [<Car: Car object (1)>, <Car: Car object (2)>, <Car: Car object (3)>, <Car: Car object (4)>]>


>>>car = Car.objects.get('car_name'='Nexon')
>>>car
>>>Nexon 120
"""

"""
UPDATE

>>> Car.objects.filter(id=1).update(car_name="new_car")
>>>1

>>>Car.objects.filter(id=1).delete()
>>>(1,{home.Car':1})
"""

"""
DELETE
>>>Car.objects.all().delete()
>>>(3,{'home.Car':3})
"""