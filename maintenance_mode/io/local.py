# -*- coding: utf-8 -*-
"""
.. module:: maintenance_mode.io.local.py
   :synopsis: Define IO class to save the maintenance mode status in a local
   file

.. moduleauthor:: Edgar Zamora Gomez <edgarzamoragomez@gmail.com>
"""
from maintenance_mode.io import AbstractIO


class IO(AbstractIO):

    def read_file(self, file_path, default_content=''):
        """ TODO: Add docs """
        try:
            handler = open(file_path, 'r')
            content = handler.read()
            handler.close()
            return content or default_content

        except IOError:
            return default_content

    def write_file(self, file_path, content):
        """ TODO: Add docs """
        try:
            handler = open(file_path, 'w+')
            handler.write(content)
            handler.close()
            return True

        except IOError:
            return False
