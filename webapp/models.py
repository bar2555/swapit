from django.db import models


# define user model
# TODO

# define item model
class Item(models.Model):
    item_name = models.CharField(max_length=50)
    item_description = models.CharField(max_length=200)
    date_posted = models.DateTimeField()
    # set item object representation for admin etc.
    def __str__(self):
        return self.item_name
