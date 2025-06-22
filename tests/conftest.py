import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.domain.models.list_task import ListTask
from src.domain.models.task import Task
from src.domain.models.user import User
from src.infrastructure.data.db import get_db
from src.infrastructure.data.db_methods import Base
from src.infrastructure.security.password_hasher import PasswordHasher
from src.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(setup_test_db):
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session):
    user = User(
        email="test@example.com",
        hashed_password=PasswordHasher.hash_password("testpassword123"),
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_list_task(db_session, test_user):
    list_task = ListTask(title="Test List", description="Test Description")
    db_session.add(list_task)
    db_session.commit()
    db_session.refresh(list_task)
    return list_task


@pytest.fixture
def test_task(db_session, test_user, test_list_task):
    task = Task(
        title="Test Task",
        description="Test Task Description",
        status="Pending",
        priority="Medium",
        completeness="0%",
        id_user=test_user.id_user,
        id_list_task=test_list_task.id_list_task,
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    return task


@pytest.fixture
def auth_headers(test_user):
    from datetime import datetime, timedelta

    from jose import jwt

    from configs import settings

    expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRATION_TIME)
    payload = {"sub": test_user.email, "exp": expire}
    token = jwt.encode(
        payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def mock_resend_service():
    with pytest.mock.patch(
        "src.infrastructure.services.resend.resend_service.send_email"
    ) as mock:
        mock.return_value = {"id": "test-email-id"}
        yield mock


@pytest.fixture(autouse=True)
def setup_test_env(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///./test.db")
    monkeypatch.setenv("JWT_SECRET_KEY", "test-secret-key-for-testing-only")
    monkeypatch.setenv("JWT_ALGORITHM", "HS256")
    monkeypatch.setenv("JWT_EXPIRATION_TIME", "30")
    monkeypatch.setenv("RESEND_API_KEY", "test-resend-api-key")
    monkeypatch.setenv("RESEND_FROM_EMAIL", "test@example.com")
