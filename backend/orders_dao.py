from sql_connection import get_sql_connection
import traceback

def get_all_orders(connection):
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT order_id, customer_name, datetime, total FROM `order` ORDER BY datetime DESC"
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        traceback.print_exc()
        return []
    finally:
        cursor.close()

def insert_order(connection, orders):
    if not isinstance(orders, list):
        orders = [orders]

    inserted_orders = []  # will store dicts: {"order_id": X, "total_amount": Y}

    try:
        cursor = connection.cursor(dictionary=True)

        for order in orders:
            total_order_amount = 0
            product_prices = {}

            # Calculate total order amount
            for detail in order['order_details']:
                product_id = detail['product_id']
                quantity = float(detail['quantity'])

                if product_id not in product_prices:
                    cursor.execute(
                        "SELECT price_per_unit FROM product WHERE product_id = %s",
                        (product_id,)
                    )
                    price_data = cursor.fetchone()
                    if not price_data:
                        raise ValueError(f"Product ID {product_id} not found")
                    product_prices[product_id] = float(price_data['price_per_unit'])

                total_order_amount += product_prices[product_id] * quantity

            # Insert into order table
            cursor.execute(
                "INSERT INTO `order` (customer_name, datetime, total) VALUES (%s, NOW(), %s)",
                (order['customer_name'], total_order_amount)
            )
            order_id = cursor.lastrowid
            inserted_orders.append({"order_id": order_id, "total_amount": total_order_amount})

            # Insert order details
            for detail in order['order_details']:
                product_id = detail['product_id']
                quantity = float(detail['quantity'])
                line_total = product_prices[product_id] * quantity
                uom_id = detail.get('uom_id')

                if uom_id is not None:
                    cursor.execute(
                        "INSERT INTO order_details (order_id, product_id, Quantity, total_price, uom_id) VALUES (%s, %s, %s, %s, %s)",
                        (order_id, product_id, quantity, line_total, uom_id)
                    )
                else:
                    cursor.execute(
                        "INSERT INTO order_details (order_id, product_id, Quantity, total_price) VALUES (%s, %s, %s, %s)",
                        (order_id, product_id, quantity, line_total)
                    )

        connection.commit()
        return inserted_orders

    except Exception as e:
        connection.rollback()
        traceback.print_exc()
        return None
    finally:
        cursor.close()

def get_order_details(connection, order_id):
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT od.order_detail_id, od.order_id, od.product_id, p.product_name,
                   od.Quantity, od.total_price, u.uom_name
            FROM order_details od
            INNER JOIN product p ON od.product_id = p.product_id
            LEFT JOIN uom u ON od.uom_id = u.uom_id
            WHERE od.order_id = %s
        """
        cursor.execute(query, (order_id,))
        return cursor.fetchall()
    except Exception as e:
        traceback.print_exc()
        return []
    finally:
        cursor.close()
