# utils/identity.py

import uuid
from fastapi import Request, Response


def get_or_set_anon_id(
        request: Request, 
        response: Response
        ) -> str:
    anon_id = request.cookies.get("anon_id")

    if not anon_id:
        anon_id = str(uuid.uuid4())
        response.set_cookie(
            key="anon_id",
            value=anon_id,
            max_age=60 * 60 * 24 * 30,
            httponly=True
        )

    return anon_id