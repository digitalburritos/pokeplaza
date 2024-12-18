from fastapi import APIRouter, Depends, HTTPException
from app.models.user_model import User
from app.services.auth_service import AuthService
from app.database import get_db
from app.schemas.user_schemas import UserCreate, UserUpdate, UserResponse, LoginRequest, UserListResponse, ErrorResponse
from app.schemas.pagination_schema import EnhancedPagination
from sqlalchemy.orm import Session
from uuid import uuid4

router = APIRouter()

# Register a new user
@router.post("/register", response_model=UserResponse, responses={400: {"model": ErrorResponse}})
async def register_user(user_create: UserCreate, db: Session = Depends(get_db), auth_service: AuthService = Depends()):
    # Check if the username already exists
    existing_user = db.query(User).filter(User.username == user_create.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Hash the user's password
    hashed_password = auth_service.hash_password(user_create.password)
    
    # Create new user
    new_user = User(
        username=user_create.username,
        email=user_create.email,
        first_name=user_create.first_name,
        last_name=user_create.last_name,
        trainer_level=user_create.trainer_level,
        hashed_password=hashed_password,
    )
    
    # Save user to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# Login user and generate JWT token
@router.post("/login", response_model=LoginRequest, responses={401: {"model": ErrorResponse}})
async def login_user(login_request: LoginRequest, db: Session = Depends(get_db), auth_service: AuthService = Depends()):
    user = db.query(User).filter(User.username == login_request.username).first()
    
    if not user or not auth_service.verify_password(login_request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create the access token
    access_token = auth_service.create_access_token(user.id, user.trainer_level)
    return {"access_token": access_token, "token_type": "bearer"}


# Update user information
@router.put("/update/{user_id}", response_model=UserResponse, responses={404: {"model": ErrorResponse}})
async def update_user(user_id: uuid.UUID, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update the user fields
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    return user


# List users with pagination
@router.get("/", response_model=EnhancedPagination, responses={404: {"model": ErrorResponse}})
async def list_users(page: int = 1, per_page: int = 10, db: Session = Depends(get_db)):
    total_users = db.query(User).count()
    users = db.query(User).offset((page - 1) * per_page).limit(per_page).all()
    
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    
    pagination = EnhancedPagination(page=page, per_page=per_page, total_items=total_users, total_pages=(total_users // per_page) + 1)
    
    for user in users:
        pagination.add_link("self", f"/users/{user.id}")
    
    pagination.items = users
    return pagination


# Get specific user by ID
@router.get("/{user_id}", response_model=UserResponse, responses={404: {"model": ErrorResponse}})
async def get_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user


# Delete user by ID
@router.delete("/delete/{user_id}", responses={404: {"model": ErrorResponse}})
async def delete_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"msg": "User deleted successfully"}

