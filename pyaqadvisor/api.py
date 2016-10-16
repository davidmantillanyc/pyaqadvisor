
# MIT License
# 
# Copyright (c) 2016 David Mantilla
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE

"""
api.py

This module is meant to be the main interface to aqadvisor.com.
It provides a more friendly interface to the webservice through
the user of python objects, Stocking and Tank

Create a Tank() object, add some fish (stocking) to it,
and then make the call to aqadvisor to see if your tank is well
stocked and if it has enough filtration.
"""

from fuzzywuzzy import process

from pyaqadvisor.fishyparser import get_stocking_info
from pyaqadvisor.aqadvisor_assets import TANK_INFO, FILTER_DATA, fish_species


class Stocking(object):
    """
    Stocking object defines a fish tank's stocking plan
    and follows a builder design pattern.

    Uses fuzzy matching to look up fish species that are available in
    AqAdvisor's database. First match is always returned.
    Call aqadvisor_stock_list to get the matched stocking list

    Example:
    s = Stocking().add('cardinal tetra', 5).add('panda cory', 6)
    s.aqadvisor_stock_list
    """

    _stock_list = None  # internal representation of users' stocking
    @property
    def stock_list(self):
        if self._stock_list:
            return self._stock_list
        else:
            self._stock_list = {}
            return self._stock_list

    _aqadvisor_stock_list = None # these values must match AqAdvisor's labels
    @property
    def aqadvisor_stock_list(self):
        if self._aqadvisor_stock_list:
            return self._aqadvisor_stock_list
        else:
            return self.build().aqadvisor_stock_list

    def __init__(self, stock_list=None):
        if stock_list and isinstance(stock_list, dict): self._stock_list = stock_list

    def add(self, english_name, quantity, scientific_name=None):
        """append stocking to stock list"""
        species_name = scientific_name if scientific_name else english_name
        self.stock_list[species_name] = quantity
        return self

    def remove(self, english_name, quantity):
        """ removes from stocking list"""
        # TODO
        raise NotImplementedError

    def build(self):
        """Updates the object's AqAdvisor matching list"""
        self._aqadvisor_stock_list = {}
        for user_species_name, quantity in self._stock_list.items():
            aqadvisor_species_name = process.extractOne(user_species_name,
                                                        fish_species)[0]
            self._aqadvisor_stock_list[aqadvisor_species_name] = quantity
        return self

    def __str__(self):
        return str(self.stock_list)


class Tank(object):
    """
    Tank - represents an aquarium fish tank, including its
    dimensions, filtration, and stocking.

    This is the main interface for pyadqavisor. Use this object
    to call out to pyaqadvisor service.

    Example:
        t = Tank('10g').add_filter("AquaClear 30").add_stocking(
                Stocking().add('cardinal tetra', 5).add('panda cory', 5))
        print t, t.stocking, t.length, t.depth, t.height, t.ldh, t.filter_
        print t.get_stocking_level()
    """

    def __init__(self, tank_size, filter_name=None, stocking=None):
        """ given a tank size, '55g', get dimensions """
        self.length, self.depth, self.height = TANK_INFO.get(tank_size, [None, None, None])
        self.tank_size = tank_size
        self._stocking = stocking if stocking else Stocking()
        if filter_name: self.add_filter(filter_name)

    def add_filter(self, filter_name):
        matched_filter_name = process.extractOne(filter_name, FILTER_DATA.keys())[0]
        if matched_filter_name:
            self.filter_name = matched_filter_name
            self.filter_capacity = FILTER_DATA[matched_filter_name]
        else:
            self.filter_name = 'Filter Not Found'
            self.filter_capacity = '0'
        return self

    def add_stocking(self, stocking):
        """ input: Stocking object """
        self._stocking = stocking
        return self

    @property
    def stocking(self):
        return self._stocking

    @property
    def ldh(self):
        """ returns tuple of legnth-depth-height dimesions"""
        return (self.length, self.depth, self.height)

    @property
    def filter_(self):
        return (self.filter_name, self.filter_capacity)

    def __str__(self):
        # FIXME: not pythonic, but got job done with decent readability
        s = "<Tank: {0}".format(self.tank_size)
        s += " with {0}".format(self.filter_name) if getattr(self, 'filter_name', None) else ""
        s += ">"
        return s

    def get_stocking_level(self):
        return get_stocking_info(self.stocking.aqadvisor_stock_list,
                                 self.ldh,
                                 self.filter_)
