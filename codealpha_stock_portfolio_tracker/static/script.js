let portfolio = [];

document.getElementById('add-stock-button').addEventListener('click', function() {
    // Toggle the visibility of the stock form
    const form = document.getElementById('stock-form');
    form.style.display = (form.style.display === 'none' || form.style.display === '') ? 'block' : 'none';
});

document.getElementById('stock-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const stockSymbol = document.getElementById('stock-symbol').value;
    const stockQuantity = parseFloat(document.getElementById('stock-quantity').value);
    const stockPrice = parseFloat(document.getElementById('stock-price').value);

    // Make POST request to Flask backend to add stock
    fetch('/add_stock', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            symbol: stockSymbol,
            quantity: stockQuantity,
            purchase_price: stockPrice
        })
    })
    .then(response => response.json())
    .then(data => {
        // Clear form fields
        document.getElementById('stock-symbol').value = '';
        document.getElementById('stock-quantity').value = '';
        document.getElementById('stock-price').value = '';

        // Fetch updated portfolio
        loadPortfolio();
        document.getElementById('stock-form').style.display = 'none';
    });
});

// Fetch and update the portfolio table
function loadPortfolio() {
    fetch('/get_portfolio')
        .then(response => response.json())
        .then(data => {
            portfolio = data;
            updatePortfolioTable(portfolio);
            updateTotalPortfolioValue(portfolio);
        });
}

// Function to update the portfolio table dynamically
function updatePortfolioTable(portfolio) {
    const tbody = document.querySelector('#portfolio-table tbody');
    tbody.innerHTML = '';

    portfolio.forEach((stock, index) => {
        const tr = document.createElement('tr');
        const stockValue = stock.value.toFixed(2);
        tr.innerHTML = `
            <td>${index + 1}</td>
            <td>${stock.symbol}</td>
            <td>${stock.quantity}</td>
            <td>${stock.purchase_price}</td>
            <td>${stock.current_price.toFixed(2)}</td>
            <td>${stockValue}</td>
            <td><button onclick="removeStock(${stock.id})">Remove</button></td>
        `;
        tbody.appendChild(tr);
    });
}

// Function to update the total portfolio value
function updateTotalPortfolioValue(portfolio) {
    let totalValue = 0;
    
    portfolio.forEach(stock => {
        totalValue += stock.value;
    });

    document.getElementById('total-value-amount').textContent = totalValue.toFixed(2);
}

// Remove stock from the portfolio
function removeStock(stockId) {
    fetch(`/remove_stock/${stockId}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);  // Log success message
        // Refresh the portfolio after removal
        loadPortfolio();
    })
    .catch(error => console.error('Error:', error));
}

// Load the portfolio when the page is loaded
window.onload = function() {
    loadPortfolio();
};
