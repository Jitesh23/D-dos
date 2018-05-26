import json
import jwt

from users.models import Users


class Utility():
    """
    JWT token
    """
    SECRET_KEY = 'SECRET_KEY'
    ID = 'id'
    EMAIL = 'email'
    TOKEN = 'token'

    def __init__(self):
        pass

    def get_jwt_token(self,user):
        """
        Create JWT token
        :param user:
        :return jwt_token:
        """
        payload = {
            self.ID: user.id,
            self.EMAIL: user.email,
        }
        jwt_token = {self.TOKEN: jwt.encode(payload, self.SECRET_KEY)}
        return json.dumps(jwt_token)

    def decode_auth_token(self, token):
        """
        Validate JWT token
        :param token:
        :return:
        """
        try:
            payload = jwt.decode(token, self.SECRET_KEY)
            user_id = payload[self.ID]
            return user_id
        except jwt.DecodeError as error:
            return error

class GetUser():
    """
    Return User object
    """
    def __init__(self, user_id):
        """
        :param user_id:
         :return user_object
        """
        self.user_data = Users.objects.get(id=user_id)

    def user(self):
        return self.user_data