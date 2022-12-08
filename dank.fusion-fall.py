import os
import sys
import json
import time
import shutil
import requests
from dankware import align, clr_banner, clr, cls, magenta, white, green, reset, chdir, err

exec_mode = "script"
exec(chdir(exec_mode))
try: os.mkdir("dank.ff")
except: pass
os.chdir("dank.ff")

if exec_mode == "script" and not os.path.exists("unitypack"):

    print(clr("\n  > ERROR: unitypack folder missing!",2))
    print(clr("  > Download it from: https://github.com/dongresource/UnityPackFF",2))
    print(clr("  > [NOTE] UnityPackFF is slightly modified for dank.ff",2))
    print(clr("  > Exiting in 10s...",2))
    time.sleep(10); sys.exit()

from unitypack.asset import Asset

try:

    from wand.image import Image
    from unitypack.modding import import_texture, import_mesh, import_audio
    from unitypack.object import FFOrderedDict, ObjectPointer
    from unitypack.export import OBJMesh

except:

    print(clr("\n  > ERROR: ImageMagick not installed!",2))

    choice = input(clr("  > Download Now? [y/n]: "))
    if choice.lower() == "y":
    
        print(clr("  > Downloading..."))
        download_name = "ImageMagick-7.1.0-37-Q16-HDRI-x64-dll.exe"
        open(download_name,"wb").write(requests.get(f"https://www.islandmediaarts.ca/{download_name}").content)
        os.system(download_name)

    else: sys.exit()

    input(clr("  > Hit [ENTER] after installing... "))
    from unitypack.modding import import_texture, import_mesh, import_audio
    from unitypack.object import FFOrderedDict, ObjectPointer
    from unitypack.export import OBJMesh

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

    id = ''; data = str(xdtdata).split(filename)[1].split('path_id=')[1]
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

def fix_bundles():

    try: os.mkdir("bundles_to_fix"); input(clr("  > Created bundles_to_fix folder! Hit [ENTER] after adding your files... "))
    except: pass
    try: os.mkdir("fixed_bundles")
    except: pass

    bundles = os.listdir("bundles_to_fix")
    for bundle in bundles:
        original_bytes = open(f"bundles_to_fix/{bundle}", 'rb').read()
        modded_bytes = b'UnityWeb' + original_bytes[original_bytes.find(b'\x00'):]
        open(f"fixed_bundles/{bundle}", 'wb+').write(modded_bytes)

    shutil.rmtree("bundles_to_fix"); print(clr(f"\n  > Fixed [{len(bundles)}] bundles!\n"))

def tswap_mass(dxt_mode):

    try: os.mkdir("tswap_textures"); input(clr("  > Created tswap_textures folder! Hit [ENTER] after adding your files... "))
    except: pass

    textures = os.listdir("tswap_textures")
    for texture in textures:
        try: import_texture(xdtdata, f"tswap_textures/{texture}", texture.split('.')[0], f'dxt{dxt_mode}')
        except: print(clr(err(sys.exc_info()), 2))
        
    print(clr(f"\n  > Imported [{len(textures)}] textures!\n"))

def shortcut(mode, cmd, to_exec):

    if mode == 1:
        if "=" not in cmd: exec(f"print({to_exec})".replace('index', cmd))
        else: cmd = cmd.split(' = '); exec(to_exec.replace('index',cmd[0]) + f" = \"{cmd[1]}\"")
    elif mode == 2: 
        if len(cmd) == 1: exec(f"print({to_exec})".replace('index', cmd[0]))
        else: exec(to_exec.replace('index',cmd[0]) + f" = \"{cmd[1]}\"")
    elif mode == 3:
        exec(to_exec)
    print()

# main

def one():
    
    global tabledata, xdtdata

    cab_path = input(clr('  > Drag and Drop Custom Asset Bundle: ') + green).replace('"','')
    index = int(input(clr('  > TableData Object Index: ') + green))
    cab_name = str(cab_path.split('\\')[-1])
    print(clr(logger(f"  > tabledata = Asset.from_file(open('{cab_path}', 'rb'))")))
    tabledata = Asset.from_file(open(cab_path, 'rb'))
    print(clr(logger(f"  > xdtdata = tabledata.objects[{index}].contents")))
    xdtdata = tabledata.objects[index].contents
    print(clr("\n  > Pre-defined commands: dump-xdt, path_id('filename'), fix-bundles, help, log, save, save-all, exit\n"))

    while True:
        try:
            cmd = logger(input(f"  {magenta}> {green}")); print(reset); cmd_lower = cmd.lower()
            if cmd_lower == "help":

                print(clr("""  > Available Shortcuts With Examples:\n
 - aimport sound.wav 22.5 sound  >  new_audio = tabledata.add_object(83); import_audio(new_audio.contents,'sound.wav',22.5,'sound'); tabledata.add2ab('sound.wav',new_audio.path_id)
 - aswap sound.wav 22.5 sound  >  import_audio(xdtdata,'sound.wav',22.5,'sound')
 - export example.obj  >  open('example.obj','w').write(OBJMesh(xdtdata).export())
 - imesh npc_alienx.obj npc_alienx  >  import_mesh(xdtdata, 'npc_alienx.obj', 'npc_alienx')
 - ms-info  >  print(xdtdata['m_pMissionTable']['m_pMissionData'][1])
 - ms-npc 1 2671  >  xdtdata['m_pMissionTable']['m_pMissionData'][1]['m_iHNPCID'] = NPC_INDEX#
 - ms-npc 1  >  print(xdtdata['m_pMissionTable']['m_pMissionData'][1]['m_iHNPCID'])
 - ms-string 11666 = dee dee's herb garden  >  xdtdata['m_pMissionTable']['m_pMissionStringData'][11666] = \"dee dee's herb garden\"
 - ms-string 11666  >  print(xdtdata['m_pMissionTable']['m_pMissionStringData'][11666])
 - ms-task 1 2  >  xdtdata['m_pMissionTable']['m_pMissionData'][1]['m_iHTaskID'] = 2
 - ms-task 1  >  print(xdtdata['m_pMissionTable']['m_pMissionData'][1]['m_iHTaskID'])
 - ms-tasknext 1 2  >  xdtdata['m_pMissionTable']['m_pMissionData'][1]['m_iSUOutgoingTask'] = 2
 - ms-tasknext 1  >  print(xdtdata['m_pMissionTable']['m_pMissionData'][1]['m_iSUOutgoingTask'])
 - mesh 344  >  print(xdtdata['m_pNpcTable']['m_pNpcMeshData'][344]['m_pstrMMeshModelString'])
 - mesh 344 fusion_cheese  >  xdtdata['m_pNpcTable']['m_pNpcMeshData'][344]['m_pstrMMeshModelString'] = \"fusion_cheese\"
 - meshid 2675 2671  >  xdtdata['m_pNpcTable']['m_pNpcData'][2675]['m_iMesh'] = 2671
 - meshid 2677  >  print(xdtdata['m_pNpcTable']['m_pNpcData'][2675]['m_iMesh'])
 - npc-name 3148 = test name  >  xdtdata['m_pNpcTable']['m_pNpcStringData'][3148]['m_strName'] = \"test name\"
 - npc-name 3148  >  print(xdtdata['m_pNpcTable']['m_pNpcStringData'][3148]['m_strName'])
 - objects 1 1000  >  for _ in range(1,1000): print(f'{_} - {tabledata.objects[_].contents}')
 - texture 344  >  print(xdtdata['m_pNpcTable']['m_pNpcMeshData'][344]['m_pstrMTextureString'])
 - texture 344 fusion_cheese  >  xdtdata['m_pNpcTable']['m_pNpcMeshData'][344]['m_pstrMTextureString'] = \"fusion_cheese\"
 - timport texture.png texture 1  >  new_texture = tabledata.add_object(28); import_texture(new_texture._contents,'texture.png','texture','dxt1'); tabledata.add2ab('texture.png',new_texture.path_id)
 - timport texture.png texture 5  >  new_texture = tabledata.add_object(28); import_texture(new_texture._contents,'texture.png','texture','dxt5'); tabledata.add2ab('texture.png',new_texture.path_id)
 - tswap texture.png texture 1  >  import_texture(xdtdata,'texture.png','texture','dxt1')
 - tswap texture.png texture 5  >  import_texture(xdtdata,'texture.png','texture','dxt5')
 - tswap-mass 1  >  mass import_texture (fmt='dxt1')
 - tswap-mass 5  >  mass import_texture (fmt='dxt5')\n"""))
            
            elif cmd_lower == "exit": break
            elif cmd_lower == "dump-xdt": 
                try: dump_xdt()
                except: print(clr(err(sys.exc_info()), 2))
            elif cmd_lower == "fix-bundles": fix_bundles()
            elif cmd_lower == "log": open("log.txt","w+").write(log)
            elif cmd_lower == "save":
                try: os.remove(cab_name)
                except: pass
                try: tabledata.save(open(cab_name,'wb'))
                except: print(clr(err(sys.exc_info()), 2))
            elif cmd_lower == "save-all":
                try: dump_xdt()
                except: print(clr(err(sys.exc_info()), 2)); continue
                open("log.txt","w+").write(log)
                try: os.remove(cab_name)
                except: pass
                try: tabledata.save(open(cab_name,'wb'))
                except: print(clr(err(sys.exc_info()), 2)) 

            elif cmd_lower.startswith('aimport '): cmd = cmd.replace('aimport ','').split(' '); new_audio = tabledata.add_object(83); import_audio(new_audio.contents,cmd[0],int(cmd[1]),cmd[2]); tabledata.add2ab(cmd[0],new_audio.path_id)
            elif cmd_lower.startswith('aswap '): cmd = cmd.replace('aswap ','').split(' '); import_audio(xdtdata, cmd[0], int(cmd[1]), cmd[2])
            elif cmd_lower.startswith('export '): cmd = cmd.replace('export ','').replace(' ',''); open(cmd,'w').write(OBJMesh(xdtdata).export())
            elif cmd_lower.startswith('imesh '): cmd = cmd.replace('imesh ','').split(' '); import_mesh(xdtdata, cmd[0], cmd[1])
            elif cmd_lower.startswith('ms-info '): print(xdtdata['m_pMissionTable']['m_pMissionData'][int(cmd.replace('ms-info ',''))])
            elif cmd_lower.startswith('ms-npc '): cmd = cmd.replace('ms-npc ','').split(' '); to_exec = "xdtdata['m_pMissionTable']['m_pMissionData'][index]['m_iHNPCID']"; shortcut(2, cmd, to_exec)
            elif cmd_lower.startswith('ms-string '): cmd = cmd.replace('ms-string ',''); to_exec = "xdtdata['m_pMissionTable']['m_pMissionStringData'][index]"; shortcut(1, cmd, to_exec)
            elif cmd_lower.startswith('ms-task '): cmd = cmd.replace('ms-task ','').split(' '); to_exec = "xdtdata['m_pMissionTable']['m_pMissionData'][index]['m_iHTaskID']"; shortcut(2, cmd, to_exec)
            elif cmd_lower.startswith('ms-tasknext '): cmd = cmd.replace('ms-tasknext ','').split(' '); to_exec = "xdtdata['m_pMissionTable']['m_pMissionData'][index]['m_iSUOutgoingTask']"; shortcut(2, cmd, to_exec)
            elif cmd_lower.startswith('mesh '): cmd = cmd.replace('mesh ','').split(' '); to_exec = "xdtdata['m_pNpcTable']['m_pNpcMeshData'][index]['m_pstrMMeshModelString']"; shortcut(2, cmd, to_exec)
            elif cmd_lower.startswith('meshid '): cmd = cmd.replace('meshid ','').split(' '); to_exec = "xdtdata['m_pNpcTable']['m_pNpcData'][index]['m_iMesh']"; shortcut(2, cmd, to_exec)
            elif cmd_lower.startswith('npc-name '): cmd = cmd.replace('npc-name ',''); to_exec = "xdtdata['m_pNpcTable']['m_pNpcStringData'][index]['m_strName']"; shortcut(1, cmd, to_exec)
            elif cmd_lower.startswith('objects '): cmd = cmd.replace('objects ','').split(' '); to_exec = f"for _ in range({cmd[0]},{cmd[1]}): print(f'{{_}} - {{tabledata.objects[_].contents}}')"; shortcut(3, cmd, to_exec)
            elif cmd_lower.startswith('texture '): cmd = cmd.replace('texture ','').split(' '); to_exec = "xdtdata['m_pNpcTable']['m_pNpcMeshData'][index]['m_pstrMTextureString']"; shortcut(2, cmd, to_exec)
            elif cmd_lower.startswith('timport '): cmd = cmd.replace('timport ','').split(' '); new_texture = tabledata.add_object(28); import_texture(new_texture._contents, cmd[0], cmd[1], f'dxt{cmd[2]}'); tabledata.add2ab(cmd[0], new_texture.path_id)
            elif cmd_lower.startswith('tswap '): cmd = cmd.replace('tswap ','').split(' '); import_texture(xdtdata, cmd[0], cmd[1], f'dxt{cmd[2]}')
            elif cmd_lower.startswith('tswap-mass '): cmd = cmd.replace('tswap-mass ','').replace(' ',''); tswap_mass(cmd)
            else:
                exec(cmd)
                print()
        except: print(clr(err(sys.exc_info()) + '\n', 2))

# extract

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
        banner = '\n    ______  _______ __   _ _     _   _______ _______\n    |     \\ |_____| | \\  | |____/    |______ |______\n    |_____/ |     | |  \\_| |    \\_ . |       |      \n                                                    \n    x\n\n        '
        x = clr("by sir.dank | nuclearff.com")
        cls(); print(align(clr_banner(banner).replace('x',x)))
        choice = input(clr("  > [1] CAB Explorer\n  > [2] Fix Bundles\n  > [0] Exit\n\n  > Choice: ") + green)
        if choice == "1": cls(); print(align(clr_banner(banner).replace('x',x))); one()
        elif choice == "2": cls(); print(align(clr_banner(banner).replace('x',x))); fix_bundles(); print(clr("  > Returning to menu in 5 seconds...")); time.sleep(5)
        #elif choice == "2": cls(); print(align(clr_banner(banner).replace('x',x))); two() ###
        elif choice == "0": cls(); sys.exit()

if __name__ == "__main__": log = ""; main()
