from datetime import datetime, timedelta, timezone

import jwt
import pytest

from app.core.config import settings
from app.core.security import (
    hash_password,
    verify_password, 
    create_access_token, 
    decode_token,
    create_refresh_token,
    )


def test_hash_password():
    password = "poiu!!"
    
    hashed = hash_password(password)
    
    assert hashed != password
    assert hashed.startswith("$argon2")
    
def test_verify_password():
    password = "pepe"
    
    hashed = hash_password(password)
    
    assert verify_password(password, hashed)
    
def test_verify_wrong_password():
    password = "papi"
    wrong_password = "popo"
    
    hashed = hash_password(password)
    
    assert not verify_password(wrong_password, hashed)
    
def test_create_access_token():
    user_id = 11
    
    token = create_access_token(user_id)
    
    assert token is not None
    assert isinstance(token, str)
    
    payload = decode_token(token)
    
    assert payload["sub"] == "11"
    assert payload["type"] == "access"
    
def test_refresh_token():
    user_id = 11
    
    token = create_refresh_token(user_id)
    
    assert token is not None
    assert isinstance(token, str)
    
    payload = decode_token(token)
    
    assert payload["sub"] == "11"
    assert payload["type"] == "refresh"
    
def test_expired_token_is_rejected():
    expire = datetime.now(timezone.utc) - timedelta(seconds=1)
    
    payload = {
        "sub": "11",
        "type": "access",
        "exp": expire,        
    }
    
    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    
    with pytest.raises(jwt.ExpiredSignatureError):
        decode_token(token)
        
def test_expired_token_debug():
    expire = datetime.now(timezone.utc) - timedelta(seconds=1)
    
    payload = {
        "sub": "11",
        "type": "access",
        "exp": expire,  
    }
    
    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    
    print(f"\n Token expired : {token}")
    
    with pytest.raises(jwt.ExpiredSignatureError) as error:
        decode_token(token)
        
    print(f"Exception received :  {type(error.value).__name__}")
    
def test_tampered_token_is_rejected():
    user_id = 11
    
    # Creatin a real token
    token = create_access_token(user_id)
    
    # Spliting JWT
    header, payload, signature = token.split(".")
    
    # We intentionally modify the payload
    import base64
    import json
    
    padding = "=" * (len(payload) % 4)
    
    decoded_payload = json.loads(
        base64.urlsafe_b64decode(
            payload + padding
        )
    )
    
    # The hacker tries to pretend to be user 99
    decoded_payload["sub"] = "99"
    
    # We rebuild the tampered payload
    new_payload = base64.urlsafe_b64encode(
        json.dumps(
            decoded_payload,
            separators=(",", ":")
        ).encode()
    ).decode().rstrip("=")
    
    tampered_token = (
        f"{header}.{new_payload}.{signature}"
    )
    
    # The backend should refuse the token
    with pytest.raises(jwt.InvalidSignatureError):
        decode_token(tampered_token)
        
def test_token_signed_with_wrong_secret_is_rejected():
    payload = {
        "sub": "11",
        "typr": "access",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=15),
    }
    
    fake_token = jwt.encode(
        payload,
        "secret-de-l-attaquant-secret-de-l-attaquant",
        algorithm="HS256",
    )

    with pytest.raises(jwt.InvalidSignatureError):
        decode_token(fake_token)