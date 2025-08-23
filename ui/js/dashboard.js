document.addEventListener("DOMContentLoaded", () => {
    getProducts(function(products) {
        const tableBody = document.querySelector("#productTable tbody");
        tableBody.innerHTML = ""; // clear old rows

        products.forEach(prod => {
            const row = `
                <tr>
                    <td>${prod.product_id}</td>
                    <td>${prod.product_name}</td>
                    <td>${prod.uom_name}</td>
                    <td>${prod.price_per_unit}</td>
                </tr>
            `;
            tableBody.innerHTML += row;
        });
    });
});
