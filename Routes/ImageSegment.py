from flask import render_template
from flask_restful import Api, Resource, reqparse
from Validations.ImageSubmitValidation import PostImageSubmitValidation
from Segmentation.Segment import Segment

postImageValidation = PostImageSubmitValidation()
 

class ImageSegment(Resource):
    def get(self):
        return render_template('index.html')
    def post(self):
        args = postImageValidation.resquestArgs.parse_args()

        imageFile = args['image']
        imageName = args['image_name'] + ".jpg"

        imagePath = "Output/"+imageName

        imageFile.save(imagePath)

        segment = Segment(imagePath)
        segment.tst();

        return {
            "message": {
                "name": imageName,
            } 
        }, 201