# -*- coding: utf-8 -*-

"""
fki_challenge.manage
~~~~~~~~~~~~~~~~~~~~

Manage commands.
"""

import csv
from flask_script import Command, Option
from . import models, settings


class PopulateDatabaseCommand(Command):
    """Pump CSV contents into the database."""

    def __init__(self, dataset=settings.FKI_DATASET):
        self.default_dataset = dataset

    def get_options(self):
        return [
            Option('-d', '--dataset', dest='dataset', default=self.default_dataset)
        ]

    def run(self, dataset):
        print('Loading dataset \'%s\'' % dataset)
        with open(dataset) as csvfile:
            # get ready, this is gonna be ugly as hell
            reader = csv.reader(csvfile)
            next(reader)  # ignore firt line

            # insert, index and keep track of ids for all found person names
            person_names = next(reader)
            person_ids = dict((index, models.Person.insert(name=name).execute())
                              for index, name in enumerate(person_names) if name)

            for attribute_row in reader:
                attribute_name = attribute_row[1]
                attribute_id = models.Attribute.insert(name=attribute_name).execute()
                # pick up person indexes with an attribute match
                relations = [i for i, value in enumerate(attribute_row[2:], start=2) if value]
                for person_index in relations:
                    models.PersonAttribute.insert(person=person_ids[person_index],
                                                  attribute=attribute_id).execute()

        print('Dataset successfully loaded')
