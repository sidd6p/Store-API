from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt

from db import db
from schemas import StoreSchema
from models import ItemModel, StoreModel

blp = Blueprint("stores", __name__, description="Store End-Points")

@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @jwt_required()
    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="Store with same name already exists"
            )
        except SQLAlchemyError:
            abort(
                500, 
                message="Error while inserting item"
            )
        return store


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        try:
            store = StoreModel.query.get_or_404(store_id)
            return store
        except SQLAlchemyError:
            abort(
                404,
                "Store Not found"
            )

    @jwt_required()
    @blp.response(200, StoreSchema)
    def delete(self, store_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(
                401,
                message="Not Admin"
            )
        try:
            store = StoreModel.query.get_or_404(store_id)
            items = ItemModel.query.filter_by(store_id=int(store_id)).all()
            for item in items:
                db.session.delete(item)
            db.session.delete(store)
            db.session.commit()
            return {"message": "Store deleted"}
        except SQLAlchemyError:
            abort(
                404,
                "Store Does not exists"
            )
