# -*- coding: utf-8 -*-

"""
fki_challenge.resources
~~~~~~~~~~~~~~~~~~~~~~~

Our API resources.
"""

import flask_restful as restful
from flask_restful import reqparse
from playhouse.shortcuts import model_to_dict
from . import models


class Attribute(restful.Resource):
    def get(self, attribute_id):
        try:
            return model_to_dict(models.Attribute.get(id=attribute_id))
        except models.Attribute.DoesNotExist:
            restful.abort(404)


class AttributeList(restful.Resource):
    def get(self):
        return [attribute for attribute in models.Attribute.select().dicts()]


class Person(restful.Resource):
    def get(self, person_id):
        try:
            return model_to_dict(models.Person.get(id=person_id))
        except models.Person.DoesNotExist:
            restful.abort(404)


class PersonList(restful.Resource):
    def get(self):
        return [person for person in models.Person.select().dicts()]


class MatchList(restful.Resource):

    def __init__(self, error_rate):
        self.error_rate = error_rate
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('attributes', type=str,
                                   required=True,
                                   help='Comma-seperated list of attributes to match')
        self.reqparse.add_argument('limit', type=int,
                                   required=False,
                                   default=5,
                                   help='Limit the number of persons matched')

    def get(self):
        args = self.reqparse.parse_args()
        attributes = args.attributes.split(',')

        # TODO: refactor probability lambda
        prob = lambda positives, negatives: round(((1-self.error_rate)**positives)*(self.error_rate**negatives), 3)

        matches = models.PersonAttribute.get_person_matches(*attributes, limit=args.limit)

        return [{p.name: prob(p.match_count, len(attributes) - p.match_count)}
                for p in matches]
