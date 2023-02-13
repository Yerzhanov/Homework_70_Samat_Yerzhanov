from django.shortcuts import render


def signupuser(request):
    return render(request, 'todo/sighupuser.html')