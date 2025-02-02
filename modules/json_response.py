import json

from Content_Recommender.settings import MAIN_URL


def json_contents_list(post):
    # Handle single category
    category = post.category  # Directly access the related CategoryModel object
    category_list = [{'name': category.name}] if category else []

    image = (
        f"{MAIN_URL}medias/{str(post.image)}"
        if json.dumps(str(post.image)) != "\"\""
        else "No Image"
    )

    post_data = {
        'id': post.id,
        'name': post.name,
        'created_at': post.created_at.strftime("%Y-%m-%d-%H:%M:%S"),
        'updated_at': post.updated_at.strftime("%Y-%m-%d-%H:%M:%S"),
        'category': category_list,
        'view_count': post.view_count,
        'image': image
    }
    return post_data


def json_comments_list(comment):

    comment_replay = None
    try:
        comment_replay = comment.replay.id
    except AttributeError:
        pass

    comment_data = {
            "message": comment.message,
            "comment_id": comment.id,
            "content_id": comment.content.id,
            "user_id": comment.user.id,
            "reply_id": comment_replay,
            "date": comment.date.strftime("%Y-%m-%d %H:%M:%S")
        }

    return comment_data
