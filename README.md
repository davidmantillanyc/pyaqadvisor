# pyaqadvisor
Python API to AqAdvisor.com

## Context

Approximately 10% of American households have fish as pets.  
It is estimated that 95% of fish deaths can be attributed to improper housing
or nutrition.  Many times fish are sold or given away without any guidance to
the new pet owner, such as goldfish giveaways at carnivals or at birthdays.
Some fish have myths associated with them, such as the betta fish (siamese
fighting fish) that supposedly can live in dirty water in small bowls.

AqAdvisor.com is a website that helps aquarists plan how to stock their fish
tank.  Users specify their tank size, their filtration, and what fish they
intend to keep in the tank.  The site will calculate the stocking level and
filtration capacity given the inputs.  This is a useful tool to get a rough
estimate on a fish tank's stocking level, it even lets you know whether the
fish are compatible with one another, if you have more than one species in the
tank.  AqAdvisor is sometimes criticized for "not being accurate", so the
output generated should be not be treated as gospel; nonetheless, it gives a
reasonable starting point, and is generally very useful for beginner
fishkeepers.  

## Why I created this tool

I started using AqAdvisor and got annoyed at the archaic design. It's not a
RESTful API, it's a clunky web site that takes a while to load.  I was doing
lots of research and found myself wanting a better useful experience. I also
had some free time on my hands one long holiday weekend so I decided to give
myself a little programming exercise of creating a python API to the site.


## How to use the tool

The easiest way to use the tool is to use the ipython notebook as a starting
point.  First, create a stocking, then a tank, and then make a call to the
AqAdvisor service.  Because of the clunky web interface, multiple calls to
AqAdvisor.com must be made if you want to have more than one fish species in a
tank (as is would be the case for a community tank).  The auto-generated
AqAdvisor URL will be printed for each call out to the website. This is useful
in case you want to jump over to the web UI, you can just copy and paste the
URL into your web browser and continue from there.

Use the common (English) name for the fish you are looking for.  PyAqAdvisor
will do a "fuzzy match" to AqAdvisor's species list and match the closet one.
This way you can specify your stocking list as "cardinal tetra" and not worry
about the scientic name. 

Please look at ``examples/example.py`` and  ``examples/example.ipynb`` for more information.

If you are looking for an extensive list of fish species, checkout
``aqadvisor_assets.py``. 

## Note

PyAqAdvisor currently only works for freshwater fish species.  If you are
interested in saltwater fish, please contact me.

This tool was handcrafted using a combination of vi and ipython.



