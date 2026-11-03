import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv


load_dotenv()


JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

JWT_ALGORITHM = "HS256"

JWT_EXPIRATION_MINUTES = 60


def create_access_token(user_id):
    expiration_time = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=JWT_EXPIRATION_MINUTES
        )
    )

    payload = {
        "sub": str(user_id),
        "exp": expiration_time
    }

    token = jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )

    return token

def verify_access_token(token):
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            return None

        return int(user_id)

    except jwt.InvalidTokenError:
        return None