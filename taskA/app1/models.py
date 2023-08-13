from django.db import models

from django.db import models
import bcrypt

class UserManager(models.Manager):
    def basic_validator(self,postData):
        errors ={}
        if len(postData['fname']) < 2 or len(postData['lname']) < 2:
            errors['fname'] = 'you must enter 2 char at least for the name'
        if len(postData['pwd']) < 8:
            errors['pwd'] = 'you must enter 8 char at least for the password'
        if postData['pwd']!=postData['cpwd']:
            errors['cpw'] = 'the passwords are not the same'
        users = User.objects.all()
        for user in users:
            if user.email == postData['email']: 
                errors['email']='this email already token'
                break
        return errors
    
    def login_validator(self,postData):
        errors ={}
        user = User.objects.filter(email=postData['email'])
        if user:
            if (user[0].email != postData['email']):
                errors['log'] ='email or passord are not correct '
            if not (bcrypt.checkpw(postData['pwd'].encode(), user[0].pwd_hash.encode())):
                    errors['log'] ='email or passord are not correct '
        else:
            errors['log'] ='email or passord are not correct '
        if len(postData['pwd']) < 8:
            errors['pwd'] = 'you must enter 8 char at least for the password'
        return errors

class CustomerManager(models.Manager):
    def basic_validator(self,postData):
        errors ={}
        if len(postData['fname']) < 2 or len(postData['lname']) < 2:
            errors['fname'] = 'you must enter 2 char at least for the name'
        

        if len(postData['phone']) < 6:
            errors['phone'] = 'you must enter 6 digit at least for the phone num'
        
        if len(postData['address']) < 10:
            errors['address'] = 'you must enter 10 char for the address '
        
        if len(postData['email']) < 1:
            errors['email'] = 'you must enter the email '
        

        return errors
    
class ServiceManager(models.Manager):
    def basic_validator(self,postData):
        errors ={}
        if len(postData['name']) < 2 :
            errors['name'] = 'you must enter 2 char at least for the name'
        if len(postData['desc']) < 10:
            errors['desc'] = 'description must be at least 10 char'
        if int(postData['price']) < 1:
            errors['price'] = 'price required'

        return errors



class User(models.Model):
    fname = models.TextField(max_length=45)
    lname = models.TextField(max_length=45)
    email = models.TextField(max_length=45)
    pwd_hash = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()



class Customer(models.Model):
    fname = models.TextField(max_length=45)
    lname = models.TextField(max_length=45)
    email = models.TextField(max_length=45)
    phone = models.TextField()
    address = models.TextField(default=None)
    user = models.ForeignKey(User,related_name='customers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CustomerManager()


class Service(models.Model):
    name = models.TextField()
    desc = models.TextField()
    price = models.FloatField()
    isActive = models.BooleanField(default=True)

    user = models.ForeignKey(User,related_name='services',on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ServiceManager()


class Active(models.Model):
    isActive = models.BooleanField(default=True)
    service = models.ForeignKey(Service,related_name='ActiveServices',on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,related_name='ActiveCustomers',on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



