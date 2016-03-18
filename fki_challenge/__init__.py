# -*- coding: utf-8 -*-

"""
fki_challenge
~~~~~~~~~~~~~
"""

import logging
from .version import __version__

__title__ = 'fki-challenge'
__author__ = 'José Fernández Ramos'
__license__ = 'BSD'
__copyright__ = 'Copyright 2016 José Fernández Ramos'

# set default logging handler
logging.getLogger(__name__).addHandler(logging.NullHandler())
