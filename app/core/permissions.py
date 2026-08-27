from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependency import get_current_user
from app.models.user import Userdata


def require_admin(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Requires the authenticated user to have an admin role (role_id == 1)."""
    if isinstance(current_user, dict):
        user_id = int(current_user.get("sub", 0))
        user = db.query(Userdata).filter(Userdata.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )
    else:
        user = current_user

    if user.role_id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    return user


def require_permission(permission: str):
    """
    Dependency factory to check if the current user has the required permission
    via their role (evaluated using code-level relationships).
    """
    def permission_checker(
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db),
    ):
        if isinstance(current_user, dict):
            user_id = int(current_user.get("sub", 0))
            user = db.query(Userdata).filter(Userdata.id == user_id).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found",
                )
        else:
            user = current_user

        if not user.role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No role assigned to user",
            )

        user_permissions = {
            perm.name
            for perm in user.role.permissions
            if perm.status == 1
        }

        if permission not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied",
            )

        return user

    return permission_checker