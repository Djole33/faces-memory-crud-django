from django.shortcuts import render, redirect
from .models import Name, Face
from random import shuffle
from .forms import NameForm

def index(request):
    if 'face_name_pairs' in request.session:
        del request.session['face_name_pairs']
    if 'current_index' in request.session:
        del request.session['current_index']
    if 'guesses' in request.session:
        del request.session['guesses']
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
    # Initialize session variables if not present
    if 'guesses' not in request.session:
        request.session['guesses'] = []
    if 'current_index' not in request.session:
        request.session['current_index'] = 0  # Start with index 0

    # Retrieve guesses and current index
    guesses = request.session.get('guesses', [])
    current_index = request.session.get('current_index', 0)

    # Retrieve face_name_pairs from session
    face_name_pairs = request.session.get('face_name_pairs', [])

    # Check if there are any face_name_pairs
    if not face_name_pairs:
        return redirect('/results')  # Redirect to a completion page or handle appropriately

    # Get current face data
    if 0 <= current_index < len(face_name_pairs):
        current_face_pk, _ = face_name_pairs[current_index]
        try:
            face = Face.objects.get(pk=current_face_pk)
            face_name_data = {'face_url': face.face.url}
        except Face.DoesNotExist:
            face_name_data = {'face_url': ''}
    else:
        face_name_data = {'face_url': ''}

    if request.method == "POST":
        if 'submit_guess' in request.POST:
            form = NameForm(request.POST)
            if form.is_valid():
                guess = form.cleaned_data['name']
                # Append the new guess
                guesses.append(guess)
                request.session['guesses'] = guesses  # Update session
                request.session.modified = True  # Mark session as modified

                # Move to the next picture
                current_index += 1
                if current_index >= len(face_name_pairs):
                    return redirect('/results')  # Redirect to a completion page

                request.session['current_index'] = current_index  # Update current index
                return redirect('/recall')
        elif 'delete_last_guess' in request.POST:
            if guesses:
                guesses.pop()  # Remove the last guess
                request.session['guesses'] = guesses  # Update session
                request.session.modified = True  # Mark session as modified
        elif 'see_results' in request.POST:
            return redirect('/results')

    else:
        form = NameForm()

    return render(request, 'recall.html', {
        'form': form,
        'guesses': guesses,
        'face_name_data': face_name_data
    })

def results(request):
    # Retrieve guesses from session
    guesses = request.session.get('guesses', [])
    # Clear guesses from session after showing results
    request.session['guesses'] = []
    request.session.modified = True

    # Retrieve face_name_pairs from session
    face_name_pairs_pks = request.session.get('face_name_pairs', [])
    
    # Fetch the Face and Name objects from the database
    face_name_pairs = []
    for face_pk, name_pk in face_name_pairs_pks:
        try:
            face = Face.objects.get(pk=face_pk)
            name = Name.objects.get(pk=name_pk)
            face_name_pairs.append((face, name))
        except (Face.DoesNotExist, Name.DoesNotExist):
            continue  # Skip if face or name does not exist

    return render(request, 'results.html', {'guesses': guesses, 'face_name_pairs': face_name_pairs})
