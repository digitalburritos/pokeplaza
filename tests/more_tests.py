import pytest
from fastapi import HTTPException
from app.services.user_service import UserService
from app.models.user_model import User, UserRole

@pytest.mark.asyncio
async def test_get_user_by_email(db_session, user):
    """
    Tests retrieving a user by their email.
    """
    # Retrieve the user by email
    retrieved_user = await UserService.get_by_email(db_session, user.email)

    # Ensure the retrieved user matches the expected email
    assert retrieved_user is not None
    assert retrieved_user.email == user.email
    assert retrieved_user.nickname == user.nickname


@pytest.mark.asyncio
async def test_get_user_by_non_existent_email(db_session):
    """
    Tests retrieving a user by a non-existent email.
    """
    # Try retrieving a user by a non-existent email
    non_existent_email = "nonexistentuser@example.com"
    retrieved_user = await UserService.get_by_email(db_session, non_existent_email)

    # Ensure no user is found
    assert retrieved_user is None


@pytest.mark.asyncio
async def test_delete_user_exists(db_session, user):
    """
    Tests deleting a user who exists.
    """
    # Attempt to delete the user
    deletion_success = await UserService.delete(db_session, user.id)

    # Ensure the deletion was successful
    assert deletion_success is True


@pytest.mark.asyncio
async def test_delete_user_does_not_exist(db_session):
    """
    Tests attempting to delete a user who does not exist.
    """
    # Attempt to delete a non-existent user
    non_existent_user_id = "non-existent-id"
    deletion_success = await UserService.delete(db_session, non_existent_user_id)

    # Ensure the deletion failed
    assert deletion_success is False


