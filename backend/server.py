from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import products_dao
import uom_dao
import orders_dao
from sql_connection import get_sql_connection
import traceback

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})

# ---------- FRONTEND PAGES ----------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/manage_product")
def manage_product():
    return render_template("manage_product.html")

@app.route("/orders")
def orders_page():
    return render_template("order.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# ---------- PRODUCTS API ----------
@app.route("/getProducts", methods=["GET"])
def get_products():
    connection = get_sql_connection()
    try:
        products = products_dao.get_all_products(connection)
        return jsonify(products)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

@app.route("/insertProduct", methods=["POST"])
def insert_product():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON payload'}), 400
    connection = get_sql_connection()
    try:
        product_id = products_dao.insert_new_product(connection, data)
        return jsonify({'product_id': product_id})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

@app.route("/updateProduct", methods=["POST"])
def update_product():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON payload'}), 400
    connection = get_sql_connection()
    try:
        rows = products_dao.update_product(connection, data)
        return jsonify({'updated_rows': rows})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

@app.route("/deleteProduct/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    connection = get_sql_connection()
    try:
        deleted = products_dao.delete_product(connection, product_id)
        return jsonify({'deleted_rows': deleted})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

# ---------- UOM API ----------
@app.route("/getUOM", methods=["GET"])
def get_uom():
    connection = get_sql_connection()
    try:
        uoms = uom_dao.get_uoms(connection)
        return jsonify(uoms)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

# ---------- ORDERS API ----------
@app.route("/getOrders", methods=["GET"])
def get_orders():
    connection = get_sql_connection()
    try:
        orders = orders_dao.get_all_orders(connection)
        return jsonify(orders)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

@app.route("/getOrderDetails/<int:order_id>", methods=["GET"])
def get_order_details(order_id):
    connection = get_sql_connection()
    try:
        details = orders_dao.get_order_details(connection, order_id)
        if not details:
            return jsonify({"error": "Order not found"}), 404
        return jsonify(details)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

@app.route('/insertOrder', methods=['POST'])
def insert_order():
    connection = get_sql_connection()
    try:
        data = request.get_json()
        customer_name = data['customer_name']
        order_details = data['order_details']

        total_amount = 0
        cursor = connection.cursor(dictionary=True)

        # Calculate total using product prices from DB
        for item in order_details:
            cursor.execute(
                "SELECT price_per_unit FROM product WHERE product_id = %s",
                (item['product_id'],)
            )
            product = cursor.fetchone()
            if not product:
                return jsonify({"error": f"Product ID {item['product_id']} not found"}), 400

            item_total = float(product['price_per_unit']) * int(item['quantity'])
            total_amount += item_total
            item['calculated_total'] = item_total  # Keep for insertion later

        # Insert into `order` table
        cursor.execute("""
            INSERT INTO `order` (customer_name, datetime, total)
            VALUES (%s, NOW(), %s)
        """, (customer_name, total_amount))
        order_id = cursor.lastrowid

        # Insert into `order_details`
        for item in order_details:
            cursor.execute("""
                INSERT INTO order_details (order_id, product_id, quantity, total_price)
                VALUES (%s, %s, %s, %s)
            """, (order_id, item['product_id'], item['quantity'], item['calculated_total']))

        connection.commit()

        return jsonify({
            'order_id': order_id,
            'total_amount': total_amount
        })
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()


# ---------- RUN SERVER ----------
if __name__ == "__main__":
    print("Starting Python Flask Server For Grocery Store Management System")
    app.run(debug=True, port=5000)
