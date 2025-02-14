from flask_restx import Api

api = Api(
    title="To-Do Management API",
    version="1.0",
    description="API for managing user authentication and to-do items.",
    authorizations={
        "basic": {
            "type": "basic",
            "description": "Basic Authentication - Provide `username:password` in Base64.",
        },
        "jwt": {
            "type": "apiKey",  # JWT
            "in": "header",  # find the key in the header
            "name": "Authorization",  # in the header but under the Authorization section
            "description": "JWT Authentication - Use `Bearer <JWT>` in the header.",
        },
    },
)
