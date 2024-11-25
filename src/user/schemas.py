from pydantic import BaseModel, Field
from typing import Any

# Схема для создания пользователя
class UserCreate(BaseModel):
    name: str = Field(..., description="Имя в формате My Nick-Name", example="My Nick-Name")
    password: str = Field(..., description="Пароль в формате QwErty123", example="My Hard1 Pas$word")
    email: str = Field(..., description="Почта в формате Email@email.com", example="my-email@gmail.com")

    def create_update_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "password": self.password,
            "email": self.email,
        }

# Схема для ответа на запрос о пользователе
class UserRead(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True
        from_attributes = True
        
# Схема для обновления пользователя
class UserEdit(BaseModel):
    name: str
    email: str

# Класс для ответа
class UserResponse:
    def __init__(self, user: Any):
        # Преобразование SQLAlchemy объекта в Pydantic модель
        self.id = user.id
        self.name = user.name
        self.email = user.email
