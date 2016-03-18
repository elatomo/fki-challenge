# -*- coding: utf-8 -*-

"""Tests for models."""

import unittest
from peewee import IntegrityError
from fki_challenge import models

TABLES = [models.Attribute, models.Person, models.PersonAttribute]

# init a memory db
models.database.init(':memory:')


class ModelsTestCase(unittest.TestCase):
    def setUp(self):
        models.database.connect()
        models.database.create_tables(TABLES, safe=True)

    def tearDown(self):
        models.database.drop_tables(TABLES, safe=True)


class AttributeTestCase(ModelsTestCase):
    """`Attribute` persistence test case."""

    def test_create_attribute(self):
        attribute = models.Attribute(name='real')
        attribute.save()
        self.assertEqual(1, attribute.id)

    def test_unique_name(self):
        attribute = models.Attribute(name='real')
        attribute.save()
        with self.assertRaises(IntegrityError):
            models.Attribute(name='real').save()


class PersonTestCase(ModelsTestCase):
    """`Person` persistence test case."""

    def test_create_person(self):
        person = models.Person(name='Marie Curie')
        person.save()
        self.assertEqual(1, person.id)

    def test_unique_name(self):
        person = models.Person(name='Marie Curie')
        person.save()
        with self.assertRaises(IntegrityError):
            models.Person(name='Marie Curie').save()


class PersonAttributeTestCase(ModelsTestCase):
    """`PersonAttribute` persistence test case."""

    def setUp(self):
        super().setUp()
        self.attribute = models.Attribute(name='fictional')
        self.attribute.save()
        self.person = models.Person(name='Marie Curie')
        self.person.save()

    def test_create_person_attribute(self):
        p_attribute = models.PersonAttribute(person=self.person,
                                             attribute=self.attribute,
                                             value=True)
        p_attribute.save()
        self.assertEqual(1, p_attribute.id)
        self.assertEqual(1, p_attribute.person.id)
        self.assertEqual(1, p_attribute.attribute.id)

    def test_unique_constrain(self):
        p_attribute = models.PersonAttribute(person=self.person,
                                             attribute=self.attribute,
                                             value=True)
        p_attribute.save()
        with self.assertRaises(IntegrityError):
            models.PersonAttribute(person=self.person,
                                   attribute=self.attribute,
                                   value=False).save()

    @unittest.skip('not implemented yet')
    def test_get_person_matches(self):
        pass
