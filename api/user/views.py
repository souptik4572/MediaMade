import json
from datetime import datetime, timedelta

import bcrypt
import jwt
import pytz
from decouple import config
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view

from .models import EndUser

utc = pytz.UTC

ACCESS_SECRET_TOKEN = config('ACCESS_SECRET_TOKEN')
BCRYPT_SALT = int(config('BCRYPT_SALT'))


def hash_item(item, is_password=True):
    item = item.encode('utf-8') if is_password else item
    return str(bcrypt.hashpw(
        item, bcrypt.gensalt(BCRYPT_SALT))).replace("b'", "").replace("'", "")


def check_password(given_password, actual_password):
    return bcrypt.checkpw(given_password.encode('utf-8'), actual_password.encode('utf-8'))

# Create your views here.


@csrf_exempt
@api_view(['POST'])
def login_user(request):
    data = json.loads(request.body)
    try:
        email = data['email']
        password = data['password']
        endUser = EndUser.objects.get(email=email)
        if not check_password(password, endUser.password):
            return JsonResponse({
                'success': False,
                'message': 'Passwords do not match'
            }, status=status.HTTP_401_UNAUTHORIZED)
        encoded_token = jwt.encode({
            'id': endUser.id,
            'exp': datetime.now() + timedelta(days=1)
        }, ACCESS_SECRET_TOKEN, algorithm='HS512')
        return JsonResponse({
            'success': True,
            'message': 'successfully logged in',
            'token': encoded_token
        }, status=status.HTTP_200_OK)
    except KeyError:
        return JsonResponse({
            'success': False,
            'message': 'Either email or password is missing'
        }, status=status.HTTP_400_BAD_REQUEST)
    except EndUser.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'User with given email does not exist'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(['PUT'])
def register_end_user(request):
    data = json.loads(request.body)
    try:
        name = data['name']
        email = data['email']
        password = data['password']
        hashed_password = hash_item(password)
        endUser = EndUser.objects.create(
            name=name, email=email,  password=hashed_password)
        return JsonResponse({
            'success': True,
            'message': 'Successfully registered end user',
        }, status=status.HTTP_201_CREATED)
    except KeyError:
        return JsonResponse({
            'success': False,
            'message': 'Please provide all data'
        }, status=status.HTTP_400_BAD_REQUEST)
    except IntegrityError:
        return JsonResponse({
            'success': False,
            'message': 'An user with same email already exists'
        }, status=status.HTTP_403_FORBIDDEN)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)
