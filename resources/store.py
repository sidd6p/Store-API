from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from db import db
from schemas import StoreSchema
from models import StoreModel

blp = Blueprint("stores", __name__, description="Store End-Points")

@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
            raise NotImplementedError(
            "Get all store not implemented"
        )

    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        # try:
        db.session.add(store)
        db.session.commit()
        # except IntegrityError:
        #     abort(
        #         400,
        #         message="Store with same name already exists"
        #     )
        # except SQLAlchemyError:
        #     abort(
        #         500, 
        #         message="Error while inserting item"
        #     )
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

    @blp.response(200, StoreSchema)
    def delete(self, store_id):
        try:
            store = StoreModel.query.get_or_404(store_id)
        except SQLAlchemyError:
            abort(
                404,
                "Store Does not exists"
            )
        else:
            raise NotImplementedError(
                "Delete Store not implemented"
            )