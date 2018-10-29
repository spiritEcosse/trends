from shutterstock.resource import Resource
from shutterstock.resources import ImageEndPoint


class Image(Resource):
    LIST = ImageEndPoint('/images/search', ['page', 'per_page'])
