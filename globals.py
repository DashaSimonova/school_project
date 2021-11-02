from api import Api
from user import User, Parent, Teacher


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
    def create_api(username: str, password: str) -> None:
        Globals.api = Api(username, password)

    @staticmethod
    def create_user() -> None:
        Globals.user = User.create(Globals.api.authorize())
