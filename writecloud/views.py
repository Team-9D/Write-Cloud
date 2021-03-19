from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect 

def writecloud_user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        writecloud_user = authenticate(username=username, password=password)

        if writecloud_user:

            if writecloud_user.is_active:
                login(request, user)


            else:
                return HttpResponse("Your WriteCloud account has been disabled.")
        else:
            print(f"Login details not valid: {username}, {password}")
            return HttpResponse("The login details provided are invalid.")

    else:
        return render(request, 'writecloud/login.html')

            

        
