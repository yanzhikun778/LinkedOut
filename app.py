from flask import (Flask, render_template, request, session, redirect)

app = Flask(__name__)
app.secret_key = "NotSecure"


@app.route('/')
def hello_world():
    return render_template('demo.html')


@app.route('/test')
def hello_world_test():
    return render_template('demo.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
