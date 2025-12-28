from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, HTTPException
from src.domain.user import User
from src.repository.user_repository import UserRepository
from src.router.schemas import UserCreate, UserResponse


router = APIRouter(prefix="/users", tags=["users"])
user_repository = UserRepository()


@router.post("", response_model=UserResponse, status_code=201)
async def create_user(user_data: UserCreate):
    now = datetime.now()
    user = User(
        id=str(uuid4()),
        name=user_data.name,
        created_at=now,
        updated_at=now
    )
    created_user = await user_repository.create(user)
    return UserResponse(
        id=created_user.id,
        name=created_user.name,
        created_at=created_user.created_at,
        updated_at=created_user.updated_at
    )


@router.get("", response_model=list[UserResponse])
async def list_users():
    users = await user_repository.find_all()
    return [
        UserResponse(
            id=user.id,
            name=user.name,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
        for user in users
    ]


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    user = await user_repository.find_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(
        id=user.id,
        name=user.name,
        created_at=user.created_at,
        updated_at=user.updated_at
    )
