from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello from Vercel Flask!'

@app.route('/test')
def test():
    return {'status': 'success', 'message': 'Flask is working on Vercel!'} 