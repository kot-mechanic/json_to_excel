from flask import Flask, request, send_file, make_response
from flask_httpauth import HTTPBasicAuth
import pandas as pd
import random
import string

app = Flask(__name__)

auth = HTTPBasicAuth()
user = {'login': 'service', 'password': 'ScaNTestrApToWeITERaCEmanTALaver'}

def generate_random_string(length):
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string


@auth.verify_password
def verify_password(username, password):
    if username == user['login'] and password == user['password']:
        return username



@app.route('/load_json', methods=['POST'])
@auth.login_required
def load_json():
    if request.method == 'POST':
        json = request.get_json()
        filename = generate_random_string(10)
        pd.DataFrame(json).to_excel("D:\\work\\poslanie\\json_to_excel\\files\\" + str(filename) + ".xlsx", index=False)
        response = make_response(str("http://192.168.42.125:5000/get_excel/"+ str(filename) + ".xlsx" ), 200)
        response.mimetype = "text/plain"
        return response

@app.route('/get_excel/<file>', methods=['GET'])
@auth.login_required
def get_excel(file):
    if request.method == 'GET':
        print(file)
        return send_file("D:\\work\\poslanie\\json_to_excel\\files\\" + file, as_attachment=True, mimetype='application/vnd.ms-excel')

if __name__ == '__main__':
    app.run(host='192.168.42.125', port=5000)