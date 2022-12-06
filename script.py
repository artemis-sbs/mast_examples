import sbslibs
from  sbs_utils.handlerhooks import *

from sbs_utils.gui import Gui
from sbs_utils.mast.maststoryscheduler import StoryPage
from sbs_utils.mast.mast import Mast
import sbs
from sbs_utils import faces
from sbs_utils.spaceobject import SpaceObject

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

    faces.set_face(artemis.id, faces.random_terran_male())
    faces.set_face(hera.id, faces.random_terran_female())
    faces.set_face(atlas.id, faces.random_terran_fluid())
    ds1 = mast_scheduler.Npc().spawn(sim, 1000, 0, 0,"ds1", "tsn", "Starbase", "behav_station").py_object
    ds1.add_role("Station")
    faces.set_face(ds1.id, faces.random_torgoth())
    Mast.make_global_var("ds1", ds1)

    for station in SpaceObject.get_role("Station"):
        for player in SpaceObject.get_role("__PLAYER__"):
            player.start_task("artemis_comms_ds1", {"station": station})
    

class MyStoryPage(StoryPage):
    #story_file = "story.mast"
    #story_file = "examples/credits.mast"
    #story_file = "examples/bar.mast"
    #story_file = "examples/joke.mast"
    story_file = "examples/add_comms.mast"

Gui.server_start_page_class(MyStoryPage)
Gui.client_start_page_class(MyStoryPage)



