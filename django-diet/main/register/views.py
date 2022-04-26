from django.db import reset_queries
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def register(response):
    """
    User registration form used with html to render on website
    Collects Username and Password to create user
    """

    if response.user.is_authenticated:
        return redirect("/tracker")

    #When user hits submit button
    if response.method == "POST":
        form = UserCreationForm(response.POST) #Pre-built registration form 

        #Ensure form has right data types as inputs
        if form.is_valid():
            form.save()

            #Login user by validating form credentials in database
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],)

            login(response, new_user)

            return redirect("/tracker")

    
    #Create empty form for when page first loads
    else:
        form = UserCreationForm()

    #Display html on webpage with django form boxes
    return render(response, "register.html", {"form": form})