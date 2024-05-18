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

@app.route('/log-in_staff', methods=['GET'])
def log_in_staff():
    conn = connect_to_db()
    cur = conn.cursor()
    data = request.get_json()

    cur.execute(f"""SELECT password FROM staff WHERE mail = '{data['email']}'""")
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

@app.route('/register', methods=['POST'])
def register_user():
    conn = connect_to_db()
    cur = conn.cursor()
    data = request.get_json()
    city_id = 0
    country_id = 0

    cur.execute(f"""SELECT city_id FROM city WHERE city = '{data['address']['city']}'""")
    existing_city = cur.fetchone()
    if existing_city:
        city_id = existing_city[0]
    else:
        cur.execute(f"INSERT INTO city (city) VALUES ('{data['address']['city']}') RETURNING city_id")
        city_id = cur.fetchone()[0]

    cur.execute(f"""SELECT country_id FROM country WHERE country = '{data['address']['country']}'""")
    existing_country = cur.fetchone()
    if existing_country:
        country_id = existing_country[0]
    else:
        cur.execute(f"INSERT INTO country (country) VALUES ('{data['address']['country']}') RETURNING country_id")
        country_id = cur.fetchone()[0]

    cur.execute(f"""
        INSERT INTO address (postal_code, city_id, address_1, address_2, country_id)
        VALUES ('{data['address']['post_code']}', '{city_id}', '{data['address']['address_1']}', '{data['address']['address_2']}', '{country_id}') RETURNING address_id
    """)
    address_id = cur.fetchone()[0]

    cur.execute(f"""SELECT customer_id FROM customer 
                    WHERE first_name = '{data['first_name']}' 
                    AND last_name = '{data['last_name']}' 
                    AND mail = '{data['email']}' 
                    AND date_of_birth = '{data['date_of_birth']}' 
                    AND phone_no = '{data['phone_number']}'""")
    existing_customer = cur.fetchone()
    if existing_customer:
        return jsonify({'error': 'Customer already exists'}), 400

    cur.execute(f"""INSERT INTO customer(address_id, first_name, last_name, mail, password, date_of_birth, phone_no) 
    VALUES ('{address_id}', '{data['first_name']}', '{data['last_name']}', '{data['email']}', '{data['password']}', 
    '{data['date_of_birth']}', '{data['phone_number']}')""")

    conn.commit()

    return jsonify({f'Success mr./mrs. {data['first_name']} {data['last_name']}, you have been registered': True}), 200

if __name__ == '__main__':
    app.run(debug=True)
