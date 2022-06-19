# Note: dank.fusion-fall.py is meant to be run as an .exe by default, if you would like to execute the script, make the below changes...
#       - set mode = "exe"

from genericpath import isdir
from dankware import align, clr_banner, clr, cls
import requests
import time
import json
import sys
import os

mode = "script"
if mode == "script": filepath = os.path.dirname(__file__) # as .py
else:filepath = os.path.dirname(sys.argv[0]) # as .exe
os.chdir(filepath)

if mode == "script" and not os.path.exists("unitypack"):
    print(clr("\n  > ERROR: unitypack missing!",2))
    print(clr("  > Download it from: https://github.com/dongresource/UnityPackFF",2))
    print(clr("  > Exiting in 10s...",2))
    time.sleep(10); sys.exit()
from unitypack.asset import Asset

if not os.path.exists("dank.ff"): os.mkdir("dank.ff")
os.chdir("dank.ff")

try:
    from wand.image import Image
    from unitypack.modding import import_texture
    from unitypack.modding import import_mesh
    from unitypack.modding import import_audio
except:
    print(clr("\n  > ERROR: ImageMagick not installed!",2))
    choice = input(clr("  > Download Now? [y/n]: "))
    if choice.lower() == "y": print(clr("  > Downloading...")); download_name = "ImageMagick-7.1.0-37-Q16-HDRI-x64-dll.exe"; open(download_name,"wb").write(requests.get(f"https://download.imagemagick.org/ImageMagick/download/binaries/{download_name}").content); os.system(download_name)
    else: sys.exit()
    wait = input(clr("  > Hit [ENTER] after installing..."))
    from unitypack.modding import import_texture
    from unitypack.modding import import_mesh
    from unitypack.modding import import_audio

# Dependencies for ffextract.py
#import traceback
#from io import BytesIO
#from unitypack.export import OBJMesh
#from unitypack.environment import UnityEnvironment
#from collections import OrderedDict
#from unitypack.object import ObjectPointer
#from PIL import ImageOps

def main():

    sys.setrecursionlimit(10000)
    while True:
        banner = """

    ______  _______ __   _ _     _   _______ _______
    |     \ |_____| | \  | |____/    |______ |______
    |_____/ |     | |  \_| |    \_ . |       |      
                                                    

        """

        cls(); print(align(clr_banner(banner)))
        print(clr("  > [1] XDT Explorer"))
        print(clr("  > [0] Exit"))
        choice = input(clr("\n  > Choice: "))
        if choice == "1": cls(); print(align(clr_banner(banner))); one()
        if choice == "0": cls(); sys.exit()

def path_id(filename: str):
    data = str(xdtdata).split(filename)[1].split('path_id=')[1]
    id = ''
    for _ in data:
        if _ != ')' and _.isdigit(): id += _
        else: break
    print(clr(f"  > path_id: {id}"))

def one():
    
    global xdtdata
    cab_path = input(clr('  > Drag and Drop Custom Asset Bundle: ')).replace('"','')
    index = int(input(clr('  > TableData Object Index: ')))
    cab_name = str(cab_path.split('\\')[-1])
    print(clr(f"  > tabledata = Asset.from_file(open('{cab_path}', 'rb'))"))
    tabledata = Asset.from_file(open(cab_path, 'rb'))
    print(clr(f"  > xdtdata = tabledata.objects[{index}].contents"))
    xdtdata = tabledata.objects[index].contents
    print(clr("\n  > Pre-defined functions: save, dump-xdt, path_id('filename'), exit\n")) # add extract

    while True:
        cmd = input(clr("  > ")); print()
        if cmd.lower() == "exit": break
        elif cmd.lower() == "save":
            tabledata.save(open(cab_name,'wb'))
        elif cmd.lower() == "dump-xdt":
            out = {}
            for tname, table in xdtdata.items():
                out[tname] = {}
                try:
                    for dname, data in table.items(): out[tname][dname] = data
                except: out[tname] = "<err>"
            json.dump(out, open("xdt.json", "w+"), indent=4)
        #elif cmd.lower() == "extract":
        #    counter = 1
        #    while os.path.exists(f"{cab_name}_{counter}"): counter += 1
        #    sys.argv.append(cab_path.replace(cab_name,'')); sys.argv.append(f"{cab_name}_{counter}")
        #    exec(open(f"{os.path.dirname(__file__)}\\ffextract.py","r").read())
        else:
            try: exec(cmd)
            except Exception as err: print(clr(f"  > ERROR: {err}",2))
            print()

if __name__ == "__main__":
    main()
