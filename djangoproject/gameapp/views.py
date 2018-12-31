from django.shortcuts import render
from django.http import JsonResponse

def home(request):
    return render(request, "home.html", {})

def about(request):
    from gameapp.placeholder import test_function
    return render(request, "about.html", {"my_stuff" : test_function})

def test_json(request):
    from gameapp.placeholder import test_function
    context = {
        'title': 'some title',
        'description': 'some description',
    }
    return JsonResponse(test_function())

def react_test(request):
    from gameapp.placeholder import test_function
    return render(request, "reactTest.html", {"rTest" : test_function})