from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'index.html')

def faces_list(request):
    return render(request, 'faces-list.html')

def recall(request):
    return render(request, 'recall.html')

def results(request):
    return render(request, 'results.html')

