from rest_framework.response import Response

from .models import ContentModel, ViewCountModel


def home(request):
    data = ContentModel.objects.all()
    context = {"contents": data}
    return Response(context)
