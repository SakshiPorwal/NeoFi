from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Note, NoteChange
from .serializers import NoteSerializer, NoteChangeSerializer

@api_view(['POST'])
def signup(request):
    try:
        with transaction.atomic():
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password')

            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                return Response({'error': 'Username or email already taken'}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create_user(username=username, email=email, password=password)

            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'username': user.username}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_note(request):
    serializer = NoteSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response({'message': 'Note created successfully'}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_note(request, id):
    note = get_object_or_404(Note, pk=id, user=request.user)
    serializer = NoteSerializer(note)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def share_note(request):
    note_id = request.data.get('note_id')
    users_to_share = request.data.get('users_to_share')

    note = get_object_or_404(Note, pk=note_id, user=request.user)

    note.shared_with.add(*users_to_share)

    return Response({'message': 'Note shared successfully'}, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_note(request, id):
    note = get_object_or_404(Note, pk=id, user=request.user)
    new_content = request.data.get('new_content')

    note.content = new_content
    note.save()

    NoteChange.objects.create(note=note, user=request.user, content_change=new_content)

    return Response({'message': 'Note updated successfully'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def version_history(request, id):
    note = get_object_or_404(Note, pk=id, user=request.user)
    changes = NoteChange.objects.filter(note=note)

    serializer = NoteChangeSerializer(changes, many=True)

    return Response({'version_history': serializer.data}, status=status.HTTP_200_OK)



#validation 

from django.shortcuts import render, get_object_or_404, redirect
from .models import Note
from .forms import NoteForm

def create_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user  
            note.save()
            return redirect('note-list')
    else:
        form = NoteForm()

    return render(request, 'create_note.html', {'form': form})

def update_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id)

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note-list')
    else:
        form = NoteForm(instance=note)

    return render(request, 'update_note.html', {'form': form, 'note': note})



# error handling

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Note
from .forms import NoteForm
from .exceptions import NoteCreationError, NoteUpdateError

def create_note(request):
    try:
        if request.method == 'POST':
            form = NoteForm(request.POST)
            if form.is_valid():
                note = form.save(commit=False)
                note.user = request.user  
                note.save()
                return JsonResponse({'message': 'Note created successfully'}, status=201)
            else:
                raise NoteCreationError('Invalid input data for note creation')
    except NoteCreationError as e:
        return JsonResponse({'error': str(e)}, status=400)

def update_note(request, note_id):
    try:
        note = get_object_or_404(Note, pk=note_id)
        
        if request.method == 'POST':
            form = NoteForm(request.POST, instance=note)
            if form.is_valid():
                form.save()
                return JsonResponse({'message': 'Note updated successfully'})
            else:
                raise NoteUpdateError('Invalid input data for note update')
    except NoteUpdateError as e:
        return JsonResponse({'error': str(e)}, status=400)
