from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

bcrypt = Bcrypt()
jwt = JWTManager()


# Without these, an expired/invalid token escapes as an unhandled exception and
# Flask returns 500. The client's refresh-on-401 interceptor then never fires and
# the user gets bounced to the login page. These make the auth failures 401 so the
# client can refresh and retry transparently.

@jwt.expired_token_loader
def _expired_token(jwt_header, jwt_payload):
    return {"error": "Token has expired", "code": "token_expired"}, 401


@jwt.invalid_token_loader
def _invalid_token(reason):
    return {"error": "Invalid token", "code": "invalid_token", "detail": str(reason)}, 401


@jwt.unauthorized_loader
def _missing_token(reason):
    return {"error": "Authorization required", "code": "authorization_required", "detail": str(reason)}, 401


@jwt.needs_fresh_token_loader
def _needs_fresh(jwt_header, jwt_payload):
    return {"error": "Fresh token required", "code": "fresh_token_required"}, 401


@jwt.revoked_token_loader
def _revoked(jwt_header, jwt_payload):
    return {"error": "Token has been revoked", "code": "token_revoked"}, 401
