from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from django.contrib.auth.models import User
from .models import Item
from .forms import SignUpForm

def index(request):
    latest_items = Item.objects.order_by('-date_posted')[:5]
    context = {
        'item_list': latest_items,
    }
    return render(request, 'webapp/index.html', context)

# item detail page
def item_detail(request, item_id):
    # check item exists
    try:
        # save item in variable using id
        i = Item.objects.get(pk=item_id)
    except Item.DoesNotExist:
        # raise appropriate error if item not found
        raise Http404("Item id is not valid")
    # get user that posted item
    user = User.objects.get(id=i.user_id)
    # if item is matched get the partner
    if i.match_item is not None:
        j = i.match_item
    context = {
        'item': i,
        'user': user,
    }
    return render(request, 'webapp/item_detail.html', context)

# random item
def item(request):
    # get current user details
    current_user = request.user
    # check whether user has uploaded an item that is currently available
    item_available = False
    try:
        user_items = Item.objects.filter(user=current_user.id)
    except:
        pass
    for item in user_items:
        if item.available == True:
            item_available = True
            break
    # get list of all available items
    item_list = Item.objects.filter(available=True).order_by("?")
    return render(request, 'webapp/item.html', {'item_available': item_available, 'item_list': item_list})

# page to add new item
@login_required
def item_add(request):
    # if request is a post try to ave item
    if request.method == 'POST' and request.FILES['pic']:
        # get form data
        item_name = request.POST.get("item_name")
        item_description = request.POST.get("item_description")
        item_image = request.FILES.get("pic")
        # create item from data
        item = Item(item_name=item_name, item_description=item_description, item_image=item_image, date_posted=timezone.now())
        item.save()
        return redirect(item_detail, item_id=item.id)
    else:
        return render(request, 'webapp/item_add.html')

# page to signup/post signup form
def signup(request):
    # if method is post then try to create user
    if request.method == 'POST':
        # built in django form to create standard user with no privileges
        form = SignUpForm(request.POST)
        # validate data with inbuilt django form method
        if form.is_valid():
            # create the user
            user = form.save()
            # refresh to load the userinfo created by the post_save signal
            user.refresh_from_db()
            # save the postcode, if given
            if form.cleaned_data.get('postcode'):
                user.userinfo.postcode = form.cleaned_data.get('postcode')
                user.save()
            # get user credentials to automatically login for good user experience
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            # redirect new user to homepage
            return redirect('index')
    # if method is get then go to signup page
    else:
        form = SignUpForm()
    return render(request, 'webapp/signup.html', {'form': form})

# logout view
def logout_view(request):
    logout(request)
    return redirect('index')

# login view
def login_view(request):
    # if request is post then try to login user
    if request.method == 'POST':
        # get username and password from login form
        username = request.POST.get('username')
        password = request.POST.get('password')
        # try to login user
        user = authenticate(username=username, password=password)
        if user:
            # if user is valid and active, login and redirect to index
            if user.is_active:
                login(request, user)
                return redirect('index')
            else:
                # inactive account error
                return HttpResponse("User Inactive")
        else:
            # bad username/password error
            return HttpResponse("Invalid username/password combination")
    # if request is get then render login page
    else:
        return render(request, 'webapp/login.html', {})

# page for logging in user to browse available items
@login_required
def browse_items(request):
        # get current user details
        current_user = request.user
        # check whether user has uploaded an item that is currently available
        item_available = False
        try:
            user_items = Item.objects.filter(user=current_user.id)
        except:
            pass
        for item in user_items:
            if item.available == True:
                item_available = True
                break
        # get list of all available items
        item_list = Item.objects.filter(available=True).order_by("?")
        return render(request, 'webapp/items.html', {'item_available': item_available, 'item_list': item_list})


'''
# uncomment to set custom 404 error view
def notfound(request, exception):
    return HttpResponse("That page could not be found!")
'''
