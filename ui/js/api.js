var API_BASE_URL = "http://127.0.0.1:5000";

// -------------------- Products --------------------

// Get all products
function getProducts(successCallback) {
    $.ajax({
        url: API_BASE_URL + "/getProducts",
        type: "GET",
        success: successCallback,
        error: function(xhr, status, error) {
            console.error("Error fetching products:", error);
        }
    });
}

// Insert new product
function insertProduct(product, successCallback) {
    $.ajax({
        url: API_BASE_URL + "/insertProduct",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            product_name: product.product_name,
            uom_id: product.uom_id,
            price_per_unit: product.price_per_unit
        }),
        success: successCallback,
        error: function(xhr, status, error) {
            console.error("Error inserting product:", error);
        }
    });
}

// Update product
function updateProduct(product, successCallback) {
    $.ajax({
        url: API_BASE_URL + "/updateProduct",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            product_id: product.product_id,
            product_name: product.product_name,
            uom_id: product.uom_id,
            price_per_unit: product.price_per_unit
        }),
        success: successCallback,
        error: function(xhr, status, error) {
            console.error("Error updating product:", error);
        }
    });
}

// Delete product
function deleteProduct(productId, successCallback) {
    $.ajax({
        url: API_BASE_URL + "/deleteProduct/" + productId,
        type: "DELETE",
        success: successCallback,
        error: function(xhr, status, error) {
            console.error("Error deleting product:", error);
        }
    });
}

// -------------------- UOM --------------------

// Get UOM list
function getUOMs(successCallback) {
    $.ajax({
        url: API_BASE_URL + "/getUOM",
        type: "GET",
        success: successCallback,
        error: function(xhr, status, error) {
            console.error("Error fetching UOMs:", error);
        }
    });
}

// -------------------- Orders --------------------

// Get all orders
function getOrders(successCallback) {
    $.ajax({
        url: API_BASE_URL + "/getOrders",
        type: "GET",
        success: successCallback,
        error: function(xhr, status, error) {
            console.error("Error fetching orders:", error);
        }
    });
}

// Insert new order
function insertOrder(order, successCallback) {
    // order should be in format:
    // { customer_name: "Name", order_details: [ {product_id, quantity, uom_id}, ... ] }

    $.ajax({
        url: API_BASE_URL + "/insertOrder",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(order),
        success: function(response) {
            if (response.error) {
                successCallback({ error: response.error });
            } else {
                successCallback({
                    order_id: response.order_id,
                    total_amount: response.total_amount
                });
            }
        },
        error: function(xhr, status, error) {
            successCallback({ error: xhr.responseJSON ? xhr.responseJSON.error : error });
        }
    });
}
