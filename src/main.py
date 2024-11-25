from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from src.auth.auth import auth_backend
from src.user.schemas import UserCreate, UserRead
from src.auth.manager import get_user_manager
from src.db.models.user import User
from src.settings import settings
from src.user.router_user import router as router_users
from fastapi.middleware.cors import CORSMiddleware
from fastapi_users.router import get_reset_password_router
from src.auth.manager import UserManager

app = FastAPI(
        title = settings.PROJECT_NAME,
        version = settings.PROJECT_VERSION
    )

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend]
)

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt"
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth"
)
app.include_router(
    router_users,
    prefix="/user"
)