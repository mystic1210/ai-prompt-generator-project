"""Unit tests for backend services"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.services.user_service import UserService
from app.services.prompt_service import PromptService
from app.schemas.user import UserCreate
from app.schemas.prompt import PromptCreate

# Test database
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def db():
    """Get test database session"""
    connection = engine.connect()
    transaction = connection.begin()
    db_session = TestingSessionLocal(bind=connection)

    yield db_session

    db_session.close()
    transaction.rollback()
    connection.close()


def test_create_user(db):
    """Test user creation"""
    user_data = UserCreate(
        email="test@example.com",
        username="testuser",
        full_name="Test User",
        password="password123"
    )
    user = UserService.create_user(db, user_data)
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert user.is_active is True


def test_get_user_by_email(db):
    """Test getting user by email"""
    user_data = UserCreate(
        email="test@example.com",
        username="testuser",
        full_name="Test User",
        password="password123"
    )
    created_user = UserService.create_user(db, user_data)
    retrieved_user = UserService.get_user_by_email(db, "test@example.com")
    assert retrieved_user.id == created_user.id


def test_verify_password():
    """Test password verification"""
    password = "password123"
    hashed = UserService.hash_password(password)
    assert UserService.verify_password(password, hashed) is True
    assert UserService.verify_password("wrongpassword", hashed) is False


def test_create_prompt(db):
    """Test prompt creation"""
    # Create user first
    user_data = UserCreate(
        email="test@example.com",
        username="testuser",
        full_name="Test User",
        password="password123"
    )
    user = UserService.create_user(db, user_data)

    # Create prompt
    prompt_data = PromptCreate(
        title="Test Prompt",
        description="Test Description",
        content="This is test content",
        topic="Python",
        audience="school",
        skill_level="beginner",
        format="text",
        category="Programming"
    )
    prompt = PromptService.create_prompt(db, user.id, prompt_data)
    assert prompt.title == "Test Prompt"
    assert prompt.creator_id == user.id


def test_get_user_prompts(db):
    """Test getting user prompts"""
    # Create user
    user_data = UserCreate(
        email="test@example.com",
        username="testuser",
        full_name="Test User",
        password="password123"
    )
    user = UserService.create_user(db, user_data)

    # Create prompts
    for i in range(3):
        prompt_data = PromptCreate(
            title=f"Test Prompt {i}",
            description=f"Test Description {i}",
            content="This is test content",
            topic="Python",
            audience="school",
            skill_level="beginner",
            format="text",
            category="Programming"
        )
        PromptService.create_prompt(db, user.id, prompt_data)

    # Get prompts
    prompts = PromptService.get_user_prompts(db, user.id)
    assert len(prompts) == 3
