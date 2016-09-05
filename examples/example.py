"""
example.py


"""

from pyaqadvisor import Tank, Stocking

if __name__ == '__main__':

    stocking = Stocking().add('cardinal tetra', 5)\
                         .add('panda cory', 6)\
                         .add('lemon_tetra', 12)\
                         .add('pearl gourami', 4)

    print "My user-specified stocking is: ", stocking
    print "I translate this into: ", stocking.aqadvisor_stock_list


    t = Tank('55g').add_filter("AquaClear 30").add_stocking(stocking)
    print "My tank looks like",
    print t, t.stocking, t.length, t.depth, t.height, t.filter_
    print
    print "Aqadvisor tells me: ",
    print t.get_stocking_level()
