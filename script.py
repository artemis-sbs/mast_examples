import sbslibs
from  sbs_utils.handlerhooks import *

from sbs_utils.gui import Gui
from sbs_utils.mast.maststoryscheduler import StoryPage
from sbs_utils.mast.mast import Mast
import sbs
from sbs_utils import faces
from sbs_utils.query import role, link, to_object_list
from sbs_utils.spaceobject import SpaceObject
from sbs_utils.scatter import sphere
from random import randrange, choice

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
    

    # (count, x, y, z, r, outer=0, top_only=False, ring=False):
    # extra count doesn't matter
    friendly_pos  = sphere(5000, 0,0, 0, 2000, 4500,False, True)
    
    
    resource_types = ["Gold", "Gas", "Titanium"]
    for ds in range(randrange(2,5)):
        ds1 = mast_scheduler.Npc().spawn(sim, *next(friendly_pos),f"DS{ds}", "tsn", "Starbase", "behav_station").py_object
        ds1.add_role("Station")
        for r in resource_types:
            ds1.set_inventory_value(r, randrange(10, 20)*100)
        faces.set_face(ds1.id, faces.random_torgoth())

    for station in to_object_list(role("Station")):
        for player in to_object_list(role("__PLAYER__")):
            player.start_task("player_comms_station", {"station": station})

    for hr in range(randrange(3,5)):
        hr1 = mast_scheduler.Npc().spawn(sim, *next(friendly_pos), f"HR_{hr}", "tsn", "Cargo", "behav_npcship").py_object
        hr1.add_role("Harvester")
        hr1.set_inventory_value("storage", 0)
        hr1.set_inventory_value("storing", choice(resource_types))
        faces.set_face(hr1.id, faces.random_terran())
        hr1.start_task("harvester_patrol")

    for hr in range(randrange(3,6)):
        fr1 = mast_scheduler.Npc().spawn(sim, *next(friendly_pos), f"TSN_{randrange(99)}", "tsn", "Light Cruiser", "behav_npcship").py_object
        fr1.add_role("Friendly")
        faces.set_face(fr1.id, faces.random_terran())
        fr1.start_task("friendly_patrol")

    
    terrain_pos  = sphere(randrange(4,10), 0,0, 0, 3500, 6000,False, True)
    for center in terrain_pos:
        cluster_pos  = sphere(randrange(4,10), *center, 2000,False, True)
        for cluster in cluster_pos:
            resource = None
            if randrange(4) == 1: # 1 in four :)
                resource = choice(resource_types)
                cluster.y = 0
            ter1 = mast_scheduler.Npc().spawn(sim, *cluster, resource,None, "Asteroid 1", "behav_asteroid").py_object
            if resource is not None:
                ter1.add_role("ResourceAsteroid")
                ter1.add_role(resource)
                ter1.set_inventory_value("amount", randrange(10, 20)*100)
            faces.set_face(ter1.id, faces.random_terran(civilian=True))

    # create a link from all harvesters to all Stations
    link(role("Friendly"), "Visit", role("Station"))
    create_wave(mast_scheduler, 4)

#@Mast.make_global
def create_wave(mast_scheduler, count):
    sim = mast_scheduler.sim
    enemy_pos  = sphere(5000, 0,0, 0, 7000, 8000,False, True)
    enemy_ships = ["Hunter", "Battleship", "Dreadnaught", "Goliath", "Leviathan", "Behemoth"]
    markers = "QKWR"
    for _ in range(randrange(3,count)):
        marker = f"{choice(markers)}_{randrange(99)}"
        ship = randrange(len(enemy_ships))
        raid= mast_scheduler.Npc().spawn(sim, *next(enemy_pos), marker, "raider", enemy_ships[ship], "behav_npcship").py_object

        if ship == 0:
            faces.set_face(raid.id, faces.random_skaraan())
        elif ship < 3:
            faces.set_face(raid.id, faces.random_kralien())
        else:
            faces.set_face(raid.id, faces.random_torgoth())
    

Mast.make_global_var("create_wave", create_wave)    

class MyStoryPage(StoryPage):
    #story_file = "story.mast"
    #story_file = "examples/credits.mast"
    #story_file = "examples/bar.mast"
    #story_file = "examples/joke.mast"
    story_file = "examples/add_cargo.mast"

Gui.server_start_page_class(MyStoryPage)
Gui.client_start_page_class(MyStoryPage)


