# -*- coding: utf-8 -*-

"""
fki_challenge.models
~~~~~~~~~~~~~~~~~~~~
"""

import peewee


class SqliteFKDatabase(peewee.SqliteDatabase):
    """Custom SQLite database for enforcing foreign key constraints."""

    def initialize_connection(self, conn):
        self.execute_sql('PRAGMA foreign_keys=ON;')


# un-unitialized sqlite database
database = SqliteFKDatabase(None)


class BaseModel(peewee.Model):
    """Specify a common database for all our models."""

    class Meta:
        database = database


class Attribute(BaseModel):
    """`Attribute` representation.

    :param name: Attribute name.
    """

    name = peewee.CharField(unique=True)


class Person(BaseModel):
    """`Person` representation.

    :param name: Person name.
    """

    name = peewee.CharField(unique=True)


class PersonAttribute(BaseModel):
    """Person' attribute.

    :param person: Person ID.
    :param attribute: Attribute ID.
    :param value: (optional) `Boolean`. Defaults to `True`.
    """

    person = peewee.ForeignKeyField(db_column='person_id',
                                    rel_model=Person, to_field='id')
    attribute = peewee.ForeignKeyField(db_column='attribute_id',
                                       rel_model=Attribute, to_field='id')
    value = peewee.BooleanField(default=True)

    class Meta:
        db_table = 'person_attribute'
        indexes = (
            # unique index on person/attribute
            (('person', 'attribute'), True),
        )
