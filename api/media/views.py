import json

from django.http import JsonResponse
from django.utils.decorators import (decorator_from_middleware,
                                     decorator_from_middleware_with_args)
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view

from ..constants.media_types import IMAGE, AUDIO, VIDEO
from ..middleware.auth_strategy import AuthStrategyMiddleware
from ..user.models import EndUser
from .models import Media
from .serializers import MediaSerializer

# Create your views here.


@csrf_exempt
@api_view(['GET'])
@decorator_from_middleware(AuthStrategyMiddleware)
def get_all_medias_of_logged_user(request):
    try:
        medias = Media.objects.filter(owner__id=request.user.id).all()
        return JsonResponse({
            'success': True,
            'message': 'All medias of logged in user',
            'medias': MediaSerializer(medias, many=True).data
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(['GET'])
def get_all_medias(request):
    try:
        medias = Media.objects.all()
        return JsonResponse({
            'success': True,
            'message': 'All medias from the portal',
            'medias': MediaSerializer(medias, many=True).data
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(['PUT'])
@decorator_from_middleware(AuthStrategyMiddleware)
def create_new_media(request):
    data = request.POST
    try:
        caption = data['caption']
        file = request.FILES['file']
        type = data['type']
        if 'type' in data:
            if data['type'] not in (IMAGE, AUDIO, VIDEO):
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid value of type property'
                }, status=status.HTTP_400_BAD_REQUEST)
            type = data['type']
        endUser = request.user
        new_media = Media.objects.create(
            file=file, caption=caption, type=type, owner=endUser)
        return JsonResponse({
            'success': True,
            'message': 'Successfully created media',
            'media': MediaSerializer(new_media).data
        }, status=status.HTTP_201_CREATED)
    except KeyError:
        return JsonResponse({
            'success': False,
            'message': 'Media body parameter not found'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(['PATCH'])
@decorator_from_middleware(AuthStrategyMiddleware)
def edit_existing_media(request, media_id):
    data = request.POST
    try:
        existing_media = Media.objects.get(
            id=media_id, owner__id=request.user.id)
        if 'file' in request.FILES:
            existing_media.file = request.FILES['file']
        if 'caption' in data:
            existing_media.caption = data['caption']
        if 'type' in data:
            if data['type'] not in (IMAGE, AUDIO, VIDEO):
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid value of type property'
                }, status=status.HTTP_400_BAD_REQUEST)
            existing_media.type = data['type']
        existing_media.save()
        return JsonResponse({
            'success': True,
            'message': 'Successfully updated media',
            'media': MediaSerializer(existing_media).data
        }, status=status.HTTP_200_OK)
    except Media.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Media does not exist'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(['DELETE'])
@decorator_from_middleware(AuthStrategyMiddleware)
def delete_existing_media(request, media_id):
    try:
        existing_media = Media.objects.get(
            id=media_id, owner__id=request.user.id)
        existing_media.delete()
        return JsonResponse({
            'success': True,
            'message': 'Successfully deleted media',
        }, status=status.HTTP_200_OK)
    except Media.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Media does not exist'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)
