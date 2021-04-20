from flask_restful import reqparse
import werkzeug

class PostImageSubmitValidation: 

    resquestArgs = reqparse.RequestParser();

    resquestArgs.add_argument("image_name", type=str, required= True, help="Image name is required")

    # resquestArgs.add_argument("imagedata", type=str, required= True, help="Image data is required")

    resquestArgs.add_argument("image", type= werkzeug.datastructures.FileStorage , required= True, help="Image is required", location='files')

