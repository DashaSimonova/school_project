from api import Api
from user import User, Parent, Teacher, Administrator


class Globals:
    user: User
    api: Api

    @staticmethod
    def parent() -> Parent:
        return Globals.user

    @staticmethod
    def teacher() -> Teacher:
        return Globals.user

    @staticmethod
    def administrator() -> Administrator:
        return Globals.user

    @staticmethod
    def create_api(username: str, password: str) -> None:
        Globals.api = Api(username, password)

    @staticmethod
    def create_user() -> bool:
        json = Globals.api.authorize()
        if json is None:
            return False
        Globals.user = User.create(json)
        return True
