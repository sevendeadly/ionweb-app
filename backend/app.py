from flask import Flask, jsonify
import psycopg2
from config import DATABASE_CONFIG
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

def get_db_connection():
    try:
        app.logger.debug(f"Attempting to connect to database with config: {DATABASE_CONFIG}")
        conn = psycopg2.connect(
            dbname=DATABASE_CONFIG['database'],
            user=DATABASE_CONFIG['user'],
            password=DATABASE_CONFIG['password'],
            host=DATABASE_CONFIG['host'],
            port=DATABASE_CONFIG['port']
        )
        return conn
    except Exception as e:
        app.logger.error(f"Database connection error: {str(e)}")
        return None

@app.route('/')
def hello_world():
    try:
        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            cur.execute('SELECT name FROM users LIMIT 1')
            result = cur.fetchone()
            cur.close()
            conn.close()

            if result:
                name = result[0]
                return jsonify({
                    "message": f"Hello world, {name}",
                    "status": "success"
                })
            else:
                return jsonify({
                    "message": "No name found in database",
                    "status": "error"
                }), 404
        else:
            return jsonify({
                "message": "Database connection failed",
                "status": "error"
            }), 500
    except Exception as e:
        app.logger.error(f"Error: {str(e)}")
        return jsonify({
            "message": f"Internal server error: {str(e)}",
            "status": "error"
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
