```python
# Python code for Dog Selling Application

# Django models for user registration, dog listings, messaging, payments, reviews, and admin functionalities

from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    # Add more fields for user profile information

class Dog(models.Model):
    breed = models.CharField(max_length=100)
    age = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Add more fields for dog attributes

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # Add more fields for payment details

class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add more fields for admin functionalities

# Implement encryption, authentication, and authorization protocols

# Design architecture for scalability and efficient data handling

# Conduct thorough testing procedures including unit, integration, and user acceptance testing

# Utilize React for frontend development to achieve responsive design and real-time updates
```
This Python code provides a basic structure for implementing the Dog Selling Application using Django models for backend functionalities and outlines the necessary steps to fulfill the technical requirements mentioned in the context.