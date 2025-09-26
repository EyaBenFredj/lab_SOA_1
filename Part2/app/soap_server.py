# soap_server.py
from spyne import Application, rpc, ServiceBase, Integer, Float, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

from models import Product
from db import SessionLocal, init_db

init_db()

class InventoryService(ServiceBase):

    @rpc(Integer, Unicode, Integer, Float, _returns=Unicode)
    def CreateProduct(ctx, id, name, quantity, price):
        if quantity < 0 or price < 0:
            return "Invalid input: quantity and price must be non-negative."

        db = SessionLocal()
        product = Product(id=id, name=name, quantity=quantity, price=price)
        db.add(product)
        try:
            db.commit()
            return f"Product {name} created successfully."
        except Exception as e:
            db.rollback()
            return f"Error: {str(e)}"
        finally:
            db.close()

    @rpc(Integer, _returns=Unicode)
    def GetProduct(ctx, id):
        db = SessionLocal()
        product = db.query(Product).filter(Product.id == id).first()
        db.close()
        if product:
            return f"ID: {product.id}, Name: {product.name}, Quantity: {product.quantity}, Price: {product.price}"
        else:
            return "Product not found."

    @rpc(Integer, Unicode, Integer, Float, _returns=Unicode)
    def UpdateProduct(ctx, id, name, quantity, price):
        db = SessionLocal()
        product = db.query(Product).filter(Product.id == id).first()
        if not product:
            db.close()
            return "Product not found."

        if quantity < 0 or price < 0:
            db.close()
            return "Invalid input: quantity and price must be non-negative."

        product.name = name
        product.quantity = quantity
        product.price = price
        db.commit()
        db.close()
        return f"Product {id} updated."

    @rpc(Integer, _returns=Unicode)
    def DeleteProduct(ctx, id):
        db = SessionLocal()
        product = db.query(Product).filter(Product.id == id).first()
        if not product:
            db.close()
            return "Product not found."

        db.delete(product)
        db.commit()
        db.close()
        return f"Product {id} deleted."


# Spyne Application
application = Application(
    [InventoryService],
    tns='spyne.inventory.soap',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

wsgi_app = WsgiApplication(application)

# Run using WSGI
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    print("SOAP service running on http://localhost:8000")
    server = make_server('0.0.0.0', 8000, wsgi_app)
    server.serve_forever()
