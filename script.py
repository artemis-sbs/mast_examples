import sbslibs
from  sbs_utils.handlerhooks import *

from sbs_utils.gui import Gui
from sbs_utils.mast.maststoryscheduler import StoryPage


class MyStoryPage(StoryPage):
    story_file = "story.mast"
    #story_file = "examples/credits.mast"
    #story_file = "examples/bar.mast"
    #story_file = "examples/joke.mast"
    #story_file = "examples/consoles.mast"

Gui.server_start_page_class(MyStoryPage)
Gui.client_start_page_class(MyStoryPage)



