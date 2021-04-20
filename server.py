from flask import Flask, render_template
from flask_restful import Api, Resource

from Routes.ImageSegment import ImageSegment

app = Flask(__name__)

api = Api(app)

@app.route('/')
def index():
     return render_template('index.html')


# @app.route('/segment')
# def segment():
#      return render_template('segment.html')


api.add_resource(ImageSegment, "/segment")

if __name__ == "__main__":
    app.run(debug=True)