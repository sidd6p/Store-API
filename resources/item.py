from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError

from db import db
from schemas import ItemSchema, ItemUpdateSchema
from models import ItemModel

blp = Blueprint("items", __name__, description="Item End-Point")

@blp.route("/item")
class ItemList(MethodView):

    @blp.response(200, ItemSchema(many=True))
    def get(self):
        raise NotImplementedError(
            "Get all items is not implemented"
            )
    
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error while inserting item")
        return item        
    
@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            # item = ItemModel.query.filter_by(id=item_id).first()
            item = ItemModel.query.get_or_404(item_id)
            return item
        except SQLAlchemyError:
            abort(
                404, 
                message="Item not found"
            ) 

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        try:
            # item = ItemModel.query.filter_by(id=item_id).first()
            item = ItemModel.query.get_or_404(item_id)
        except SQLAlchemyError:
            abort(
                404, 
                message="Item not found"
            ) 
        else:
            raise NotImplementedError(
                "Updating not implemented"
                )
          
    
    @blp.response(200, ItemSchema)
    def delete(self, item_id):
        try:
            # item = ItemModel.query.filter_by(id=item_id).first()
            item = ItemModel.query.get_or_404(item_id)
        except SQLAlchemyError:
            abort(
                404, 
                message="Item not found"
            ) 
        else:
            raise NotImplementedError(
                "Deleting not implemented"
                )
          
