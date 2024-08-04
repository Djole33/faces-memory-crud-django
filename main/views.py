from django.shortcuts import render
from .models import Name, Face
from random import shuffle

def index(request):
    return render(request, 'index.html')

def faces_list(request):
    # Get all faces from the database
    face_queryset = list(Face.objects.all())
    # Shuffle the list of faces
    shuffle(face_queryset)
    
    # Get all names from the database
    name_queryset = list(Name.objects.all())
    # Shuffle the list of names
    shuffle(name_queryset)
    
    # Ensure the length of name_queryset matches face_queryset
    if len(name_queryset) < len(face_queryset):
        name_queryset.extend(name_queryset[:len(face_queryset) - len(name_queryset)])

    # Pair faces and names
    face_name_pairs = list(zip(face_queryset, name_queryset))
    
    # Store the face-name pairs in the session
    request.session['face_name_pairs'] = [(face.pk, name.pk) for face, name in face_name_pairs]

    return render(request, 'faces-list.html', {'face_name_pairs': face_name_pairs})

def recall(request):
    return render(request, 'recall.html')

def results(request):
    return render(request, 'results.html')
