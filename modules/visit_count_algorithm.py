from django.db.models import Sum
from ContentApp.models import ViewCountModel, ContentModel
import random
from django.db.models import Count


def get_user_top_categories(user):
    # Get the user activities, and the category of that posts
    # sum the view count of each category
    # order them with most views
    category_views = (
        ViewCountModel.objects.filter(user=user)
        .values('content__category')  # Group by category
        .annotate(total_views=Sum('view_count'))  # Aggregate view counts
        .order_by('-total_views')  # Sort by views in descending order
    )
    # Return categories ranked by total views
    return [entry['content__category'] for entry in category_views]


def get_ordered_posts(user):
    # Get the user's top categories
    top_categories = get_user_top_categories(user)

    # Fetch posts grouped by category
    categorized_posts = {}
    for category_id in top_categories:
        # get the List of post of a Category
        categorized_posts[category_id] = list(
            ContentModel.objects.filter(category_id=category_id)
        )

    # Interleave posts from top categories to create a dynamic feed
    ordered_posts = []
    while any(categorized_posts.values()):
        for category_id in top_categories[:3]:  # Limit to top 3 categories
            if categorized_posts.get(category_id):
                ordered_posts.append(categorized_posts[category_id].pop(0))

    # Shuffle top-category posts for dynamic behavior
    random.shuffle(ordered_posts)

    # Fetch posts from other categories not in the top 3
    other_posts = list(
        ContentModel.objects.exclude(category_id__in=top_categories[:3])
        .annotate(calculated_view_count=Count('viewcountmodel'))
        .order_by('-calculated_view_count')
    )
    random.shuffle(other_posts)  # Shuffle non-top posts

    # Combine top posts and non-top posts with a pattern
    all_posts = []
    top_post_index = 0
    non_top_post_index = 0

    while top_post_index < len(ordered_posts) or non_top_post_index < len(other_posts):
        random_number = random.randrange(3, 7)
        # Add up to 5 posts from top posts
        for post in range(random_number):
            if top_post_index < len(ordered_posts):
                all_posts.append(ordered_posts[top_post_index])
                top_post_index += 1
        # Add 1 post from non-top posts
        if non_top_post_index < len(other_posts):
            all_posts.append(other_posts[non_top_post_index])
            non_top_post_index += 1

    # Return the balanced ordered posts
    return all_posts
