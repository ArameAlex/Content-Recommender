import json

from prompt_toolkit.validation import ValidationError

from UserApp.views import check_user
from modules.json_response import json_contents_list, json_comments_list
from modules.visit_count_algorithm import get_ordered_posts
from .models import ContentModel, ViewCountModel, FavoritePosts, PostComment
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

    if user is None:  # If user is not logged in, return error
        return JsonResponse({"message": "You are not logged"}, status=401)

    return JsonResponse({
        "message": f"Hello, {user.username}!",
        "user_id": user.id,
        "contents": contents
    }, safe=False, status=200)


def single_content(request, content_id):
    # Fetch the content
    content = ContentModel.objects.filter(id=content_id).first()
    if not content:
        return JsonResponse({"message": "No post found"}, safe=False, status=404)

    content.view_count += 1
    content.save()
    # Check the logged-in user
    user = check_user(request=request)

    if user is None:  # If user is not logged in, return error
        return JsonResponse({"message": "You are not logged"}, status=401)

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

    # comments of content
    comments = PostComment.objects.filter(content_id=content_id)
    comments_json = None
    if comments is not None:
        comments_json = json_comments_list(comments)

    # Return the response
    return JsonResponse({
        "message": f"Hello, {user.username}!",
        "user_id": user.id,
        "contents": contents,
        "comments": comments_json,
        "your_view_count": view_count_obj.view_count
    }, safe=False, status=200)


def saved_contents(request: HttpRequest):
    user = check_user(request=request)

    if user is None:  # If user is not logged in, return error
        return JsonResponse({"message": "You are not logged"}, status=401)

    user_contents = FavoritePosts.objects.filter(user_id=user.id)
    content_ids = user_contents.values_list('content_id', flat=True)
    favourite_contents = ContentModel.objects.filter(id__in=content_ids)

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


def unsaved_contents(request: HttpRequest, content_id):
    user = check_user(request=request)

    if user is None:  # If user is not logged in, return error
        return JsonResponse({"message": "You are not logged"}, status=401)

    instance = FavoritePosts.objects.filter(id=content_id, user_id=user.id)
    if not instance:
        return JsonResponse({"Message": "No Saved Post Find"}, safe=False, status=404)
    else:
        instance.delete()
        return JsonResponse({"Message": "Post Removed From Saved contents"}, safe=False, status=200)


"""
    Create Comment (get userid from token, post id from 
    request url <int:pk>, and date is auto set)
    Delete Comment
    Edit Comment (just Text)
    Get Comment in single post view
"""


def create_comment_view(request, content_id):
    # Check if the user is logged in
    user = check_user(request=request)
    if user is None:  # If user is not logged in, return error
        return JsonResponse({"message": "You are not logged"}, status=401)

    # Check if content exists
    try:
        content = ContentModel.objects.get(id=content_id)
    except ContentModel.DoesNotExist:
        return JsonResponse({"message": "Content not found"}, status=404)

    # Parse the incoming data
    try:
        data = json.loads(request.body)
        message = data.get("message", "").strip()
        reply_id = data.get("reply_id")  # Optional: ID of the comment being replied to
    except (ValueError, KeyError):
        return JsonResponse({"message": "Invalid request data"}, status=400)

    # Validate the message
    if not message:
        return JsonResponse({"message": "Message cannot be empty"}, status=400)

    # Handle reply logic
    reply_comment = None
    if reply_id:
        try:
            reply_comment = PostComment.objects.get(id=reply_id)
            # Ensure reply belongs to the same content
            if reply_comment.content.id != content.id:
                return JsonResponse({"message": "Reply must be on the same content"}, status=400)
        except PostComment.DoesNotExist:
            return JsonResponse({"message": "Reply comment not found"}, status=404)

    # Create the new comment
    try:
        new_comment = PostComment.objects.create(
            user=user,
            content=content,
            message=message,
            replay=reply_comment  # None if not a reply
        )
        return JsonResponse({
            "message": message,
            "comment_id": new_comment.id,
            "content_id": content_id,
            "reply_id": reply_id,
            "date": new_comment.date.strftime("%Y-%m-%d %H:%M:%S")
        }, status=201)
    except ValidationError as e:
        return JsonResponse({"error": str(e)}, status=400)
