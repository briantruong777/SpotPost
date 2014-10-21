from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'This is spotpost!'

if __name__ == '__main__':
  # Runs on port 5000 by default
  # url: "localhost:5000"
  app.run(host="0.0.0.0")
