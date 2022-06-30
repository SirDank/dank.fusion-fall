from dankware import align, clr_banner, clr, cls, magenta, white
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
#from PIL.ImageOps import flip
#from collections import OrderedDict
#from unitypack.export import OBJMesh
#from unitypack.object import ObjectPointer
#from unitypack.environment import UnityEnvironment

# functionality

def logger(string: str) -> str:
    global log
    log += string + "\n"
    return string

def path_id(filename: str):
    data = str(xdtdata).split(filename)[1].split('path_id=')[1]
    id = ''
    for _ in data:
        if _ != ')' and _.isdigit(): id += _
        else: break
    print(clr(f"  > path_id: {id}"))

def dump_xdt():
    output = {}
    for tname, table in xdtdata.items():
        output[tname] = {}
        try:
            for dname, data in table.items(): output[tname][dname] = data
        except: output[tname] = "<err>"
    json.dump(output, open("xdt.json", "w+"), indent=4)

def shortcut(mode, cmd, to_exec):
    if mode == 1:
        if "=" not in cmd: exec(f"print({to_exec})".replace('index', cmd))
        else: cmd = cmd.split(' = '); exec(to_exec.replace('index',cmd[0]) + f" = \"{cmd[1]}\"")
    elif mode == 2:
        if len(cmd) == 1: exec(f"print({to_exec})".replace('index', cmd[0]))
        else: exec(to_exec.replace('index',cmd[0]) + f" = \"{cmd[1]}\"")
    print()

# main

def one():
    
    global xdtdata
    cab_path = input(clr('  > Drag and Drop Custom Asset Bundle: ')).replace('"','')
    index = int(input(clr('  > TableData Object Index: ')))
    cab_name = str(cab_path.split('\\')[-1])
    print(clr(logger(f"  > tabledata = Asset.from_file(open('{cab_path}', 'rb'))")))
    tabledata = Asset.from_file(open(cab_path, 'rb'))
    print(clr(logger(f"  > xdtdata = tabledata.objects[{index}].contents")))
    xdtdata = tabledata.objects[index].contents
    print(clr("\n  > Pre-defined commands: dump-xdt, path_id('filename'), help, log, save, save-all, exit\n"))

    while True:
        cmd = logger(input(f"  {magenta}> {white}")); print(); cmd_lower = cmd.lower()
        if cmd_lower == "exit": break
        elif cmd_lower == "dump-xdt": dump_xdt()
        elif cmd_lower == "log": open("log.txt","w+").write(log)
        elif cmd_lower == "save": tabledata.save(open(cab_name,'wb'))
        elif cmd_lower == "save-all": dump_xdt(); open("log.txt","w+").write(log); tabledata.save(open(cab_name,'wb'))
        elif cmd_lower == "help":
            print(clr("""  > Available Shortcuts With Examples:\n
  - aswap example-sound.wav 1 example-sound > import_audio(xdtdata,'example-sound.wav',2,'example-sound')
  - tswap example-texture.png example-texture > import_texture(xdtdata,'example-texture.png','example-texture')
  - npc-name 3148 > print(xdtdata['m_pNpcTable']['m_pNpcStringData'][3148]['m_strName'])
  - npc-name 3148 = test name > xdtdata['m_pNpcTable']['m_pNpcStringData'][3148]['m_strName'] = \"test name\"
  - mesh 344 > print(xdtdata['m_pNpcTable']['m_pNpcMeshData'][344]['m_pstrMMeshModelString'])
  - mesh 344 fusion_cheese > xdtdata['m_pNpcTable']['m_pNpcMeshData'][344]['m_pstrMMeshModelString'] = \"fusion_cheese\"
  - texture 344 > print(xdtdata['m_pNpcTable']['m_pNpcMeshData'][344]['m_pstrMTextureString'])
  - texture 344 fusion_cheese > xdtdata['m_pNpcTable']['m_pNpcMeshData'][344]['m_pstrMTextureString'] = \"fusion_cheese\"
  - meshid 2677 > print(xdtdata['m_pNpcTable']['m_pNpcData'][2675]['m_iMesh'])
  - meshid 2675 2671 > xdtdata['m_pNpcTable']['m_pNpcData'][2675]['m_iMesh'] = 2671
  - m-info > print(xdtdata['m_pMissionTable']['m_pMissionData'][1])
  - m-npc 1 > print(xdtdata['m_pMissionTable']['m_pMissionData'][1]['m_iHNPCID'])
  - m-npc 1 2671 > xdtdata['m_pMissionTable']['m_pMissionData'][1]['m_iHNPCID'] = NPC_INDEX#
  - m-task 1 > print(xdtdata['m_pMissionTable']['m_pMissionData'][1]['m_iHTaskID'])
  - m-task 1 2 > xdtdata['m_pMissionTable']['m_pMissionData'][1]['m_iHTaskID'] = 2
  - m-tasknext 1 > print(xdtdata['m_pMissionTable']['m_pMissionData'][1]['m_iSUOutgoingTask'])
  - m-tasknext 1 2 > xdtdata['m_pMissionTable']['m_pMissionData'][1]['m_iSUOutgoingTask'] = 2
  - m-string 11666 > print(xdtdata['m_pMissionTable']['m_pMissionStringData'][11666])
  - m-string 11666 = dee dee's herb garden > xdtdata['m_pMissionTable']['m_pMissionStringData'][11666] = \"dee dee's herb garden\"\n"""))
        elif cmd_lower.startswith('m-info '): print(xdtdata['m_pMissionTable']['m_pMissionData'][int(cmd.replace('m-info ',''))])
        elif cmd_lower.startswith('aswap '): cmd = cmd.replace('aswap ','').split(' '); import_audio(xdtdata, cmd[0], int(cmd[1]), cmd[2])
        elif cmd_lower.startswith('tswap '): cmd = cmd.replace('tswap ','').split(' '); import_texture(xdtdata, cmd[0], cmd[1])
        elif cmd_lower.startswith('npc-name '): cmd = cmd.replace('npc-name ',''); to_exec = "xdtdata['m_pNpcTable']['m_pNpcStringData'][index]['m_strName']"; shortcut(1, cmd, to_exec)
        elif cmd_lower.startswith('mesh '): cmd = cmd.replace('mesh ','').split(' '); to_exec = "xdtdata['m_pNpcTable']['m_pNpcMeshData'][index]['m_pstrMMeshModelString']"; shortcut(2, cmd, to_exec)
        elif cmd_lower.startswith('texture '): cmd = cmd.replace('texture ','').split(' '); to_exec = "xdtdata['m_pNpcTable']['m_pNpcMeshData'][index]['m_pstrMTextureString']"; shortcut(2, cmd, to_exec)
        elif cmd_lower.startswith('meshid '): cmd = cmd.replace('meshid ','').split(' '); to_exec = "xdtdata['m_pNpcTable']['m_pNpcData'][index]['m_iMesh']"; shortcut(2, cmd, to_exec)
        elif cmd_lower.startswith('m-npc '): cmd = cmd.replace('m-npc ','').split(' '); to_exec = "xdtdata['m_pMissionTable']['m_pMissionData'][index]['m_iHNPCID']"; shortcut(2, cmd, to_exec)
        elif cmd_lower.startswith('m-task '): cmd = cmd.replace('m-task ','').split(' '); to_exec = "xdtdata['m_pMissionTable']['m_pMissionData'][index]['m_iHTaskID']"; shortcut(2, cmd, to_exec)
        elif cmd_lower.startswith('m-tasknext '): cmd = cmd.replace('m-tasknext ','').split(' '); to_exec = "xdtdata['m_pMissionTable']['m_pMissionData'][index]['m_iSUOutgoingTask']"; shortcut(2, cmd, to_exec)
        elif cmd_lower.startswith('m-string '): cmd = cmd.replace('m-string ',''); to_exec = "xdtdata['m_pMissionTable']['m_pMissionStringData'][index]"; shortcut(1, cmd, to_exec)
        else:
            try: exec(cmd)
            except Exception as err: print(clr(f"  > ERROR: {err}",2))
            print()

'''def two():
    
    cab_path = input(clr('  > Drag and Drop Custom Asset Bundle: ')).replace('"','')
    cab_name = str(cab_path.split('\\')[-1])
    counter = 1
    while os.path.exists(f"{cab_name}_{counter}"): counter += 1
    sys.argv.append(cab_path.replace(cab_name,'')); sys.argv.append(f"{cab_name}_{counter}")
    exec(open(f"{os.path.dirname(__file__)}\\ffextract.py","r").read())
    sys.argv.remove(cab_path.replace(cab_name,'')); sys.argv.remove(f"{cab_name}_{counter}")
    print(clr("\n  > Extraction Complete! Sleeping 10s..."))
    time.sleep(10)'''

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
        #print(clr("  > [2] Extract")) ###
        print(clr("  > [0] Exit"))
        choice = input(clr("\n  > Choice: "))
        if choice == "1": cls(); print(align(clr_banner(banner))); one()
        #elif choice == "2": cls(); print(align(clr_banner(banner))); two() ###
        elif choice == "0": cls(); sys.exit()

if __name__ == "__main__": log = ""; main()
