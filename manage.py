# -*- coding: utf-8 -*-

"""
manage
~~~~~~

Manager module.
"""

from flask_script import Manager
from fki_challenge.app import create_app

manager = Manager(create_app())


if __name__ == "__main__":
    manager.run()
