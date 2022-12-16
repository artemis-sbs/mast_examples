import sys
import os
dir = os.path.dirname(__file__) 
for filename in os.listdir(dir): 
    f = os.path.join(dir, filename) 
    basename, ext = os.path.splitext(filename) 
    # checking if it is a file 
    if os.path.isfile(f): 
        if ext == ".sbslib": 
            print(f'importing lib {f}')
            sys.path.insert(0, f) 


from sbs_utils.mast.maststory import MastStory
mast = MastStory()

n = len(sys.argv)
if n == 2:
    errors = mast.from_file(dir+sys.argv[1])
    for error in errors:
         print(error)

