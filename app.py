from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import request 


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Password+@deneme.postgres.database.azure.com:5432/postgres'
db = SQLAlchemy(app)
with app.app_context():
    db.reflect()
class Product(db.Model):
    __table__ = db.Model.metadata.tables['product']  
class Orders(db.Model):
    __table__ = db.Model.metadata.tables['orders']
class Deliveries(db.Model):
    __table__ = db.Model.metadata.tables ['delivery']
class Customer (db.Model):
     __table__=db.Model.metadata.tables['customer']
class OrdersDetail(db.Model):
     __table__=db.Model.metadata.tables["ordersdetail"]
class Shipping (db.Model):
     __table__=db.Model.metadata.tables["shipping"]
class  Categories(db.Model):
    __table__=db.Model.metadata.tables["category"]


@app.route('/api/products', methods=['GET'])
def get_products():
    products =Product.query.all()
    return jsonify({'products':[{'id': p.product_id, 'name': p.product_name,'category_id':p.category_id ,'added_date':p.creation_date,'price': p.price ,'stock':p.stock_quantity,'decription':p.description} for p in products]})

@app.route ('/api/products',methods=['POST'])
def add_product():
    try:
        data=request.json
        new_product=Product(
            product_name=data.get('isim'),
            category_id=data.get('kategori_id'),
            creation_date=data.get('eklenme_tarihi'),
            price=data.get('fiyat'),
            stock_quantity=data.get('stok'),
            description=data.get('açıklama')
        )
        db.session.add(new_product)
        db.session.commit()
        
        return jsonify ({'success':True,'message':'Ürün eklendi'})
    except  Exception as e:
        db.session.rollback()
        return jsonify ({'error':str(e),'success':False})
    
@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Ürün bulunamadı.', 'success': False}), 404 
        OrdersDetail.query.filter_by(product_id=product_id).delete()
        db.session.delete(product)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Ürün başarıyla silindi.'})
    

    except  Exception as e:
        db.session.rollback()
        return jsonify ({'error':str(e),'success':False})
    
@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Ürün bulunamadı.', 'success': False}), 404
        data = request.json
        product.product_name = data.get('isim', product.product_name)
        product.category_id = data.get('kategori_id', product.category_id)
        product.creation_date = data.get('eklenme_tarihi', product.creation_date)
        product.price = data.get('fiyat', product.price)
        product.stock_quantity = data.get('stok', product.stock_quantity)
        product.description = data.get('açıklama', product.description)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Ürün başarıyla güncellendi.'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e), 'success': False})
    
@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = Categories.query.all()
    return jsonify({'categories': [{'id': c.category_id, 'name': c.category_name, 'type':c.category_type, 'description': c.description} for c in categories]})

@app.route('/api/categories', methods=['POST'])
def add_category():
    try:
        data = request.json
        new_category = Categories(
            category_id=data.get('kategori_id'),
            category_name=data.get('kategori_adi'),
            category_type=data.get('kategori_türü'),
            description=data.get('aciklama')
        )
        db.session.add(new_category)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Kategori eklendi'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e), 'success': False})

@app.route('/api/categories/<int:category_id>', methods=['DELETE'])
def delete_categories(category_id):
    try:
        category = Categories.query.get(category_id)
        
        if not category:
            return jsonify({'error': 'Kategori bulunamadı.', 'success': False}), 404

        db.session.delete(category)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Kategori başarıyla silindi.'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e), 'success': False})

@app.route('/api/categories/<int:category_id>', methods=['PUT'])
def update_categories(category_id):

    try:
        category = Categories.query.get(category_id)
        if not category:
            return jsonify({'error': 'Kategori bulunamadı.', 'success': False}), 404
        data = request.json
        category.category_name = data.get('kategori_adi', category.category_name)
        category.category_type = data.get('kategori_türü', category.category_type)
        category.description = data.get('açıklama', category.description)
        
        db.session.commit()

        return jsonify({'success': True, 'message': 'Kategori başarıyla güncellendi.'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e), 'success': False})

@app.route('/api/customers', methods=['GET'])
def get_customer():
    customers = Customer.query.all()
    return jsonify({'customer': [{'id': c.customer_id, 'name': c.first_name,'last_name': c.last_name, 'address':c.address, 'email': c.email,'phone_number':c.phone_number} for c in customers ]})

@app.route('/api/customers', methods=['POST'])
def add_customer():

    try:
        data = request.json
        new_customer = Customer(
            customer_id=data.get('musteri_id'),
            first_name=data.get('musteri_adi'),
            last_name=data.get('musteri_soyadi'),
            address=data.get('musteri_adresi'),
            email=data.get('musteri_mail'),
            phone_number=data.get('musteri_telefonu')
        )
        db.session.add(new_customer)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Müşteri eklendi'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e), 'success': False})
    
     
@app.route('/api/customers/<int:customer_id>', methods=['DELETE'])
def delete_customers(customer_id):
    try:
        customer = Customer.query.get(customer_id)
        
        if not customer:
            return jsonify({'error': 'Müşteri bulunamadı.', 'success': False}), 404

        db.session.delete(customer)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Müşteri başarıyla silindi.'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e), 'success': False})

@app.route('/api/customers/<int:customer_id>', methods=['PUT'])
def update_customers(customer_id):
    try:
        customer = Customer.query.get(customer_id)
        if not customer:
            return jsonify({'error': 'Müşteri bulunamadı.', 'success': False}), 404

        data = request.json
        customer.first_name = data.get('musteri_adi', customer.first_name)
        customer.last_name = data.get('musteri_soyadi', customer.last_name)
        customer.address = data.get('musteri_adresi', customer.address)
        customer.email = data.get('email', customer.email)
        customer.phone_number = data.get('telefon_numarasi', customer.phone_number)

        db.session.commit()
        return jsonify({'success': True, 'message': 'Müşteri başarıyla güncellendi.'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e), 'success': False})

    

@app.route('/api/orders', methods=['GET'])
def get_orders():
    orders = Orders.query.all()
    return jsonify({'orders': [{'id': o.orders_id, 'date': o.orders_date, 'customer_id': o.customer_id} for o in orders]})    


@app.route('/api/orders', methods=['POST'])
def add_order():
    try:
        data = request.json
        new_order = Orders(
            orders_id=data.get('siparis_id'),
            orders_date=data.get('siparis_tarihi'),
            customer_id=data.get('musteri_id')
        )
        db.session.add(new_order)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Sipariş eklendi'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e), 'success': False}) 

@app.route('/api/orders/<int:orders_id>', methods=['DELETE'])
def delete_orders(orders_id):
    try:
        order = Orders.query.get(orders_id)
        
        if not order:
            return jsonify({'error': 'Sipariş bulunamadı.', 'success': False}), 404

        db.session.delete(order)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Sipariş başarıyla silindi.'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e), 'success': False})

@app.route('/api/orders/<int:order_id>', methods=['PUT'])
def update_orders(order_id):
    try:
        order = Orders.query.get(order_id)
        if not order:
            return jsonify({'error': 'Sipariş bulunamadı.', 'success': False}), 404

        data = request.json
        order.orders_date = data.get('siparis_tarihi', order.orders_date)
        order.customer_id = data.get('musteri_id', order.customer_id)

        db.session.commit()

        return jsonify({'success': True, 'message': 'Sipariş başarıyla güncellendi.'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e), 'success': False})
    
@app.route('/api/shipping', methods=['GET'])
def get_shipping():
    shipping = Shipping.query.all()
    return jsonify({'shipping': [{'id': s.shipping_id, 'company': s.shipping_company, 'tracking_number': s.tracking_number, 'estimated_delivery_date': s.estimated_delivery_date} for s in shipping]})

@app.route('/api/shipping', methods=['POST'])
def add_shipping():
    try:
        data = request.json
        new_shipping = Shipping(
            shipping_id=data.get('shipping_id'),
            shipping_company=data.get('shipping_company'),
            tracking_number=data.get('tracking_number'),
            estimated_delivery_date=data.get('estimated_delivery_date')
        )
        db.session.add(new_shipping)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Kargo bilgisi eklendi'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e), 'success': False})

@app.route('/api/shipping/<int:shipping_id>', methods=['DELETE'])
def delete_shipping(shipping_id):
    try:
        shipping = Shipping.query.get(shipping_id)
        
        if not shipping:
            return jsonify({'error': 'Kargo bilgisi bulunamadı.', 'success': False}), 404

        db.session.delete(shipping)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Kargo bilgisi başarıyla silindi.'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e), 'success': False})

@app.route('/api/shipping/<int:shipping_id>', methods=['PUT'])
def update_shipping(shipping_id):
    try:
        shipping = Shipping.query.get(shipping_id)
        if not shipping:
            return jsonify({'error': 'Kargo bilgisi bulunamadı.', 'success': False}), 404

        data = request.json
        shipping.shipping_company = data.get('shipping_company', shipping.shipping_company)
        shipping.tracking_number = data.get('tracking_number', shipping.tracking_number)
        shipping.estimated_delivery_date = data.get('estimated_delivery_date', shipping.estimated_delivery_date)

        db.session.commit()

        return jsonify({'success': True, 'message': 'Kargo bilgisi başarıyla güncellendi.'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e), 'success': False})

@app.route('/api/delivery', methods=['GET'])
def get_delivery():
    delivery = Deliveries.query.all()
    return jsonify({'delivery': [{'id': d.delivery_id, 'date': d.delivery_date, 'address': d.delivery_address, 'status': d.delivery_status, 'tracking_number': d.tracking_number} for d in delivery]})

@app.route('/api/delivery', methods=['POST'])
def add_delivery():
    try:
        data = request.json
        new_delivery = Deliveries(
            delivery_id=data.get('delivery_id'),
            delivery_date=data.get('delivery_date'),
            delivery_address=data.get('delivery_address'),
            delivery_status=data.get('delivery_status'),
            tracking_number=data.get('tracking_number')
        )
        db.session.add(new_delivery)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Teslimat bilgisi eklendi'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e), 'success': False})

@app.route('/api/delivery/<int:delivery_id>', methods=['DELETE'])
def delete_delivery(delivery_id):
    try:
        delivery = Deliveries.query.get(delivery_id)
        
        if not delivery:
            return jsonify({'error': 'Teslimat bilgisi bulunamadı.', 'success': False}), 404

        db.session.delete(delivery)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Teslimat bilgisi başarıyla silindi.'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e), 'success': False})

@app.route('/api/delivery/<int:delivery_id>', methods=['PUT'])
def update_delivery(delivery_id):
    try:
        delivery = Deliveries.query.get(delivery_id)
        if not delivery:
            return jsonify({'error': 'Teslimat bilgisi bulunamadı.', 'success': False}), 404

        data = request.json
        delivery.delivery_date = data.get('delivery_date', delivery.delivery_date)
        delivery.delivery_address = data.get('delivery_address', delivery.delivery_address)
        delivery.delivery_status = data.get('delivery_status', delivery.delivery_status)
        delivery.tracking_number = data.get('tracking_number', delivery.tracking_number)

        db.session.commit()

        return jsonify({'success': True, 'message': 'Teslimat bilgisi başarıyla güncellendi.'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e), 'success': False})
    
@app.route('/api/ordersdetail', methods=['GET'])
def get_ordersdetail():
    ordersdetail = OrdersDetail.query.all()
    return jsonify({'ordersdetail': [{'id': od.orders_detail_id, 'orders_id': od.orders_id, 'product_id': od.product_id, 'quantity': od.quantity, 'unitprice': od.unitprice, 'subtotal': od.subtotal, 'delivery_id': od.delivery_id} for od in ordersdetail]})

@app.route('/api/ordersdetail', methods=['POST'])
def add_ordersdetail():
    try:
        data = request.json
        new_ordersdetail = OrdersDetail(
            orders_detail_id=data.get('orders_detail_id'),
            orders_id=data.get('orders_id'),
            product_id=data.get('product_id'),
            quantity=data.get('quantity'),
            unitprice=data.get('unitprice'),
            subtotal=data.get('subtotal'),
            delivery_id=data.get('delivery_id')
        )
        db.session.add(new_ordersdetail)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Sipariş detayı eklendi'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e), 'success': False})

@app.route('/api/ordersdetail/<int:orders_detail_id>', methods=['DELETE'])
def delete_ordersdetail(orders_detail_id):
    try:
        ordersdetail = OrdersDetail.query.get(orders_detail_id)
        
        if not ordersdetail:
            return jsonify({'error': 'Sipariş detayı bulunamadı.', 'success': False}), 404

        db.session.delete(ordersdetail)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Sipariş detayı başarıyla silindi.'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e), 'success': False})

@app.route('/api/ordersdetail/<int:orders_detail_id>', methods=['PUT'])
def update_ordersdetail(orders_detail_id):
    try:
        ordersdetail = OrdersDetail.query.get(orders_detail_id)
        if not ordersdetail:
            return jsonify({'error': 'Sipariş detayı bulunamadı.', 'success': False}), 404

        data = request.json
        ordersdetail.orders_id = data.get('orders_id', ordersdetail.orders_id)
        ordersdetail.product_id = data.get('product_id', ordersdetail.product_id)
        ordersdetail.quantity = data.get('quantity', ordersdetail.quantity)
        ordersdetail.unitprice = data.get('unitprice', ordersdetail.unitprice)
        ordersdetail.subtotal = data.get('subtotal', ordersdetail.subtotal)
        ordersdetail.delivery_id = data.get('delivery_id', ordersdetail.delivery_id)

        db.session.commit()

        return jsonify({'success': True, 'message': 'Sipariş detayı başarıyla güncellendi.'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e), 'success': False})


if __name__ == '__main__':
    with app.app_context():
         db.create_all()
    app.run(debug=True)



