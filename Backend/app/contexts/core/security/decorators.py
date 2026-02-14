# app/contexts/core/security/decorators.py
from functools import wraps
from flask import request, jsonify, current_app, g
import jwt


def _get_bearer_token() -> str | None:
    auth = request.headers.get("Authorization", "")
    if auth.lower().startswith("bearer "):
        return auth.split(" ", 1)[1].strip()
    return None


def require_auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        token = _get_bearer_token()
        if not token:
            return jsonify({"message": "Missing Bearer token"}), 401

        try:
            secret = current_app.config.get("JWT_SECRET_KEY")
            if not secret:
                return jsonify({"message": "Server misconfigured: JWT_SECRET_KEY missing"}), 500

            payload = jwt.decode(token, secret, algorithms=["HS256"])
            # store for later use in routes
            g.user = payload
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401
        except Exception as e:
            return jsonify({"message": "Auth error", "details": str(e)}), 401

        return fn(*args, **kwargs)

    return wrapper


def require_role(*allowed_roles: str):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user = getattr(g, "user", None)
            if not user:
                return jsonify({"message": "Unauthenticated"}), 401

            # allow either "role": "ADMIN" or "roles": ["ADMIN","HR"]
            role = user.get("role")
            roles = user.get("roles") or ([role] if role else [])

            if not any(r in allowed_roles for r in roles):
                return jsonify({"message": "Forbidden"}), 403

            return fn(*args, **kwargs)

        return wrapper

    return decorator