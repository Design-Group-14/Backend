from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from .models import User
from django.db import models

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the auth index.")

@csrf_exempt
@require_http_methods(["POST"])
def register_user(request):
    """Register a new user"""
    try:
        data = json.loads(request.body)
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        # Add optional fields if provided
        optional_fields = ['bio', 'date_of_birth', 'course_name', 'graduation_year', 'country', 'profile_picture_url']
        for field in optional_fields:
            if field in data:
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

@require_http_methods(["GET"])
def list_users(request):
    """List all users with pagination, filtering, and sorting"""
    try:
        # Pagination parameters
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 10))
        start = (page - 1) * per_page
        end = start + per_page

        # Filtering parameters
        course_filter = request.GET.get('course')
        country_filter = request.GET.get('country')
        search_query = request.GET.get('search')

        # Sorting parameters
        sort_by = request.GET.get('sort_by', 'id')
        sort_order = request.GET.get('sort_order', 'asc')

        # Base query
        users_query = User.objects.all()

        # Apply filters
        if course_filter:
            users_query = users_query.filter(course_name__iexact=course_filter)
        if country_filter:
            users_query = users_query.filter(country__iexact=country_filter)
        if search_query:
            users_query = users_query.filter(
                models.Q(username__icontains=search_query) |
                models.Q(email__icontains=search_query) |
                models.Q(first_name__icontains=search_query) |
                models.Q(last_name__icontains=search_query)
            )

        # Apply sorting
        if sort_order.lower() == 'desc':
            sort_by = f'-{sort_by}'
        users_query = users_query.order_by(sort_by)

        # Get paginated results
        total_users = users_query.count()
        users = users_query[start:end]

        # Format user data
        user_list = [{
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'course_name': user.course_name,
            'country': user.country,
            'graduation_year': user.graduation_year,
            'date_joined': user.date_joined,
            'last_login': user.last_login,
            'is_active': user.is_active
        } for user in users]

        return JsonResponse({
            'users': user_list,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total_users,
                'total_pages': (total_users + per_page - 1) // per_page
            },
            'filters': {
                'course': course_filter,
                'country': country_filter,
                'search': search_query
            },
            'sorting': {
                'sort_by': sort_by.lstrip('-'),
                'sort_order': sort_order
            }
        })
    except ValueError as e:
        return JsonResponse({'error': 'Invalid parameter value'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

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