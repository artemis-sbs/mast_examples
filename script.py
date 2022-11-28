import sbslibs
from  sbs_utils.handlerhooks import *

from sbs_utils.gui import Gui
from sbs_utils.mast.maststoryscheduler import StoryPage
from sbs_utils.mast.mast import Mast
import sbs

@Mast.make_global
class MyClass:
    def func():
        print("class member")

@Mast.make_global
def create_map(mast_scheduler):
    sim = mast_scheduler.sim
    artemis = mast_scheduler.PlayerShip().spawn(sim, 0, 0, 0,"Artemis", "tsn", "Battle Cruiser").py_object
    hera = mast_scheduler.PlayerShip().spawn(sim, 0, 0, 0,"Hera", "tsn", "Battle Cruiser").py_object
    atlas = mast_scheduler.PlayerShip().spawn(sim, 0, 0, 0,"Atlas", "tsn", "Battle Cruiser").py_object
    sbs.assign_client_to_ship(0, artemis.id)
    Mast.make_global_var("artemis", artemis)
    Mast.make_global_var("hera", hera)
    Mast.make_global_var("atlas", atlas)

class MyStoryPage(StoryPage):
    story_file = "story.mast"
    #story_file = "examples/credits.mast"
    #story_file = "examples/bar.mast"
    #story_file = "examples/joke.mast"
    #story_file = "examples/consoles.mast"

Gui.server_start_page_class(MyStoryPage)
Gui.client_start_page_class(MyStoryPage)



