from __future__ import unicode_literals

from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from errors import *
from serializer.user_serializers import *
from utility.utility import *


class UsersData(APIView):
    """
    Get, post Users instance
    """
    HTTP_TOKEN = 'HTTP_TOKEN'
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """
        Get user profile detail
        :param request:
        :return:
        """
        utility_data = Utility()
        try:
            user_id = utility_data.decode_auth_token(request.META[self.HTTP_TOKEN])
            user_data = GetUser(user_id)
            user_serializer = UserSerializer(user_data.user())

            return Response(user_serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(INVALID_TOKEN_ERROR, status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request):
        """
        Update user profile detail
        :param request:
        :return:
        """
        utility_data = Utility()
        try:
            user_id = utility_data.decode_auth_token(request.META[self.HTTP_TOKEN])
            user_data = GetUser(user_id)
            user_instance = user_data.user()

            serializer = UserSerializer(user_instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                print '------------=-------=---=-', serializer.data
                return Response(serializer.data, status = status.HTTP_200_OK)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        except:
            return Response(INVALID_TOKEN_ERROR, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request):
        """

        :param request:
        :return:
        """
        utility_data = Utility()
        try:
            user_id = utility_data.decode_auth_token(request.META[self.HTTP_TOKEN])
            user_data = GetUser(user_id)
            user_instance = user_data.user()
            user_instance.delete()
            return Response(USER_DELETED_SUCCESSFULLY,status = status.HTTP_204_NO_CONTENT)
        except:
            return Response(INVALID_TOKEN_ERROR, status=status.HTTP_401_UNAUTHORIZED)

class UserLogin(APIView):
    """
    Handle login function
    """

    EMAIL = 'email'
    PASSWORD = 'password'
    JWT_TOKEN = 'jwt_token'
    HTTP_TOKEN = 'HTTP_TOKEN'
    CONFIRM_PASSWORD = 'confirm_password'

    def post(self, request):
        try:
            user = Users.objects.get(email = request.data[self.EMAIL])
            serializer = UserSerializer(Users.objects.get(email=user.email))

            if user.password == request.data[self.PASSWORD]:

                utility_obj = Utility()
                jwt_auth_token = utility_obj.get_jwt_token(user)

                token = {self.JWT_TOKEN:jwt_auth_token}
                token.update(serializer.data)

                return Response(token, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        """
        Change the user password
        :return:
        """

        serializer = ChangePasswordSerializer(data = request.data)
        if serializer.is_valid():
            utility_data = Utility()

            try:
                user_id = utility_data.decode_auth_token(request.META[self.HTTP_TOKEN])
                user_data = GetUser(user_id)
                user_instance = user_data.user()
                if request.data[self.PASSWORD] == request.data[self.CONFIRM_PASSWORD]:
                    user_instance.password = request.data[self.PASSWORD]
                    user_instance.save()
                    user_serializer = UserSerializer(Users.objects.get(id=user_id))
                    return Response(user_serializer.data, status=status.HTTP_200_OK)
                return Response(PASSWORD_NOT_MATCHING, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(INVALID_TOKEN_ERROR, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TokenAuthentication(APIView):
    """
    Authenticate the provided token
    """
    TOKEN = 'token'

    @csrf_exempt
    def post(self, request):
        """
        Check token authentication
        :param request:
        :return:
        """

        serializer = TokenAuthenticationSerializer(data = request.data)

        if serializer.is_valid():
            utility_data = Utility()
            try:
                user_id = utility_data.decode_auth_token(request.data[self.TOKEN])
                user_serializer = UserSerializer(Users.objects.get(id = user_id))
                return Response(user_serializer.data, status=status.HTTP_200_OK)
            except:
                return Response(INVALID_TOKEN_ERROR, status = status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

