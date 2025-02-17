from django.shortcuts import render, redirect, get_object_or_404
from .models import Item
from django.utils.text import slugify
from .forms import ItemForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm 
from django.contrib.auth import login,logout 
from django.contrib.auth.decorators import login_required


def registration_view(request):
    form = UserCreationForm() 
    if request.method == 'POST':
        form = UserCreationForm(request.POST) 
        if form.is_valid(): 
            form.save()
            return redirect('item_list')
    return render(request,'include/registration.html',{'form':form})


def login_user(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('item_list')
    return render(request,'include/signin.html',{'form':form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('registration_view')

@login_required
def create_item(request):
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(request.POST) # This will get the data from the form        
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user             
            item.name = slugify(item.name)  # Convert title to slug format before saving
            item.save()
            return redirect('item_list')
    return render(request, 'myapp/item_form.html', {'form': form})


@login_required       
def item_list(request):
    # print(request.user)
    # tasks = Task.objects.all()
    items = Item.objects.filter(user=request.user)
    return render(request, 'myapp/item_list.html', {'items': items})

@login_required
def item_detail(request, name):
    slug = slugify(name)
    item = get_object_or_404(Item, title__iexact=slug)
    return render(request, 'myapp/item_detail.html', {'item': item})

@login_required
def item_update(request, name):
    slug = slugify(name)
    # task = get_object_or_404(Task,title__iexact=slug)
    item = get_object_or_404(Item, title__iexact=slug,user=request.user)
    form = ItemForm(instance=item)
    
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            item.name = slugify(item.name)
            item.save()
            return redirect('item_list')
    
    return render(request, 'myapp/item_form.html', {'form': form})
    
    
def item_delete(request,id):
    task = get_object_or_404(Item, id=id,user=request.user)
    task.delete()
    return redirect('item_list')
    
    
