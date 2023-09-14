from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy

from src.auth.models import User

SECRET = "ikncode"

cookie_transport = CookieTransport(cookie_max_age=3600) # cоздание cookies

def get_jwt_strategy() -> JWTStrategy: # Стандарт доступа токена JSON
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

auth_backend = AuthenticationBackend( # Сочетание транспорта и стратегии
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    [auth_backend],
)

current_user = fastapi_users.current_user()