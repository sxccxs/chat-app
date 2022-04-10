from fastapi import status

from schemas import payloads, model_schemas as schemas

docs = {
    "login": {
        status.HTTP_200_OK: {
            "description": "Successful Login",
            "model": payloads.Tokens
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found",
            "content": {
                "application/json": {
                    "example": {"detail": "User with given credentials was not found."}
                }
            }
        }
    },
    "refresh": {
        status.HTTP_200_OK: {
            "description": "Successful Refresh",
            "model": payloads.Tokens,
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid Token",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid token provided."}
                }
            }
        }
    },
    "register": {
        status.HTTP_204_NO_CONTENT: {
            "description": "Successful Registration",
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid Data provided",
            "content": {
                "application/json": {
                    "example": {"detail": "Email is in invalid format."}
                }
            }
        }
    },
    "activate": {
        status.HTTP_204_NO_CONTENT: {
            "description": "Successful Account Activation",
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid token or uid provided",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid uidb64 or token"}
                }
            }
        }
    },
    "check_email_exists": {
        status.HTTP_200_OK: {
            "description": "Email exists",
            "content": None
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Email does not exist",
        }
    },
    "me": {
        status.HTTP_200_OK: {
            "description": "Successful Response",
            "model": schemas.UserOut
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Not Authorized",
            "content": {
                "application/json": {
                    "example": {"detail": "Not authenticated"}
                }
            }
        }
    },
}
