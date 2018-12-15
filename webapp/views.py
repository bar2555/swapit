from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Item

def index(request):
    return HttpResponse("Hello world, this is swapit!")

# item detail page
def detail(request, item_id):
    # check item exists
    try:
        # save item in variable using id
        i = Item.objects.filter(id=item_id)[0]
    except:
        # raise appropriate error if item not found
        return HttpResponse("Item id is not valid", status=404)
    return HttpResponse("This is an item page. The item desciption is: " + i.item_description)

'''
# uncomment to set custom 404 error view
def notfound(request, exception):
    return HttpResponse("That page could not be found!")
'''
