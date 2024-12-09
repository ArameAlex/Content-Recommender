from UserApp.views import check_user
from modules.json_response import json_contents_list
from modules.visit_count_algorithm import get_ordered_posts
from .models import ContentModel, ViewCountModel, FavoritePosts
from django.http import JsonResponse, HttpRequest

"""MAKE THE ACCESS TOKEN TO 5MIN!"""


def json_post(model):
    contents = []
    for post in model:
        post_data = json_contents_list(post)
        contents.append(post_data)
    return contents


def home(request):
    user = check_user(request=request)
    # order posts based on user activities
    ordered_posts = get_ordered_posts(user)
    # json the result of the ordered post
    contents = json_post(ordered_posts)

    try:
        return JsonResponse({
            "message": f"Hello, {user.username}!",
            "user_id": user.id,
            "contents": contents
        }, safe=False, status=200)
    except:
        return JsonResponse(user, safe=False, status=401)


def single_content(request, id):
    # Fetch the content
    content = ContentModel.objects.filter(id=id).first()
    if not content:
        return JsonResponse({"message": "No post found"}, safe=False, status=404)

    content.view_count += 1
    content.save()
    # Check the logged-in user
    user = check_user(request=request)
    try:
        # Handle view count
        view_count_obj, created = ViewCountModel.objects.get_or_create(
            content=content,
            user=user,
            defaults={"view_count": 0}  # Default view_count for new objects
        )
        # Increment the view count
        view_count_obj.view_count += 1
        view_count_obj.save()

        # Prepare the content response
        contents = json_contents_list(content)

        # Return the response
        return JsonResponse({
            "message": f"Hello, {user.username}!",
            "user_id": user.id,
            "contents": contents,
            "your_view_count": view_count_obj.view_count
        }, safe=False, status=200)
    except Exception:
        return JsonResponse(user, safe=False, status=401)


def saved_contents(request: HttpRequest):
    user = check_user(request=request)

    try:
        user_contents = FavoritePosts.objects.filter(user_id=user.id)
        content_ids = user_contents.values_list('content_id', flat=True)
        favourite_contents = ContentModel.objects.filter(id__in=content_ids)

        # paginator = Paginator(favourite_products, 16)
        # page_number = request.GET.get('page', 1)
        # page_obj = paginator.get_page(page_number)

        # Prepare the product data manually to include the full category details
        contents = []
        for product in favourite_contents:
            product_data = json_post(product)
            contents.append(product_data)
        # Return the response
        return JsonResponse({
            "message": f"Hello, {user.username}!",
            "user_id": user.id,
            "contents": contents,
        }, safe=False, status=200)
    except Exception:
        return JsonResponse(user, safe=False, status=401)


def create_comment_view(request):
    pass
