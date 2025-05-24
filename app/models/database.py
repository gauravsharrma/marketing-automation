from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from sqlalchemy import Column, Integer, String, Boolean


Base = declarative_base()

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    hashed_password = Column(String)
    role = Column(SQLEnum(UserRole), default=UserRole.USER)
    connected_accounts_json = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    is_verified = Column(Boolean, default=False)

    # Relationships
    auth_logs = relationship("AuthLog", back_populates="user")
    prompts = relationship("Prompt", back_populates="user")
    post_logs = relationship("PostLog", back_populates="user")

class AuthLog(Base):
    __tablename__ = "auth_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    method = Column(String)  # "email_otp", "google_oauth"
    status = Column(String)  # "success", "failed"
    error_message = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationship
    user = relationship("User", back_populates="auth_logs")

class Prompt(Base):
    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    input_text = Column(String)
    blog_output = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    user = relationship("User", back_populates="prompts")
    post_logs = relationship("PostLog", back_populates="prompt")

class PostLog(Base):
    __tablename__ = "post_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    prompt_id = Column(Integer, ForeignKey("prompts.id"))
    platform = Column(String)  # "facebook", "linkedin"
    content = Column(String)
    status = Column(String)  # "pending", "published", "failed"
    error = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="post_logs")
    prompt = relationship("Prompt", back_populates="post_logs") 