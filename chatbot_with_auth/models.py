from typing import Optional,List 
from sqlmodel import Field,SQLModel,Relationship
from enum import Enum
from sqlalchemy import DateTime
from datetime import datetime,timedelta,UTC
from pydantic import EmailStr

class Role(str,Enum):
    USER = "user"
    ADMIN = "admin"

class User(SQLModel,table = True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None,primary_key=True)
    username: str = Field(unique= True,index= True)
    email: EmailStr = Field(unique= True)
    hashed_password: str 
    disabled: bool = False

    is_verified: bool = Field(default=False, nullable=False)
    verification_code: Optional[str] = Field(default=None, nullable=True)
    verification_code_expires_at: Optional[datetime] = Field(default=None, nullable=True)

    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(UTC), nullable=True
    )
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(UTC), nullable=True,
        sa_column_kwargs={"onupdate": lambda: datetime.now(UTC)}
    )
class UserCreate(SQLModel):
    username: str
    password: str
    email: EmailStr
    full_name: Optional[str] = None

class UserRead(SQLModel):
    id: int
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    disabled: bool
    role: Role
    is_verified: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class Forgot_password_request(SQLModel):
    email:EmailStr

class Reset_password_request(SQLModel):
    token : str
    new_password: str

class VerifyEmailRequest(SQLModel):
    email: EmailStr
    otp: str
    
class Token(SQLModel):
    access_token: str
    token_type: str

class Token_data(SQLModel):
    username: Optional[str] = None




    