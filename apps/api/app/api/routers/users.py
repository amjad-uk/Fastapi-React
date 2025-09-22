from fastapi import APIRouter, Depends, Query, Path
from ...schemas.user import UserOut, UserCreate, UserUpdate
from ...services.user_service import UserService
from ...api.deps import get_user_service

router = APIRouter(tags=["users"])

@router.get("/users", response_model=list[UserOut])
async def list_users(svc: UserService = Depends(get_user_service)):
    return await svc.list_users()

@router.post("/users/create", response_model=UserOut, status_code=201)
async def create_user(payload: UserCreate, svc: UserService = Depends(get_user_service)):
    return await svc.create_user(payload.model_dump())

@router.put("/user/{id}", response_model=UserOut)
async def update_user(id: int = Path(..., ge=1), payload: UserUpdate | None = None, svc: UserService = Depends(get_user_service)):
    patch = payload.model_dump(exclude_unset=True) if payload else {}
    return await svc.update_user(id, patch)

@router.delete("/user", status_code=204)
async def delete_user(id: int = Query(..., description="User ID"), svc: UserService = Depends(get_user_service)):
    await svc.delete_user(id)
    return None
