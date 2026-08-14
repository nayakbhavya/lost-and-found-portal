from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Item
from .forms import ItemForm, RegisterForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# 🏠 Home + Search
def home(request):
    query = request.GET.get('q')

    if query:
        items = Item.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )
    else:
        items = Item.objects.all()

    return render(request, 'home.html', {
        'items': items,
        'query': query
    })


# ➕ Add Item
@login_required
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            return redirect('home')
    else:
        form = ItemForm()

    return render(request, 'add_item.html', {'form': form})


# ✏️ Edit Item
@login_required
def edit_item(request, id):
    item = get_object_or_404(Item, id=id, user=request.user)

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ItemForm(instance=item)

    return render(request, 'edit_item.html', {'form': form})


# ❌ Delete Item
@login_required
def delete_item(request, id):
    item = get_object_or_404(Item, id=id, user=request.user)
    item.delete()
    return redirect('home')


# 📝 Register
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


# 🔐 Login
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')

    return render(request, 'login.html')


# 🚪 Logout
def user_logout(request):
    logout(request)
    return redirect('home')