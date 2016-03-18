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

    @classmethod
    def get_person_matches(cls, *attributes, limit=100):
        """Get persons and their amount of matches for the given attributes.

        Each `Person` object is extended with an `match_count` property, which
        denotes the total amount of positive matches for the given attributes.

        The generator is sorted by the number of matches in descending order.

        :param \*attributes: attribute names to match.
        :param limit: (optinal) maximum number of persons to return.
        """

        # all `True` person attributes for a given list of attributes
        subquery = (cls.select(cls.person, cls.attribute)
                    .join(Attribute)
                    .where(cls.value == True, Attribute.name << attributes))

        match_count = peewee.fn.count(subquery.c.attribute_id)

        # all person names, plus the amount of `True` matches for each one
        q = (Person.select(Person.name)
             .join(subquery, join_type=peewee.JOIN_LEFT_OUTER,
                   on=(Person.id == subquery.c.person_id))
             .group_by(Person.name)
             .order_by(match_count.desc())
             .annotate(subquery, match_count.alias('match_count'))
             .limit(limit))

        return q.iterator()
