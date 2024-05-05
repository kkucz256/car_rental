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
    return 'Witaj w API wypożyczalni!'


@app.route('/cars', methods=['POST'])
def add_car():
    conn = connect_to_db()
    cur = conn.cursor()
    data = request.get_json()

    cur.execute(f"""INSERT INTO car (brand_id, status, price_per_day, year_of_production,
                horsepower, engine_type, body, color_id, max_velocity, gearbox, seats_no,
                deposit, last_rental_beginning, last_rental_end, place_id, photo) VALUES ('{data['brand_id']}',
                 '{data['status']}', '{data['price_per_day']}', '{data['year_of_production']}', '{data['horsepower']}',
                  '{data['engine_type']}', '{data['body']}', '{data['color_id']}', '{data['max_velocity']}',
                   '{data['gearbox']}', '{data['seats_no']}', '{data['deposit']}', '{data['last_rental_beginning']}',
                    '{data['last_rental_end']}', '{data['place_id']}', '{data['photo']}')""")
    conn.commit()
    brand_id = data['brand_id']
    cur.execute(f"SELECT brand FROM brand WHERE brand_id = {brand_id}")
    brand_name = cur.fetchone()[0] if cur.rowcount > 0 else None

    cur.close()
    conn.close()
    return f'Car {brand_name} added successfully!'

@app.route('/log-in', methods=['GET'])
def log_in():
    conn = connect_to_db()
    cur = conn.cursor()
    data = request.get_json()

    cur.execute(f"""SELECT password FROM customer WHERE mail = '{data['email']}'""")
    try:
        db_password = cur.fetchone()[0]
        print(db_password, data['password'])
        if db_password == data['password']:
            return jsonify({'success': True}), 200
        else:
            return jsonify({'Wrong password': True}), 300
    except:
        return jsonify({'error': 'Wrong username or password'}), 400
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
