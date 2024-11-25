from fastapi import APIRouter, Depends, HTTPException
from src.db.models.user import User
from src.db.session import async_session_maker
from src.user.schemas import UserEdit, UserRead, UserResponse
from sqlalchemy.future import select
from fastapi_users import FastAPIUsers
from src.main import get_user_manager, auth_backend
from sqlalchemy.exc import SQLAlchemyError


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend]
)

current_user = fastapi_users.current_user()

router = APIRouter()

@router.get("/profile-{id}")
async def profile_user(id: int):
    try:
        id = int(id)
        async with async_session_maker() as async_session:
            result = await async_session.execute(select(User).where(User.id == id))
            user_record = result.scalars().first()
            user = UserResponse(user_record) if user_record else None
        return {"state": 200, "user": UserRead.from_orm(user)}
    except SQLAlchemyError as e:
            await async_session.rollback()
            raise HTTPException(status_code=500, detail="Ошибка базы данных") from e

@router.get("/my-profile")
async def my_profile(user: User = Depends(current_user)):
    try:
        async with async_session_maker() as async_session:
            result = await async_session.execute(select(User).where(User.id == user.id))
            user_record = result.scalars().first()
            user = UserResponse(user_record) if user_record else None
        return {"state": 200, "user": UserRead.from_orm(user)}
    except SQLAlchemyError as e:
            await async_session.rollback()
            raise HTTPException(status_code=500, detail="Ошибка базы данных") from e


@router.put("/my-profile-settings")
async def my_profile_settings(
    user_update: UserEdit,
    user: User = Depends(current_user)
):
    async with async_session_maker() as async_session:
        try:
            # Получаем текущего пользователя
            result = await async_session.execute(select(User).where(User.id == user.id))
            user_record = result.scalars().first()

            if not user_record:
                return {"state": 404, "detail": "Пользователь не найден"}

            # Проверяем уникальность email, если он обновляется
            if user_update.email and user_update.email != user_record.email:
                existing_user_result = await async_session.execute(
                    select(User).where(User.email == user_update.email)
                )
                existing_user = existing_user_result.scalars().first()
                if existing_user:
                    return {"state": 400, "detail": "Пользователь с таким E-mail уже существует"}

                user_record.email = user_update.email

            # Обновляем другие данные пользователя
            if user_update.name:
                user_record.name = user_update.name

            # Сохраняем изменения
            async_session.add(user_record)
            await async_session.commit()

            user = UserResponse(user_record) if user_record else None
            return {"state": 200, "user": UserRead.from_orm(user)}

        except Exception as e:
            await async_session.rollback()
            return {"state": 500, "detail": f"Произошла непредвиденная ошибка: {str(e)}"}
