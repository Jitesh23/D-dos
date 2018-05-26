from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from serializer.event_serializer import *
from users.errors import *
from utility.utility import *
from users.models import *

class Events(APIView):
    """
    Handle event related API's
    """
    HTTP_TOKEN = 'HTTP_TOKEN'

    def post(self, request):
        """
        Create an Event
        :param request:
        :return:
        """
        serializer = EventSerializer(data = request.data)

        if serializer.is_valid():
            utility_data = Utility()
            try:
                user_id = utility_data.decode_auth_token(request.META[self.HTTP_TOKEN])
                user_detail = GetUser(user_id)
                user = user_detail.user()
                serializer.save(users = user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except:
                return Response(INVALID_TOKEN_ERROR, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, event_id):
        """
        Update specific event details
        :param request:
        :param event_id:
        :return:
        """
        utility_data = Utility()
        try:
            user_id = utility_data.decode_auth_token(request.META[self.HTTP_TOKEN])
            user_detail = GetUser(user_id)
            user = user_detail.user()
            try:
                event = Event.objects.get(id=event_id)
                serializer = EventSerializer(event, data=request.data)

                if serializer.is_valid():
                    serializer.save(users=user)
                    return Response(serializer.data, status = status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(EVENT_DOES_NOT_FOUND, status = status.HTTP_404_NOT_FOUND)
        except:
            return Response(INVALID_TOKEN_ERROR, status=status.HTTP_401_UNAUTHORIZED)

    def get(self,request, event_id):
        """
        Return specific event details
        :param event_id:
        :return:
        """

        utility_data = Utility()
        try:
            user_id = utility_data.decode_auth_token(request.META[self.HTTP_TOKEN])
            user_detail = GetUser(user_id)
            user = user_detail.user()
            try:
                serializer = EventSerializer(Event.objects.get(id=event_id))
                return Response(serializer.data, status = status.HTTP_200_OK)
            except:
                return Response(EVENT_DOES_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(INVALID_TOKEN_ERROR, status=status.HTTP_401_UNAUTHORIZED)