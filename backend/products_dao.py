from sql_connection import get_sql_connection
import traceback

def get_all_products(connection):
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT product.product_id, product.product_name, 
                   product.price_per_unit, uom.uom_name 
            FROM product
            INNER JOIN uom ON product.uom_id = uom.uom_id
        """
        cursor.execute(query)
        response = cursor.fetchall()
        return response
    except Exception as e:
        traceback.print_exc()
        return []
    finally:
        cursor.close()


def insert_new_product(connection, product):
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO product (product_name, uom_id, price_per_unit)
            VALUES (%s, %s, %s)
        """
        data = (product['product_name'], product['uom_id'], product['price_per_unit'])
        cursor.execute(query, data)
        connection.commit()
        return cursor.lastrowid
    except Exception as e:
        connection.rollback()
        traceback.print_exc()
        return None
    finally:
        cursor.close()


def update_product(connection, product):
    """
    Updates a product. Expects dictionary with keys:
    product_id, product_name, uom_id, price_per_unit
    """
    try:
        cursor = connection.cursor()
        query = """
            UPDATE product
            SET product_name = %s,
                uom_id = %s,
                price_per_unit = %s
            WHERE product_id = %s
        """
        data = (product['product_name'], product['uom_id'], product['price_per_unit'], product['product_id'])
        cursor.execute(query, data)
        connection.commit()
        return cursor.rowcount
    except Exception as e:
        connection.rollback()
        traceback.print_exc()
        return 0
    finally:
        cursor.close()


def delete_product(connection, product_id):
    try:
        cursor = connection.cursor()
        query = "DELETE FROM product WHERE product_id = %s"
        cursor.execute(query, (product_id,))
        connection.commit()
        return cursor.rowcount
    except Exception as e:
        connection.rollback()
        traceback.print_exc()
        return 0
    finally:
        cursor.close()
