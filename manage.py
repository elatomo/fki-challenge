# -*- coding: utf-8 -*-

"""
manage
~~~~~~

Manager module.
"""

from flask_script import Manager
from fki_challenge.app import create_app
from fki_challenge.manage import PopulateDatabaseCommand

manager = Manager(create_app())
manager.add_command('populate_database', PopulateDatabaseCommand())


if __name__ == "__main__":
    manager.run()
