from django.db import models
from django import forms
from django.urls import reverse
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def reg_validation(self, form):
        errors={}
        if len(form['fname']) < 2:
            errors['fname']="First name must have at least 2 characters"
        if len(form['lname']) < 2:
            errors['lname'] = "Last name must have at least 2 characters"
        if not EMAIL_REGEX.match(form['email']):
            errors['email']= "Invalid Email format" 
        email_check= self.filter(email=form['email'])
        if email_check:
            errors['email'] = "email already in use"
        if len(form['password']) < 7:
            errors['password'] = "Password must be minimum of 8 characters"
        if (form['password']) != (form['confirmpw']):
            errors['password'] = "Passwords do not match"
        return errors
    def log_validation(self, email, password):
        users = User.objects.filter(email=email)
        if not users:
            return False
        user=users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())

class User(models.Model):
    first_name= models.CharField(max_length=45)
    last_name= models.CharField(max_length=45)
    email= models.CharField(max_length=255)
    password= models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects=UserManager()

class Food(models.Model):
    food_name= models.CharField(max_length=255)
    food_calories = models.IntegerField()
    fat = models.IntegerField(default=0)
    carbs = models.IntegerField(default=0)
    protein = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.food_name

class Exercise(models.Model):
    exercise_name = models.CharField(max_length=255)
    exer_calories = models.IntegerField(default=0)
    exerciser= models.ForeignKey(User, on_delete=models.CASCADE)
    date_done = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Meal(models.Model):
    meal_tag = models.CharField(max_length=50, default="breakfast")
    meal= models.ForeignKey(Food, related_name="food", on_delete=models.CASCADE)
    eater = models.ForeignKey(User, related_name="meal_consumer", on_delete=models.CASCADE)
    date_eaten= models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.meal_tag

class Weight(models.Model):
    weigh_in = models.IntegerField()
    weigher=models.ForeignKey(User, related_name="user_weight", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Blog(models.Model):
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=250)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
