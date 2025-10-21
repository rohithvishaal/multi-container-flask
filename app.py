from flask import Flask, render_template
from flask_cors import CORS
import os
import psycopg2
from random import randint
from waitress import serve
from dotenv import load_dotenv
load_dotenv()


def connect_to_db():
    try:
        conn = psycopg2.connect(dbname=os.environ["DB_NAME"],
                                user=os.environ["DB_USER"],
                                password=os.environ["DB_PASS"],
                                host=os.environ["DB_HOST"],
                                port=os.environ["DB_PORT"])
        cur = conn.cursor()
        return conn, cur
    except (Exception, psycopg2.Error) as error:
        print(f"Error : {error}")
        return None, None


app = Flask(__name__)
CORS(app)


def load_all_quotes():
    conn, cur = connect_to_db()
    if conn is not None and cur is not None:
        cur.execute("SELECT ID, AUTHOR, QUOTE FROM QUOTES.QUOTES")
        quotes = cur.fetchall()
        cur.close()
        conn.close()
        return quotes
    return None


@app.route("/")
def index():
    quote = "The Matrix has you Neo!"
    return render_template('index.html', quote=quote)


all_quotes = load_all_quotes()


@app.route("/quote", methods=["GET"])
def get_random_quote():
    random_quote = all_quotes[randint(
        0, len(all_quotes) - 1)] if all_quotes is not None else None
    return {
        "quote": random_quote
    }


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)
