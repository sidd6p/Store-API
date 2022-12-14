import os
import requests

from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt,
    get_jwt_identity,
)
from sqlalchemy import or_

from db import db
from blocklist import BLOCKLIST
from schemas import PlainUserSchema, UserSchema
from models import UserModel

blp = Blueprint("users", __name__, description="USer End-Point")

domain = os.getenv("MAILGUN_DOMAIN")
api_key = os.getenv("MAILGUN_API_KEY")


def send_simple_message(user_email, user_name):
    return requests.post(
        url=f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api", f"{api_key}"),
        data={
            "from": f"Excited User <mailgun@{domain}>",
            "to": [user_email],
            "subject": "Hello",
            "text": f"Welcome to Store-API, {user_name}",
        },
    )


@blp.route("/user")
class User(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        users = UserModel.query.all()
        return users

    @blp.arguments(UserSchema)
    @blp.response(200, UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(
            or_(
                UserModel.username == user_data["username"],
                UserModel.email == user_data["email"],
            )
        ).first():
            abort(409, messgae="User already exists")
        user = UserModel(**user_data)
        user.password = pbkdf2_sha256.hash(user.password)
        try:
            db.session.add(user)
            print("3")
            res = send_simple_message(user.email, user.username)
            print(res.content)
            db.session.commit()
            return user
        except SQLAlchemyError as e:
            abort(500, message=str(e))


@blp.route("/user/<string:user_id>")
class UserList(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(int(user_id))
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(int(user_id))
        try:
            db.session.delete(user)
            db.session.commit()
            return {"message": " User deleted"}, 200
        except SQLAlchemyError as e:
            abort(500, message=str(e))


@blp.route("/login")
class Login(MethodView):
    @blp.arguments(PlainUserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}
        abort(401, message="Invalid Credentials.")


@blp.route("/logout")
class LogOut(MethodView):
    @jwt_required()
    @blp.response(200)
    def post(self):
        jti = get_jwt().get("jti")
        BLOCKLIST.add(jti)
        return {"message": "Loged Out"}


@blp.route("/refresh")
class Refresh(MethodView):
    @jwt_required(refresh=True)
    @blp.response(200)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}
