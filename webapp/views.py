from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth import login, authenticate, logout

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
    context = {
        'item': i,
    }
    return render(request, 'webapp/item_detail.html', context)

# page to add new item
def item_add(request):
    if request.method == 'GET':
        return render(request, 'webapp/item_add.html')
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

'''
# uncomment to set custom 404 error view
def notfound(request, exception):
    return HttpResponse("That page could not be found!")
'''
