from flask import Flask
from waitress import serve

from app import app

if __name__ == "__main__":
    serve(app.run(),
          host="127.0.0.1",
          port=8080,
          threads=2
          )
