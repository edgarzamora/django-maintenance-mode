# -*- coding: utf-8 -*-
"""
.. module:: maintenance_mode.io.abstract_io.py
   :synopsis: Define an Abstract IO class

.. moduleauthor:: Edgar Zamora Gomez <edgarzamoragomez@gmail.com>
"""


class AbstractIO(object):

    def read_file(self, file_path, default_content=''):
        """ TODO: Add docs """
        raise NotImplementedError

    def write_file(self, file_path, content):
        """ TODO: Add docs """
        raise NotImplementedError
