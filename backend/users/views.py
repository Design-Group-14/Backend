from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
import json
from datetime import datetime

User = get_user_model()

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the users index.")

@csrf_exempt
@require_http_methods(["POST"])
def register_user(request):
    """Register a new user"""
    try:
        data = json.loads(request.body)
        user = User.objects.create_user(
            email=data['email'],
            password=data['password'],
            username=data.get('username', '')  # Optional username
        )
        # Add optional fields if provided
        optional_fields = ['bio', 'date_of_birth', 'course_name', 'graduation_year', 'country', 'profile_picture_url']
        for field in optional_fields:
            if field in data:
                if field == 'date_of_birth':
                    user.date_of_birth = datetime.strptime(data['date_of_birth'], "%Y-%m-%d").date()
                elif field == 'graduation_year':
                    user.graduation_year = int(data['graduation_year'])
                else:
                    setattr(user, field, data[field])
        user.save()
        
        return JsonResponse({
            'message': 'User created successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }, status=201)
    except KeyError as e:
        return JsonResponse({'error': f'Missing required field: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    

@csrf_exempt
@require_http_methods(["POST"])
def login_user(request):
    """Authenticate and log in a user"""
    try:
        data = json.loads(request.body)
        user = authenticate(request, email=data.get('email'), password=data.get('password'))
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful'})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)

@require_http_methods(["GET"])
def list_users(request):
    """List all users (with pagination)"""
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 10))
    start = (page - 1) * per_page
    end = start + per_page
    
    users = User.objects.all()[start:end]
    user_list = [{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'course_name': user.course_name,
        'country': user.country
    } for user in users]
    
    return JsonResponse({
        'users': user_list,
        'page': page,
        'per_page': per_page,
        'total': User.objects.count()
    })

@require_http_methods(["GET"])
def get_user(request, user_id):
    """Get a specific user's details"""
    user = get_object_or_404(User, id=user_id)
    return JsonResponse({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'bio': user.bio,
        'course_name': user.course_name,
        'graduation_year': user.graduation_year,
        'country': user.country,
        'profile_picture_url': user.profile_picture_url
    })

@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
@login_required
def update_user(request, user_id):
    """Update a user's details"""
    if request.user.id != user_id and not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    user = get_object_or_404(User, id=user_id)
    data = json.loads(request.body)
    
    # Fields that can be updated
    allowed_fields = ['username', 'email', 'bio', 'date_of_birth', 
                     'course_name', 'graduation_year', 'country', 
                     'profile_picture_url']
    
    for field in allowed_fields:
        if field in data:
            if field == 'date_of_birth':
                user.date_of_birth = datetime.strptime(data['date_of_birth'], "%Y-%m-%d").date()
            elif field == 'graduation_year':
                user.graduation_year = int(data['graduation_year'])
            else:
                setattr(user, field, data[field])
    
    user.save()
    return JsonResponse({'message': 'User updated successfully'})

@csrf_exempt
@require_http_methods(["DELETE"])
@login_required
def delete_user(request, user_id):
    """Delete a user"""
    if request.user.id != user_id and not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return JsonResponse({'message': 'User deleted successfully'})

@login_required
def get_my_profile(request):
    """Get the current user's profile"""
    user = request.user
    return JsonResponse({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'bio': user.bio,
        'course_name': user.course_name,
        'graduation_year': user.graduation_year,
        'country': user.country,
        'profile_picture_url': user.profile_picture_url
    })

@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
@login_required
def update_my_profile(request):
    """Update the current user's profile"""
    return update_user(request, request.user.id)
