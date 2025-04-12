import jwt
import json
from datetime import datetime, timedelta
from .keys import load_keys
from gqlauth.core.utils import app_settings
from gqlauth.jwt.types_ import TokenPayloadType, TokenType


def encode_jwt_dynamic(user) -> TokenType:
    keys_data = load_keys()
    private_key = keys_data["private_key"]
    current_kid = keys_data["current_kid"]

    # Use JWT_PAYLOAD_PK dynamically as the key
    user_pk = app_settings.JWT_PAYLOAD_PK.python_name
    pk_field = {user_pk: getattr(user, user_pk)}

    payload = TokenPayloadType(**pk_field)

    # Construct your full payload
    custom_payload = {
        "user_id": user.id,
        "role": user.role,
        "key_version": current_kid,
        "exp": datetime.utcnow() + timedelta(days=7),
        "iat": datetime.utcnow(),
        "payload": json.dumps(payload.as_dict(), sort_keys=True),
    }

    import logging
    logging.debug(f"JWT payload: {payload}")

    token = jwt.encode(
        payload=custom_payload,
        key=private_key,
        algorithm=app_settings.JWT_ALGORITHM,
        headers={"kid": current_kid}
    )

    return TokenType(token=token, payload=payload)