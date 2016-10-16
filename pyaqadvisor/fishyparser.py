
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
fishyparser.py

Contains very primitive "wrappers" around the adadvisor.com web service,
a non-RESTful interface.
"""


#import pandas as pd
#import numpy as np
from sys import stderr
import re
from urllib import quote
import requests
from fuzzywuzzy import process
from BeautifulSoup import BeautifulSoup as beatsoup

from pyaqadvisor.aqadvisor_assets import TANK_INFO, fish_species

def build_url(tank_dimensions, filter_data, fish_selection, fish_quantity, alreadyselected=""): # -> return URL
    """Creates the url string for call to aqadvisor; mimicking a RESTful API call."""
    uri_root   ="http://aqadvisor.com/AqAdvisor.php?"
    uri_params ="AquTankName=" +\
                "&AquListBoxTank=Choose" +\
                "&AquTankLength={AquTankLength}" +\
                "&AquTankDepth={AquTankDepth}" +\
                "&AquTankHeight={AquTankHeight}" +\
                "&AquListBoxFilter={AquListBoxFilter}" +\
                "&AquTextFilterRate={AquTextFilterRate}" +\
                "&AquListBoxFilter2=Choose" +\
                "&AquTextFilterRate2=N%2FA+" +\
                "&FormSubmit=Update" +\
                "&AquFilterString=" +\
                "&AquListBoxChooser={AquListBoxChooser}" +\
                "&AquTextBoxQuantity={AquTextBoxQuantity}" +\
                "&AquTextBoxRemoveQuantity=" +\
                "&AlreadySelected={AlreadySelected}" +\
                "&FilterMode=Display+all+species" +\
                "&AqTempUnit=F" +\
                "&AqVolUnit=gUS" +\
                "&AqLengthUnit=inch" +\
                "&AqSortType=cname" +\
                "&FilterQuantity=2" +\
                "&AqJuvMode=" +\
                "&AqSpeciesWindowSize=short" +\
                "&AqSearchMode=simple"
    uri_params = uri_params.format(AquTankLength=quote(tank_dimensions[0]),
                                   AquTankDepth=quote(tank_dimensions[1]),
                                   AquTankHeight=quote(tank_dimensions[2]),
                                   AquListBoxFilter=quote(filter_data[0]),
                                   AquTextFilterRate=quote(filter_data[1]),
                                   AquListBoxChooser=quote(fish_selection),
                                   AquTextBoxQuantity=quote(fish_quantity),
                                   AlreadySelected=quote(alreadyselected))
    uri = uri_root + uri_params
    print uri
    return uri

def call_aqadvisor(url):
    """ calls aqadvisor and returns the filtration capacity string AND already selected fish"""
    r = requests.get(url)
    returnval = None
    html_proc = None
    alreadyselected = None
    if r.status_code == 200: # yay success!
        # find relevant filtration info
        for line in r.text.split('\n'):
            m = re.search('Your aquarium filtration.*\\.', line)
            if m:
                returnval = m.group(0)

                html_proc = beatsoup(r.text)
        #if not html_proc: raise Exception, "html_proc is null"
        if html_proc:
            hiddeninput = html_proc.findAll('input', {'type':'hidden'})

            # extract already selected hidden form value
            for i in hiddeninput:
                if i['name'] == 'AlreadySelected':
                    alreadyselected =  i['value']

        if returnval:
            return returnval, alreadyselected
    else:
        raise Exception, "Could not complete the call to AqAdvisor.com.  HTTP Status Code was {0}".format(r.status_code)
    return "Could not complete call to AqAdvisor. Please try again later.", ""

def get_stocking_info(stocking_plan, ldh_dimensions, filter_data):
    """
    Calls out iteratively to aqadvisor to get stockin level and filtration level.

    Input:
        stocking_plan: dictionary { 'fish species name': quantity },
        ldh_dimensions: tuple of strings: ('48', '12', '20')
        filter_data: tuple of strings:  ('User Defined', '200')
    """

    my_already_selected = ""
    for species, quantity in stocking_plan.items():
        my_url = build_url(ldh_dimensions, filter_data, species, str(quantity), my_already_selected)
        try:
            msg, my_already_selected = call_aqadvisor(my_url)
        except requests.exceptions.ConnectionError:
            print >> stderr, "ConnectionError: Could not contact aqadvisor.com"
            return None
    return msg


if __name__ == '__main__':
    # Note: brute force dev/testing, use new API instead
    my_stocking = {
        process.extractOne("cardinal tetra", fish_species)[0]: '15',
        process.extractOne("pearl gourami", fish_species)[0]: '4',
        process.extractOne("panda cory", fish_species)[0]: '12',
        process.extractOne("espei rasbora", fish_species)[0]: '8',
        process.extractOne("lemon tetra", fish_species)[0]: '12',
    }
    my_ldh_dimensions = TANK_INFO['55g']
    my_filter_data = ('User Defined', '200')

    print get_stocking_info(my_stocking, my_ldh_dimensions, my_filter_data)

