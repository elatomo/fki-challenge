# -*- coding: utf-8 -*-

"""
fki_challenge.settings
~~~~~~~~~~~~~~~~~~~~~~

Application default settings.
"""

import os

DEBUG = True

APP_DIR = os.path.abspath(os.path.dirname(__file__))  # thhis directory
PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))

FKI_DATABASE_FILE = os.path.join(PROJECT_ROOT, 'fki-challenge.sqlite')
FKI_DATASET = os.path.join(PROJECT_ROOT, 'data', 'dataset.csv')
FKI_ERROR_RATE = 0.2
