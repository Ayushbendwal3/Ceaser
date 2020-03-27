from django.shortcuts import render
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from Ceaser.forms import UserForm,UserProfileInfoForm
from Ceaser.models import Document
from django.conf import settings
from SIH import settings as s
import pytesseract as pl
from PIL import Image
import os

# Create your views here.

def index(request):
    return render(request, 'index.html')

@login_required
def upload(request):
    if request.method == 'POST' and request.FILES['doc_img']:
        document = Document()
        document.document_name = request.POST.get('doc_name')
        document.document_img = request.FILES['doc_img']
        document.document_desc = request.POST.get('doc_desc')
        document.document_date = request.POST.get('doc_date')
        document.save()

        doc = Document.objects.all()
        temp_list = list(Document.objects.values_list('document_img'))
        for i in range(0, len(temp_list)):
	        temp_list[i] = list(temp_list[i])

        new_doc = []
        new_doc = temp_list[-1]

        def listToString(s):
            str1 = ""  
            
            for ele in s:  
                str1 += ele   
                
            return str1
        
        img_name = listToString(new_doc)
        img_path = s.BASE_DIR+settings.MEDIA_URL+img_name

        extracted_image = pl.image_to_string(Image.open(img_path))

        params = {'Data': doc, 'processed_img': extracted_image}
        return render(request, 'show.html', params) 

    else:
        return HttpResponse('Failed To Upload')

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def special(request):
    return HttpResponse("You are logged in !!")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                print('found it')
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'login.html', {})  