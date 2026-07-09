from fastapi import HTTPException


def require_role(payload, roles: list[int]):

    if payload["role_id"] not in roles:
        raise HTTPException(
            status_code=403,
            detail="Permission Denied"
        )

    return True