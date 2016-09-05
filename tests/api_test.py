import unittest

import pyaqadvisor
from pyaqadvisor.fishyparser import build_url
from pyaqadvisor.api import Stocking, Tank


class TestAPI(unittest.TestCase):

    def setUp(self):
        pass

    def test_stocking(self):
        test_input = [('cardinal_tetra', 5), ('cory panda', 6), ('lemon_tetra', 12), ('pearl gourami', 4)]
        expected_output = {'Pearl Gourami (Trichogaster leerii)': 4, 'Lemon Tetra (Hyphessobrycon pulchripinnis)': 12, 'Cardinal Tetra (Paracheirodon axelrodi)': 5, 'Adolfo Cory (Corydoras adolfoi)': 6}

        s = Stocking()
        for i in test_input:
            s.add(i[0], i[1])
        actual_output = s.aqadvisor_stock_list
        self.assertEquals(expected_output, actual_output)

    def test_build_url(self):
        expected_output = """http://aqadvisor.com/AqAdvisor.php?AquTankName=&AquListBoxTank=Choose&AquTankLength=20&AquTankDepth=10&AquTankHeight=12&AquListBoxFilter=Aquaclear%2030&AquTextFilterRate=30&AquListBoxFilter2=Choose&AquTextFilterRate2=N%2FA+&FormSubmit=Update&AquFilterString=&AquListBoxChooser=Cardinal%20Tetra%20%28Paracheirodon%20axelrodi%29&AquTextBoxQuantity=5&AquTextBoxRemoveQuantity=&AlreadySelected=&FilterMode=Display+all+species&AqTempUnit=F&AqVolUnit=gUS&AqLengthUnit=inch&AqSortType=cname&FilterQuantity=2&AqJuvMode=&AqSpeciesWindowSize=short&AqSearchMode=simple"""

        t = Tank('10g').add_filter("AquaClear 30").add_stocking(Stocking().add('cardinal tetra', 5))
        aq_stocking = t.stocking.aqadvisor_stock_list.items()[0]
        actual_output = build_url(t.ldh, t.filter_, aq_stocking[0], str(aq_stocking[1]), alreadyselected="")
        self.assertEquals(expected_output, actual_output)

    def test_tank(self):
        t = Tank('10g').add_filter("AquaClear 30").add_stocking(Stocking().add('cardinal tetra', 5).add('panda cory', 5))
        self.assertEquals(t.stocking.stock_list,  {'panda cory': 5, 'cardinal tetra': 5})
        self.assertEquals(t.length, '20')
        self.assertEquals(t.depth, '10')
        self.assertEquals(t.height, '12')
        self.assertEquals(t.ldh, ('20', '10', '12'))
        self.assertEquals(t.filter_, ('Aquaclear 30', '30'))
        self.assertEquals(str(t), "<Tank: 10g with Aquaclear 30>")

    def test_call_aqadvisor(self):
        import requests
        expected_output = """Your aquarium filtration capacity for above selected species is <b>194%</b>.<A HREF=AqHelp.php#FiltrationCapacity target=_blank><img border=0 alt="Help on Filtration capacity" src=Images/Question11.png></A><BR>Recommended water change schedule: <b>28"""
        t = Tank('10g').add_filter("AquaClear 30").add_stocking(Stocking().add('cardinal tetra', 5).add('panda cory', 5))
        try:
            actual_output = t.get_stocking_level()
            self.assertTrue(actual_output.startswith(expected_output)) # NOTE: we are clipping result due to Facebook message length limit
        except requests.exceptions.ConnectionError:
            import sys
            # NOTE: Should probably make this more pythonic
            print >> sys.stderr, "ERROR: Could not connect to aqadvisor.com. Test will silently fail. Please check your internet connection."
            #self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()

