from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('portfolio.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS stocks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT,
                    quantity INTEGER,
                    purchase_price REAL,
                    current_price REAL
                  )''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    # Display the main portfolio page
    return render_template('index.html')

@app.route('/add_stock', methods=['POST'])
def add_stock():
    # Add a stock entry to the database
    symbol = request.json.get('symbol')
    quantity = request.json.get('quantity')
    purchase_price = request.json.get('purchase_price')
    current_price = purchase_price * 1.2  # Example: current price is 20% more than purchase price

    conn = sqlite3.connect('portfolio.db')
    c = conn.cursor()
    c.execute('INSERT INTO stocks (symbol, quantity, purchase_price, current_price) VALUES (?, ?, ?, ?)',
              (symbol, quantity, purchase_price, current_price))
    conn.commit()
    conn.close()

    return jsonify({"message": "Stock added successfully!"}), 200

@app.route('/get_portfolio', methods=['GET'])
def get_portfolio():
    # Retrieve all stock entries from the database
    conn = sqlite3.connect('portfolio.db')
    c = conn.cursor()
    c.execute('SELECT * FROM stocks')
    stocks = c.fetchall()
    conn.close()
    
    portfolio = []
    for stock in stocks:
        portfolio.append({
            'id': stock[0],
            'symbol': stock[1],
            'quantity': stock[2],
            'purchase_price': stock[3],
            'current_price': stock[4],
            'value': stock[2] * stock[4]
        })
    
    return jsonify(portfolio), 200

@app.route('/remove_stock/<int:id>', methods=['DELETE'])
def remove_stock(id):
    # Delete stock entry from the database by its id
    conn = sqlite3.connect('portfolio.db')
    c = conn.cursor()
    c.execute('DELETE FROM stocks WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": f"Stock {id} removed successfully!"}), 200

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
