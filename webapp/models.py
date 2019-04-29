from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# define item model
class Item(models.Model):
    item_name = models.CharField(max_length=50)
    item_description = models.CharField(max_length=200)
    date_posted = models.DateTimeField()
    item_image = models.ImageField(upload_to="images", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    match_item = models.OneToOneField("self", null=True, blank=True, default=None, related_name='match', on_delete=models.SET_DEFAULT)
    # set item object representation for admin etc.
    def __str__(self):
        return self.item_name

# extend the user model through a one-to-one link
class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    postcode = models.CharField(max_length=8)

# model for messages between matched users
class Message(models.Model):
    user_sent = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    user_rec = models.ForeignKey(User, related_name='recieved_messages', on_delete=models.CASCADE)
    item_sent = models.ForeignKey(Item, related_name='sent_messages', on_delete=models.CASCADE)
    item_rec = models.ForeignKey(Item, related_name='recieved_messages', on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    sent_at = models.DateTimeField()
    # todo : methods for retrieving inbox etc.


'''
credit: https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
use the receiver decorator to connect the following functions to the post_save signal
post_save hooks the functions to the User model whenever a 'save' event occurs
then userinfo is created/updated whenever a user instance is created/updated
'''
@receiver(post_save, sender=User)
def create_userinfo(sender, instance, created, **kwargs):
    if created:
        UserInfo.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_userinfo(sender, instance, **kwargs):
    instance.userinfo.save()
