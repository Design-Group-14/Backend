from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Post
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST
from .models import Post, Follow 


User = get_user_model()

@require_http_methods(["GET"])
def list_posts(request):
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 5))
    start = (page - 1) * per_page
    end = start + per_page

    posts = Post.objects.all()[start:end]
    post_list = [{
        'id': post.id,
        'user': post.user.email if hasattr(post.user, 'email') else post.user.username,
        'title': post.title,
        'content': post.content,
        'image_url': post.image_url,
        'created_at': post.created_at,
        'latitude': post.latitude,
        'longitude': post.longitude,
        'location': post.location  # ✅ keep user-written location
    } for post in posts]

    return JsonResponse({
        'posts': post_list,
        'page': page,
        'per_page': per_page,
        'total': Post.objects.count()
    })

@require_http_methods(["GET"])
def get_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    response = JsonResponse({
        'id': post.id,
        'user': post.user.email if hasattr(post.user, 'email') else post.user.username,
        'title': post.title,
        'content': post.content,
        'image_url': post.image_url,
        'latitude': post.latitude,
        'longitude': post.longitude,
        'location': post.location,  # ✅ added
        'created_at': post.created_at
    })
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

@csrf_exempt
@require_http_methods(["POST"])
def create_post(request):
    try:
        data = json.loads(request.body)

        user_email = data.get("email")

        if user_email:
            user = User.objects.filter(email=user_email).first()
            if not user:
                return JsonResponse({'error': f'User with email {user_email} not found'}, status=404)
        else:
            user = request.user
            if not user.is_authenticated:
                try:
                    user = User.objects.get(email="sultan@gmail.com")
                except User.DoesNotExist:
                    user = User.objects.first()
                    if not user:
                        return JsonResponse({'error': 'No users in the system'}, status=400)

        post = Post.objects.create(
            user=user,
            title=data.get('title', 'Untitled Post'),
            content=data['content'],
            image_url=data.get('image_url', None),
            latitude=data.get('latitude', None),
            longitude=data.get('longitude', None),
            location=data.get('location', None)  # ✅ store user-written location
        )

        return JsonResponse({
            'message': 'Post created successfully',
            'post': {
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'image_url': post.image_url,
                'latitude': post.latitude,
                'longitude': post.longitude,
                'location': post.location,
                'created_at': post.created_at
            }
        }, status=201)

    except KeyError as e:
        return JsonResponse({'error': f'Missing required field: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def get_user_posts(request, email):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    posts = Post.objects.filter(user=user).order_by('-created_at')
    post_list = [{
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'image_url': post.image_url,
        'latitude': post.latitude,
        'longitude': post.longitude,
        'location': post.location,  # ✅ added
        'created_at': post.created_at,
    } for post in posts]

    return JsonResponse({'posts': post_list}, safe=False)

@csrf_exempt
@login_required
@require_http_methods(["PUT", "PATCH"])
def update_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    data = json.loads(request.body)

    if 'title' in data:
        post.title = data['title']
    if 'content' in data:
        post.content = data['content']
    if 'image_url' in data:
        post.image_url = data['image_url']
    if 'latitude' in data:
        post.latitude = data['latitude']
    if 'longitude' in data:
        post.longitude = data['longitude']
    if 'location' in data:
        post.location = data['location']  # ✅ added

    post.save()
    return JsonResponse({'message': 'Post updated successfully'})

@csrf_exempt
@login_required
@require_http_methods(["DELETE"])
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    post.delete()
    return JsonResponse({'message': 'Post deleted successfully'})

@require_GET
def follow_status(request):
    follower_email = request.GET.get('follower')
    followed_email = request.GET.get('followed')

    if not follower_email or not followed_email:
        return JsonResponse({'error': 'Missing parameters'}, status=400)

    is_following = Follow.objects.filter(
        follower__email=follower_email,
        followed__email=followed_email
    ).exists()

    return JsonResponse({'is_following': is_following})

@csrf_exempt
@require_POST
def follow_user(request):
    data = json.loads(request.body)
    follower_email = data.get("follower")
    followed_email = data.get("followed")

    if not (follower_email and followed_email):
        return JsonResponse({'error': 'Both follower and followed are required'}, status=400)

    follower = User.objects.filter(email=follower_email).first()
    followed = User.objects.filter(email=followed_email).first()

    if not follower or not followed:
        return JsonResponse({'error': 'User not found'}, status=404)

    # Toggle follow/unfollow
    follow, created = Follow.objects.get_or_create(follower=follower, followed=followed)
    if not created:
        follow.delete()
        return JsonResponse({'message': 'Unfollowed', 'following': False})

    return JsonResponse({'message': 'Followed', 'following': True})

@require_GET
def get_followers(request, email):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    followers = Follow.objects.filter(followed=user).select_related('follower')
    follower_list = [{
        'email': f.follower.email,
        'name': f.follower.get_full_name() or f.follower.username
    } for f in followers]

    return JsonResponse({'followers': follower_list})

@require_GET
@login_required
def current_user(request):
    return JsonResponse({
        'email': request.user.email,
        'name': request.user.get_full_name() or request.user.username
    })

@require_GET
def get_following(request, email):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    following = Follow.objects.filter(follower=user).select_related('followed')
    following_list = [{
        'email': f.followed.email,
        'name': f.followed.get_full_name() or f.followed.username
    } for f in following]

    return JsonResponse({'following': following_list})

