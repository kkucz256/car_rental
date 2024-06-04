from flask import Flask, jsonify, request
import psycopg2
from Car_details_class import Car_details_class

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


from flask import Flask, jsonify, request
from Car_for_list import Car_for_list
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

    cur.execute(f"SELECT brand_id FROM brand WHERE brand = %s", (data['brand_name'].capitalize(),))
    existing_brand = cur.fetchone()
    if existing_brand:
        brand_id = existing_brand[0]
    else:
        cur.execute(f"INSERT INTO brand (brand) VALUES (%s) RETURNING brand_id", (data['brand_name'].capitalize(),))
        brand_id = cur.fetchone()[0]

    cur.execute("SELECT color_id FROM color WHERE color = %s", (data['color_name'].capitalize(),))
    existing_color = cur.fetchone()
    if existing_color:
        color_id = existing_color[0]
    else:
        cur.execute("INSERT INTO color (color) VALUES (%s) RETURNING color_id", (data['color_name'].capitalize(),))
        color_id = cur.fetchone()[0]

    cur.execute("""INSERT INTO car (brand_id, status, price_per_day, year_of_production,
                    horsepower, engine_type, body, color_id, max_velocity, gearbox, seats_no,
                    deposit, last_rental_beginning, last_rental_end, place_id, photo, model) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (brand_id, data['status'], data['price_per_day'], data['year_of_production'],
                 data['horsepower'], data['engine_type'].lower(), data['body'].lower(), color_id,
                 data['max_velocity'], data['gearbox'].lower(), data['seats_no'], data['deposit'],
                 data['last_rental_beginning'], data['last_rental_end'], data['place_id'],
                 data['photo'], data['model']))
    conn.commit()

    cur.close()
    conn.close()
    return jsonify({f'Car {data['brand_name']} added successfully': True}), 200


@app.route('/log-in', methods=['GET'])
def log_in():
    conn = connect_to_db()
    cur = conn.cursor()
    data = request.get_json()

    cur.execute("SELECT customer_id, password FROM customer WHERE mail = %s", (data['email'],))
    try:
        user = cur.fetchone()
        if user and user[1] == data['password']:
            user_id = user[0]
            return jsonify({'success': True, 'user_id': user_id}), 200
        else:
            return jsonify({'Wrong password': True}), 300
    except:
        return jsonify({'Wrong username or password': True}), 400
    finally:
        cur.close()
        conn.close()



@app.route('/log-in_staff', methods=['GET'])
def log_in_staff():
    conn = connect_to_db()
    cur = conn.cursor()
    data = request.get_json()

    cur.execute("SELECT password FROM staff WHERE mail = %s", (data['email'],))
    try:
        db_password = cur.fetchone()[0]
        print(db_password, data['password'])
        if db_password == data['password']:
            return jsonify({'success': True}), 200
        else:
            return jsonify({'Wrong password': True}), 300
    except:
        return jsonify({'Wrong username or password': True}), 400
    finally:
        cur.close()
        conn.close()


@app.route('/register', methods=['POST'])
def register_user():
    conn = connect_to_db()
    cur = conn.cursor()
    data = request.get_json()

    cur.execute("SELECT city_id FROM city WHERE city = %s", (data['address']['city'].capitalize(),))
    existing_city = cur.fetchone()
    if existing_city:
        city_id = existing_city[0]
    else:
        cur.execute("INSERT INTO city (city) VALUES (%s) RETURNING city_id", (data['address']['city'].capitalize(),))
        city_id = cur.fetchone()[0]

    cur.execute("SELECT country_id FROM country WHERE country = %s", (data['address']['country'].capitalize(),))
    existing_country = cur.fetchone()
    if existing_country:
        country_id = existing_country[0]
    else:
        cur.execute("INSERT INTO country (country) VALUES (%s) RETURNING country_id",
                    (data['address']['country'].capitalize(),))
        country_id = cur.fetchone()[0]

    cur.execute("""
        INSERT INTO address (postal_code, city_id, address_1, address_2, country_id)
        VALUES (%s, %s, %s, %s, %s) RETURNING address_id
    """, (
    data['address']['post_code'], city_id, data['address']['address_1'], data['address']['address_2'], country_id))

    address_id = cur.fetchone()[0]

    cur.execute("""SELECT customer_id FROM customer 
                   WHERE first_name = %s 
                   AND last_name = %s 
                   AND mail = %s 
                   AND date_of_birth = %s 
                   AND phone_no = %s""",
                (data['first_name'], data['last_name'], data['email'], data['date_of_birth'], data['phone_number']))
    existing_customer = cur.fetchone()
    if existing_customer:
        return jsonify({'error': 'Customer already exists'}), 400

    cur.execute("""INSERT INTO customer (address_id, first_name, last_name, mail, password, date_of_birth, phone_no) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (address_id, data['first_name'], data['last_name'], data['email'], data['password'],
                 data['date_of_birth'], data['phone_number']))

    conn.commit()

    return jsonify({f'Success mr./mrs. {data['first_name']} {data['last_name']}, you have been registered': True}), 200


@app.route('/user-screen', methods=['GET'])
def provide_cars():
    car_list = []
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("""SELECT car.car_id, brand.brand, color.color, car.model, car.price_per_day, car.body, 
                           car.gearbox, car.seats_no 
                           FROM car 
                           JOIN brand ON car.brand_id = brand.brand_id 
                           JOIN color ON car.color_id = color.color_id""")
        rows = cur.fetchall()
        for row in rows:
            car = Car_for_list(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            car_list.append(car)
        conn.close()
        return jsonify([car.__dict__ for car in car_list])
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500


@app.route('/car-details/<int:car_id>', methods=['GET'])
def getcardetails(car_id):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT car.car_id, brand.brand, car.status, car.price_per_day, car.year_of_production, car.horsepower, 
            car.engine_type,car.body, color.color, car.max_velocity, car.gearbox,
            car.seats_no,car.deposit,  car.last_rental_end,car.model,car.photo
            FROM car 
            JOIN brand ON car.brand_id = brand.brand_id 
            JOIN color ON car.color_id = color.color_id
            WHERE car.car_id = %s
        """, (car_id,))
        row = cur.fetchone()
        conn.close()
        if row:
            car = Car_details_class(*row)
            print(car.__dict__)
            return jsonify(car.__dict__)
        else:
            return jsonify({"error": "Car not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
