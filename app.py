from flask import Flask, request, render_template, redirect, url_for, jsonify
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from urllib.parse import quote_plus
import os

load_dotenv()

username = quote_plus(os.getenv('MONGO_USERNAME'))
password = quote_plus(os.getenv('MONGO_PASSWORD'))

client = MongoClient(f"mongodb+srv://{username}:{password}@cluster0.twkbvhk.mongodb.net/?appName=Cluster0")
db = client.test
collection = db['flask-tutorial']

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    error = None

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        age = request.form.get('age', '').strip()

        if not name or not age:
            error = 'Please provide both name and age.'
        else:
            try:
                age_int = int(age)
                document = {'name': name, 'age': age_int}
                collection.insert_one(document)
                return redirect(url_for('success'))
            except ValueError:
                error = 'Age must be a valid number.'
            except PyMongoError as e:
                error = f'Database error: {e}'
            except Exception as e:
                error = f'Unexpected error: {e}'

    return render_template('form.html', error=error)

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/api', methods=['GET'])
def api():
    try:
        data = list(collection.find({}, {"_id": 0}))
        return jsonify(data)
    except PyMongoError as e:
        return jsonify({"error": f"Database error: {e}"})
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {e}"})

if __name__ == '__main__':
    app.run(debug=True)
