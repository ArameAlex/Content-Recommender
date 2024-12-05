from UserApp.views import check_user
from modules.json_response import json_contents_list
from modules.visit_count_algorithm import get_ordered_posts
from .models import ContentModel, ViewCountModel
from django.http import JsonResponse
"""
CHANGE THE DAY DELTA OF ACCESS TOKEN!!
"""


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
        contents = json_contents_list(content)  # Assuming this converts the content to JSON

        # Return the response
        return JsonResponse({
            "message": f"Hello, {user.username}!",
            "user_id": user.id,
            "contents": contents,
            "your_view_count": view_count_obj.view_count
        }, safe=False, status=200)
    except:
        return JsonResponse(user, safe=False, status=401)
