from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

db_params = {
    'dbname': 'defaultdb',
    'user': 'avnadmin',
    'password': 'AVNS_QxzPpkrNJXOolRyltc4',
    'host': 'car-rental-car-rreennttaall.e.aivencloud.com',
    'port': '22365'
}


def connect_to_db():
    conn = psycopg2.connect(**db_params)
    return conn


@app.route('/')
def index():
    return 'Witaj w API naszej wypożyczalni samochodów!'


@app.route('/cars', methods=['GET'])
def get_cars():
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM cars")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)


@app.route('/cars', methods=['POST'])
def add_car():
    conn = connect_to_db()
    cur = conn.cursor()

    data = request.get_json()
    brand = data.get('brand')
    color = data.get('color')

    cur.execute(f"SELECT * FROM cars WHERE brand LIKE '{brand}' AND color LIKE '{color}'")
    existing_car = cur.fetchone()

    if existing_car:
        return jsonify({'message': f'Samochód marki {brand} o kolorze {color} już istnieje.'}), 400

    cur.execute(f"INSERT INTO cars (brand, color) VALUES ('{brand}', '{color}')")
    conn.commit()

    cur.close()
    conn.close()

    return jsonify({'message': f'Samochód {brand} o kolorze {color} dodany pomyślnie!'}), 201

if __name__ == '__main__':
    app.run(debug=True)

