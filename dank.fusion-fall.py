import os
import sys
import json
import time
import shutil
import requests
import pretty_errors
from dankware.tkinter import file_selector
from dankware import align, clr, cls, err, rm_line, title
from dankware import white, white_normal, red, red_normal, red_dim, green, reset, Style

title("𝚍𝚊𝚗𝚔.𝚏𝚞𝚜𝚒𝚘𝚗-𝚏𝚊𝚕𝚕")

def change_dir():

    os.chdir(os.path.dirname(__file__))
    if os.path.basename(os.getcwd()) == "dank.fusion-fall.dist":
        os.chdir("..")
    if not os.path.isdir("dank.fusion-fall"):
        os.mkdir("dank.fusion-fall")
    os.chdir("dank.fusion-fall")

def setup():
    
    global magickwand_installed

    try: from wand.image import Image; magickwand_installed = True
    except ImportError:
        
        magickwand_installed = False

        cls(); print(clr("\n  - MagickWand shared library not found!",2))
        
        if input(clr("\n  > Download ImageMagick? [y/n]: ") + red).lower() == "y":
    
            while True:
                try:

                    file_name = "ImageMagick-7.1.0-37-Q16-HDRI-x64-dll.exe"
                    print(clr(f"\n  - Downloading [ {file_name} ]..."))
                    response = requests.get(f"https://github.com/SirDank/dank.fusion-fall/raw/main/__assets__/{file_name}", headers={'user-agent':'dank.fusion-fall'}, allow_redirects=True)
                    data = response.content
                    try: size = '{:.3}'.format(int(response.headers['Content-Length'])/1024000)
                    except: size = "?"
                    open(file_name,"wb").write(data)
                    print(clr(f"\n  - Downloaded [ {file_name} ] [ {size} MB ]"))
                    break

                except: input(clr(f"\n  > Failed [ {file_name} ] Press {white}ENTER{red} to try again... ",2))

            print(clr("\n  - Launching ImageMagick Installer..."))
            os.system(file_name)
            input(clr("\n  > Press [ENTER] after you have installed ImageMagick... "))
            magickwand_installed = True

change_dir()
setup()

if magickwand_installed:
    
    # there is a reason this is being written like this!
    try: from wand.image import Image; from unitypackff.asset import Asset; from unitypackff.export import OBJMesh; from unitypackff.object import FFOrderedDict, ObjectPointer; from unitypackff.modding import import_texture, import_mesh, import_audio
    except:
        print(clr("\n  - Failed to import required packages! Exiting...",2))
        time.sleep(3)
        sys.exit(0)
else:
    print(clr("\n  - ImageMagick is required to run this tool! Exiting...",2))
    time.sleep(3)
    sys.exit(0)

def banner():
    
    banner = '\n\n ____  _____ _____ _____   _____ _____    ___ \n|    \\|  _  |   | |  |  | |   __|   __|  |_  |\n|  |  |     | | | |    -|_|   __|   __|  |  _|\n|____/|__|__|_|___|__|__|_|__|  |__|     |___|\n\nx\n\n'
    x = Style.BRIGHT + clr(f"by sir.dank | {green}nuclearff.{green}com")
    cls(); print(align(clr(banner,4,colours=[white, white_normal, red, red_normal, red_dim]).replace('x',x)))

def open_workspace():

    banner()
    
    folders = [_ for _ in os.listdir() if os.path.isdir(_)]

    if len(folders) == 0:
        
        print(clr("\n  - No workspaces found!\n",2))
        while True:
            try:
                workspace = input(clr("  > New workspace name: ") + red)
                os.mkdir(workspace)
                os.chdir(workspace)
                break
            except:
                rm_line()
                print(clr(f"  - Failed to make directory: {workspace}",2))       
    
    else:
        
        print(clr("\n  - Workspaces:\n\n    0 - Create New Workspace"))
        for i, workspace in enumerate(folders):
            print(clr(f"    {i+1} > {workspace}"))
        
        print()
        while True:
            _ = input(clr("  > Select workspace [num/name]: ") + red)
            if _.isdigit() and int(_) >= 0 and int(_) <= len(folders):
                if int(_) == 0:
                    print()
                    while True:
                        try:
                            workspace = input(clr("  > New workspace name: ") + red)
                            if not os.path.isdir(workspace):
                                os.mkdir(workspace); break
                            else:
                                rm_line()
                        except:
                            rm_line()
                            print(clr(f"  - Failed to make directory: {workspace}",2))   
                    break
                else: workspace = folders[int(_)-1]; break
            elif _ in folders: workspace = _; break
            else: rm_line()
            
        os.chdir(workspace)
        workspace = os.getcwd()
        if "y" in input(clr("\n  > Open workspace in explorer? [y/n]: ") + red).lower():
            os.system(f'explorer.exe "{workspace}"')

def logger(string: str) -> str:

    global log
    log += string + "\n"
    return string

def path_id(filename: str):

    id = ''; data = str(xdtdata).split(filename)[1].split('path_id=')[1]
    for _ in data:
        if _ != ')' and _.isdigit(): id += _
        else: break
    print(clr(f"  - path_id: {id}"))

def dump_xdt():

    output = {}
    for tname, table in xdtdata.items():
        output[tname] = {}
        try:
            for dname, data in table.items():
                output[tname][dname] = data
        except: output[tname] = "<err>"
    
    if "CustomAssetBundle-TableData" in cab_name: file_name = "xdt1013.json"
    else: file_name = "xdt.json"

    json.dump(output, open(file_name, "w+"), indent=4)

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

    shutil.rmtree("bundles_to_fix"); print(clr(f"\n  - Fixed [{len(bundles)}] bundles!\n"))

def texture_swap_mass(dxt_mode):

    try: os.mkdir("texture_swap"); input(clr("  > Created texture_swap folder! Hit [ENTER] after adding your files... "))
    except: pass

    textures = os.listdir("texture_swap")
    for texture in textures:
        try: import_texture(xdtdata, f"texture_swap/{texture}", texture.split('.')[0], f'dxt{dxt_mode}')
        except: print(clr(err(sys.exc_info()), 2))
        
    print(clr(f"\n  - Mass swapped [{len(textures)}] textures!\n"))

def texture_import_mass(dxt_mode):
    
    try: os.mkdir("texture_import"); input(clr("  > Created texture_import folder! Hit [ENTER] after adding files... "))
    except: pass

    textures = os.listdir("texture_import")
    for texture in textures:
        try: 
            new_texture = tabledata.add_object(28)
            import_texture(new_texture._contents, f"texture_import/{texture}", texture.split('.')[0], f'dxt{dxt_mode}')
            tabledata.add2ab(f"texture/{texture}.dds", new_texture.path_id)
        except: print(clr(err(sys.exc_info()), 2))
        
    print(clr(f"\n  - Mass imported [{len(textures)}] textures!\n"))

def shortcut(mode, cmd, to_exec):

    if mode == 1:
        if "=" not in cmd: exec(f"print({to_exec})".replace('key', cmd))
        else: cmd = cmd.split(' = '); exec(to_exec.replace('key',cmd[0]) + f" = \"{cmd[1]}\"")
    elif mode == 2: 
        if len(cmd) == 1: exec(f"print({to_exec})".replace('key', cmd[0]))
        else: exec(to_exec.replace('key',cmd[0]) + f" = \"{cmd[1]}\"")
    print()

def add_mission():

    mission_id = int(sorted([_['m_iHMissionID'] for _ in xdtdata['m_pMissionTable']['m_pMissionData']])[-1]) + 1
    print(clr(f"  - New Mission ID: {green}{mission_id}"))
    multiplier = mission_id - 919

    min_required_lvl = max(int(input(clr("  > Minimum Required Level (int): ") + green)), 0)
    required_missions = input(clr("  > Required Mission (int,int): ") + green).split(',',1)
    quest_giver_npc = int(input(clr("  > Quest Giver NPC ID (int): ") + green))
    quest_npc = int(input(clr("  > Quest NPC ID (int): ") + green))
    enemy_id = int(input(clr("  > Enemy ID (int): ") + green))
    quest_item = input(clr("  > Quest Item (str): ") + green)
    reward_item_type = input(clr("  > Reward Item Type (int,int,int,int): ") + green).split(',',3)
    reward_item_id = input(clr("  > Reward Item ID (int,int,int,int): ") + green).split(',',3)

    if len(reward_item_type) != 4:
        print(clr("  - Reward Item Type must be 4 integers separated by 3 commas!", 2))
        return
    if len(reward_item_id) != 4:
        print(clr("  - Reward Item ID must be 4 integers separated by 3 commas!", 2))
        return
    if len(required_missions) != 2:
        print(clr("  - Required Mission must be 2 integers separated by 1 comma!", 2))
        return

    for _ in range(4):
        if not reward_item_type[_].isdigit() or not reward_item_id[_].isdigit():
            print(clr("  - Reward Item Type and ID must be integers!", 2))
            return
        reward_item_type[_] = int(reward_item_type[_])
        reward_item_id[_] = int(reward_item_id[_])

    for _ in range(2):
        if not required_missions[_].isdigit():
            print(clr("  - Required Mission must be integers!", 2))
            return
        required_missions[_] = int(required_missions[_])

    data = FFOrderedDict()
    data['m_iHMissionType'] = 3
    data['m_iHMissionID'] = mission_id
    data['m_iHMissionName'] = 16038 + (16*multiplier)
    data['m_iHTaskType'] = 1
    data['m_iHTaskID'] = 5249 + (3*multiplier)
    data['m_iHNPCID'] = quest_giver_npc
    data['m_iHJournalNPCID'] = quest_giver_npc
    data['m_iHTerminatorNPCID'] = quest_npc
    data['m_iHDifficultyType'] = 2
    data['m_iHBarkerTextID'] = [0, 0, 0, 0]
    data['m_iHCurrentObjective'] = 16039 + (16*multiplier)
    data['m_iRequireInstanceID'] = 0
    data['m_iRepeatflag'] = 0
    data['m_iKorStReqLvlMin'] = 0
    data['m_iCTRReqLvMin'] = min_required_lvl
    data['m_iCTRReqLvMax'] = 0
    data['m_iCSTRReqNano'] = [0, 0, 0, 0, 0]
    data['m_iCSTReqGuide'] = 0
    data['m_iCSTReqMission'] = required_missions
    data['m_iCSTEntranceGroupMin'] = 0
    data['m_iCSTEntranceGroupMax'] = 0
    data['m_iCSTItemID'] = [0, 0, 0]
    data['m_iCSTItemNumNeeded'] = [0, 0, 0]
    data['m_iCSTTrigger'] = 0
    data['m_iCSUCheckTimer'] = 0
    data['m_iCSUEnemyID'] = [0, 0, 0]
    data['m_iCSUNumToKill'] = [0, 0, 0]
    data['m_iCSUItemID'] = [0, 0, 0]
    data['m_iCSUItemNumNeeded'] = [0, 0, 0]
    data['m_iCSUDEFNPCID'] = 0
    data['m_iCSUDEFNPCAI'] = 0
    data['m_iCSUDEPNPCFollow'] = 0
    data['m_iSTGrantTimer'] = 0
    data['m_iSTItemID'] = [0, 0, 0]
    data['m_iSTItemNumNeeded'] = [0, 0, 0]
    data['m_iSTItemDropRate'] = [0, 0, 0]
    data['m_iSTGrantWayPoint'] = quest_npc
    data['m_iSTSpawnMonsterID'] = 0
    data['m_iSTSpwanLocation'] = 0
    data['m_iSTMessageType'] = 0
    data['m_iSTMessageTextID'] = 0
    data['m_iSTMessageSendNPC'] = 0
    data['m_iSTDialogBubble'] = 16040 + (16*multiplier)
    data['m_iSTDialogBubbleNPCID'] = quest_giver_npc
    data['m_iSTJournalIDAdd'] = 2988 + (3*multiplier)
    data['m_pstrSTScript'] = ''
    data['m_iSTNanoID'] = 0
    data['m_iKorSuccRewardID'] = 0
    data['m_iSUReward'] = 0
    data['m_iSUOutgoingMission'] = 0
    data['m_iSUOutgoingTask'] = 5250 + (3*multiplier)
    data['m_iSUItem'] = [0, 0, 0]
    data['m_iSUInstancename'] = [0, 0, 0]
    data['m_iSUMessageType'] = 0
    data['m_iSUMessagetextID'] = 0
    data['m_iSUMessageSendNPC'] = 0
    data['m_iSUDialogBubble'] = 16041 + (16*multiplier)
    data['m_iSUDialogBubbleNPCID'] = quest_npc
    data['m_iSUJournaliDAdd'] = 2988 + (3*multiplier)
    data['m_iFOutgoingMission'] = 0
    data['m_iFOutgoingTask'] = 0
    data['m_iFItemID'] = [0, 0, 0]
    data['m_iFItemNumNeeded'] = [0, 0, 0]
    data['m_iFMessageType'] = 0
    data['m_iFMessageTextID'] = 0
    data['m_iFMessageSendNPC'] = 0
    data['m_iFDialogBubble'] = 0
    data['m_iFDialogBubbleNPCID'] = 0
    data['m_iFJournalIDAdd'] = 0
    data['m_iDelItemID'] = [0, 0, 0, 0]
    data['m_iMentorEmailID'] = [0, 0, 0, 0, 0]
    xdtdata['m_pMissionTable']['m_pMissionData'].append(data)

    data = FFOrderedDict()
    data['m_iHMissionType'] = 3
    data['m_iHMissionID'] = mission_id
    data['m_iHMissionName'] = 16038 + (16*multiplier)
    data['m_iHTaskType'] = 5
    data['m_iHTaskID'] = 5250 + (3*multiplier)
    data['m_iHNPCID'] = 0
    data['m_iHJournalNPCID'] = quest_npc
    data['m_iHTerminatorNPCID'] = 0
    data['m_iHDifficultyType'] = 2
    data['m_iHBarkerTextID'] = [0, 0, 0, 0]
    data['m_iHCurrentObjective'] = 16043 + (16*multiplier)
    data['m_iRequireInstanceID'] = 0
    data['m_iRepeatflag'] = 0
    data['m_iKorStReqLvlMin'] = 0
    data['m_iCTRReqLvMin'] = min_required_lvl
    data['m_iCTRReqLvMax'] = 0
    data['m_iCSTRReqNano'] = [0, 0, 0, 0, 0]
    data['m_iCSTReqGuide'] = 0
    data['m_iCSTReqMission'] = required_missions
    data['m_iCSTEntranceGroupMin'] = 0
    data['m_iCSTEntranceGroupMax'] = 0
    data['m_iCSTItemID'] = [0, 0, 0]
    data['m_iCSTItemNumNeeded'] = [0, 0, 0]
    data['m_iCSTTrigger'] = 0
    data['m_iCSUCheckTimer'] = 0
    data['m_iCSUEnemyID'] = [enemy_id, 0, 0]
    data['m_iCSUNumToKill'] = [0, 0, 0]
    data['m_iCSUItemID'] = [578 + (1*multiplier), 0, 0]
    data['m_iCSUItemNumNeeded'] = [1, 0, 0]
    data['m_iCSUDEFNPCID'] = 0
    data['m_iCSUDEFNPCAI'] = 0
    data['m_iCSUDEPNPCFollow'] = 0
    data['m_iSTGrantTimer'] = 0
    data['m_iSTItemID'] = [578 + (1*multiplier), 0, 0]
    data['m_iSTItemNumNeeded'] = [0, 0, 0]
    data['m_iSTItemDropRate'] = [100, 0, 0]
    data['m_iSTGrantWayPoint'] = 0
    data['m_iSTSpawnMonsterID'] = 0
    data['m_iSTSpwanLocation'] = 0
    data['m_iSTMessageType'] = 2
    data['m_iSTMessageTextID'] = 16044 + (16*multiplier)
    data['m_iSTMessageSendNPC'] = quest_giver_npc
    data['m_iSTDialogBubble'] = 0
    data['m_iSTDialogBubbleNPCID'] = 0
    data['m_iSTJournalIDAdd'] = 2989 + (3*multiplier)
    data['m_pstrSTScript'] = ''
    data['m_iSTNanoID'] = 0
    data['m_iKorSuccRewardID'] = 0
    data['m_iSUReward'] = 0
    data['m_iSUOutgoingMission'] = 0
    data['m_iSUOutgoingTask'] = 5251 + (3*multiplier)
    data['m_iSUItem'] = [0, 0, 0]
    data['m_iSUInstancename'] = [0, 0, 0]
    data['m_iSUMessageType'] = 0
    data['m_iSUMessagetextID'] = 0
    data['m_iSUMessageSendNPC'] = 0
    data['m_iSUDialogBubble'] = 0
    data['m_iSUDialogBubbleNPCID'] = 0
    data['m_iSUJournaliDAdd'] = 2989 + (3*multiplier)
    data['m_iFOutgoingMission'] = 0
    data['m_iFOutgoingTask'] = 0
    data['m_iFItemID'] = [0, 0, 0]
    data['m_iFItemNumNeeded'] = [0, 0, 0]
    data['m_iFMessageType'] = 0
    data['m_iFMessageTextID'] = 0
    data['m_iFMessageSendNPC'] = 0
    data['m_iFDialogBubble'] = 0
    data['m_iFDialogBubbleNPCID'] = 0
    data['m_iFJournalIDAdd'] = 0
    data['m_iDelItemID'] = [0, 0, 0, 0]
    data['m_iMentorEmailID'] = [0, 0, 0, 0, 0]
    xdtdata['m_pMissionTable']['m_pMissionData'].append(data)

    data = FFOrderedDict()
    data['m_iHMissionType'] = 3
    data['m_iHMissionID'] = mission_id
    data['m_iHMissionName'] = 16038 + (16*multiplier)
    data['m_iHTaskType'] = 4
    data['m_iHTaskID'] = 5251 + (3*multiplier)
    data['m_iHNPCID'] = 0
    data['m_iHJournalNPCID'] = quest_giver_npc
    data['m_iHTerminatorNPCID'] = quest_giver_npc
    data['m_iHDifficultyType'] = 2
    data['m_iHBarkerTextID'] = [0, 0, 0, 0]
    data['m_iHCurrentObjective'] = 16046 + (16*multiplier)
    data['m_iRequireInstanceID'] = 0
    data['m_iRepeatflag'] = 0
    data['m_iKorStReqLvlMin'] = 0
    data['m_iCTRReqLvMin'] = min_required_lvl
    data['m_iCTRReqLvMax'] = 0
    data['m_iCSTRReqNano'] = [0, 0, 0, 0, 0]
    data['m_iCSTReqGuide'] = 0
    data['m_iCSTReqMission'] = required_missions
    data['m_iCSTEntranceGroupMin'] = 0
    data['m_iCSTEntranceGroupMax'] = 0
    data['m_iCSTItemID'] = [0, 0, 0]
    data['m_iCSTItemNumNeeded'] = [0, 0, 0]
    data['m_iCSTTrigger'] = 0
    data['m_iCSUCheckTimer'] = 0
    data['m_iCSUEnemyID'] = [0, 0, 0]
    data['m_iCSUNumToKill'] = [0, 0, 0]
    data['m_iCSUItemID'] = [578 + (1*multiplier), 0, 0]
    data['m_iCSUItemNumNeeded'] = [1, 0, 0]
    data['m_iCSUDEFNPCID'] = 0
    data['m_iCSUDEFNPCAI'] = 0
    data['m_iCSUDEPNPCFollow'] = 0
    data['m_iSTGrantTimer'] = 0
    data['m_iSTItemID'] = [578 + (1*multiplier), 0, 0]
    data['m_iSTItemNumNeeded'] = [1, 0, 0]
    data['m_iSTItemDropRate'] = [0, 0, 0]
    data['m_iSTGrantWayPoint'] = quest_giver_npc
    data['m_iSTSpawnMonsterID'] = 0
    data['m_iSTSpwanLocation'] = 0
    data['m_iSTMessageType'] = 2
    data['m_iSTMessageTextID'] = 16047 + (16*multiplier)
    data['m_iSTMessageSendNPC'] = quest_npc
    data['m_iSTDialogBubble'] = 0
    data['m_iSTDialogBubbleNPCID'] = 0
    data['m_iSTJournalIDAdd'] = 2990 + (3*multiplier)
    data['m_pstrSTScript'] = ''
    data['m_iSTNanoID'] = 0
    data['m_iKorSuccRewardID'] = 0
    data['m_iSUReward'] = 722 + (1*multiplier)
    data['m_iSUOutgoingMission'] = 0
    data['m_iSUOutgoingTask'] = 0
    data['m_iSUItem'] = [578 + (1*multiplier), 0, 0]
    data['m_iSUInstancename'] = [-1, 0, 0]
    data['m_iSUMessageType'] = 0
    data['m_iSUMessagetextID'] = 0
    data['m_iSUMessageSendNPC'] = 0
    data['m_iSUDialogBubble'] = 16048 + (16*multiplier)
    data['m_iSUDialogBubbleNPCID'] = quest_giver_npc
    data['m_iSUJournaliDAdd'] = 2990 + (3*multiplier)
    data['m_iFOutgoingMission'] = 0
    data['m_iFOutgoingTask'] = 0
    data['m_iFItemID'] = [0, 0, 0]
    data['m_iFItemNumNeeded'] = [0, 0, 0]
    data['m_iFMessageType'] = 0
    data['m_iFMessageTextID'] = 0
    data['m_iFMessageSendNPC'] = 0
    data['m_iFDialogBubble'] = 0
    data['m_iFDialogBubbleNPCID'] = 0
    data['m_iFJournalIDAdd'] = 0
    data['m_iDelItemID'] = [0, 0, 0, 0]
    data['m_iMentorEmailID'] = [0, 0, 0, 0, 0]
    xdtdata['m_pMissionTable']['m_pMissionData'].append(data)

    data = FFOrderedDict()
    data['m_iMissionSummary'] = 16037 + (16*multiplier)
    data['m_iDetaileMissionDesc'] = 16034 + (16*multiplier)
    data['m_iMissionCompleteSummary'] = 16035 + (16*multiplier)
    data['m_iDetaileMissionCompleteSummary'] = 16036 + (16*multiplier)
    data['m_iTaskSummary'] = 0
    data['m_iDetailedTaskDesc'] = 16042 + (16*multiplier)
    xdtdata['m_pMissionTable']['m_pJournalData'].append(data)

    data = FFOrderedDict()
    data['m_iMissionSummary'] = 16037 + (16*multiplier)
    data['m_iDetaileMissionDesc'] = 16034 + (16*multiplier)
    data['m_iMissionCompleteSummary'] = 16035 + (16*multiplier)
    data['m_iDetaileMissionCompleteSummary'] = 16036 + (16*multiplier)
    data['m_iTaskSummary'] = 0
    data['m_iDetailedTaskDesc'] = 16045 + (16*multiplier)
    xdtdata['m_pMissionTable']['m_pJournalData'].append(data)

    data = FFOrderedDict()
    data['m_iMissionSummary'] = 16037 + (16*multiplier)
    data['m_iDetaileMissionDesc'] = 16034 + (16*multiplier)
    data['m_iMissionCompleteSummary'] = 16035 + (16*multiplier)
    data['m_iDetaileMissionCompleteSummary'] = 16036 + (16*multiplier)
    data['m_iTaskSummary'] = 0
    data['m_iDetailedTaskDesc'] = 16049 + (16*multiplier)
    xdtdata['m_pMissionTable']['m_pJournalData'].append(data)

    data = FFOrderedDict()
    data['m_iMissionRewardID'] = 722 + (1*multiplier)
    data['m_iMissionRewarItemType'] = reward_item_type
    data['m_iMissionRewardItemID'] = reward_item_id
    data['m_iBox1Choice'] = 0
    data['m_iMissionRewardItemType2'] = [0, 0, 0, 0]
    data['m_iMissionRewardItemID2'] = [0, 0, 0, 0]
    data['m_iBox2Choice'] = 0
    data['m_iCash'] = 10000
    data['m_iFusionMatter'] = 10000
    xdtdata['m_pMissionTable']['m_pRewardData'].append(data)

    for _ in range(1,17):
        mission_string = input(clr(f"  > MissionString [{_}]: " + green))
        data = FFOrderedDict()
        data['m_pstrNameString'] = mission_string
        xdtdata['m_pMissionTable']['m_pMissionStringData'].append(data)

    data = FFOrderedDict()
    data['m_iItemNumber'] = 578 + (1*multiplier)
    data['m_iItemName'] = 578 + (1*multiplier)
    data['m_iComment'] = 0
    data['m_iQuestStart'] = 0
    data['m_iDelete'] = 0
    data['m_iIcon'] = 2
    xdtdata['m_pQuestItemTable']['m_pItemData'].append(data)

    data = FFOrderedDict()
    data['m_strName'] = quest_item
    data['m_strComment'] = quest_item
    data['m_strComment1'] = ""
    data['m_strComment2'] = ""
    data['m_iExtraNumber'] = 0
    xdtdata['m_pQuestItemTable']['m_pItemStringData'].append(data)

def add_npc():
    
    tmp = str(xdtdata['m_pNpcTable']['m_pNpcData'][-1])
    
    if "m_iNpcNumber" not in tmp:
        print(clr('\n  - Could not find "m_iNpcNumber" in str(xdtdata["m_pNpcTable"]["m_pNpcData"][-1])',2))
        return
    
    new_npc_num = int(tmp.split("'m_iNpcNumber', ")[1].split(')')[0]) + 1
    
    data = FFOrderedDict()
    print(clr(f"  > data['m_iNpcNumber'] = {new_npc_num}"))
    data['m_iNpcNumber'] = new_npc_num
    print(clr(f"  > data['m_iNpcName'] = {new_npc_num}"))
    data['m_iNpcName'] = new_npc_num
    print(clr(f"  > data['m_iComment'] = {new_npc_num}"))
    data['m_iComment'] = new_npc_num
    
    new_mesh_num = int(tmp.split("'m_iMesh', ")[1].split(')')[0]) + 1
    print(clr(f"  > data['m_iMesh'] = {new_mesh_num}"))
    data['m_iMesh'] = new_mesh_num
    
    counter = -1
    while True:
        last_barker_num = int(str(xdtdata['m_pNpcTable']['m_pNpcData'][counter]).split("'m_iBarkerNumber', ")[1].split(')')[0])
        if last_barker_num != 0: break
        counter -= 1

    print(clr(f"  > data['m_iBarkerNumber'] = {last_barker_num + 1}"))
    data['m_iBarkerNumber'] = last_barker_num + 1
    
    for key in ['m_iDifficulty', 'm_iTeam', 'm_iNpcLevel', 'm_iNpcType', 'm_iHNpc', 'm_iHNpcNum', 'm_iNpcStyle', 'm_iAiType', 'm_iHP', 'm_iHPRegen', 'm_iDropType', 'm_iRegenTime', 'm_iHeight', 'm_iRadius', 'm_fScale', 'm_iPower', 'm_iAccuracy', 'm_iProtection', 'm_iDodge', 'm_iRunSpeed', 'm_iSwimSpeed', 'm_iJumpHeight', 'm_iJumpDistance', 'm_iSightRange', 'm_iIdleRange', 'm_iCombatRange', 'm_iAtkRange', 'm_iAtkAngle', 'm_iAtkRate', 'm_iEffectArea', 'm_iTargetMode', 'm_iTargetNumber', 'm_iInitalTime', 'm_iDeliverTime', 'm_iDelayTime', 'm_iDurationTime', 'm_iMegaType', 'm_iMegaTypeProb', 'm_iCorruptionType', 'm_iCorruptionTypeProb', 'm_iActiveSkill1', 'm_iActiveSkill1Prob', 'm_iActiveSkill2', 'm_iActiveSkill2Prob', 'm_iActiveSkill3', 'm_iActiveSkill3Prob', 'm_iSupportSkill', 'm_iPassiveBuff', 'm_iNeck', 'm_iTexture', 'm_iTexture2', 'm_iIcon1', 'm_iEffect', 'm_iSound', 'm_iWalkSpeed', 'm_iMapIcon', 'm_iLegStyle', 'm_iBarkerType', 'm_iMegaAni', 'm_iActiveSkill1Ani', 'm_iActiveSkill2Ani', 'm_iSupportSkillAni', 'm_iMegaString', 'm_iCorruptionString', 'm_iActiveSkill1String', 'm_iActiveSkill2String', 'm_iSupportSkillString', 'm_iServiceNumber']:
        while True:
            try: data[key] = int(input(clr(f"  > data['{key}'] (int) = ") + green)); break
            except: pass
            
    for key in ['m_fAnimationSpeed', 'm_fWalkAnimationSpeed', 'm_fRunAnimationSpeed']:
        while True:
            try: data[key] = float(input(clr(f"  > data['{key}'] (float) = ") + green)); break
            except: pass

    print(clr("  > xdtdata['m_pNpcTable']['m_pNpcData'].append(data)"))
    xdtdata['m_pNpcTable']['m_pNpcData'].append(data)

    #data = FFOrderedDict()
    #for key in ['m_iIconNumber', 'm_iIconType']:
    #    while True:
    #        try: data[key] = int(input(clr(f"  > data['{key}'] (int) = ") + green)); break
    #        except: pass
    #print(clr("  > xdtdata['m_pNpcTable']['m_pNpcIconData'].append(data)"))
    #xdtdata['m_pNpcTable']['m_pNpcIconData'].append(data)
    
    data = FFOrderedDict()
    for key in ['m_pstrMMeshModelString', 'm_pstrMTextureString', 'm_pstrMTextureString2', 'm_pstrFTextureString', 'm_pstrFTextureString2', 'm_pstrFMeshModelString']:
        while True:
            try: data[key] = input(clr(f"  > data['{key}'] (string) = ") + green); break
            except: pass
    print(clr("  > xdtdata['m_pNpcTable']['m_pNpcMeshData'].append(data)"))
    xdtdata['m_pNpcTable']['m_pNpcMeshData'].append(data)

    data = FFOrderedDict()
    for key in ['m_strName', 'm_strComment', 'm_strComment1', 'm_strComment2']:
        while True:
            try: data[key] = input(clr(f"  > data['{key}'] (string) = ") + green); break
            except: pass
    while True:
        try: data['m_iExtraNumber'] = int(input(clr(f"  > data['m_iExtraNumber'] (int) = ") + green)); break
        except: pass
    print(clr("  > xdtdata['m_pNpcTable']['m_pNpcBarkerData'].append(data)"))
    xdtdata['m_pNpcTable']['m_pNpcBarkerData'].append(data)
    
    data = FFOrderedDict()
    for key in ['m_strName', 'm_strComment', 'm_strComment1', 'm_strComment2']:
        while True:
            try: data[key] = input(clr(f"  > data['{key}'] (string) = ") + green); break
            except: pass
    while True:
        try: data['m_iExtraNumber'] = int(input(clr(f"  > data['m_iExtraNumber'] (int) = ") + green)); break
        except: pass
    print(clr("  > xdtdata['m_pNpcTable']['m_pNpcStringData'].append(data)"))
    xdtdata['m_pNpcTable']['m_pNpcStringData'].append(data)

def print_bundle():
    
    container = tabledata.objects[1].read()['m_Container']
    print(clr(logger('asset\t\tindex\tsize\tpath')))
    for path, mtdt in container:
        print(clr(logger('{}\t{}\t{}\t{}'.format(mtdt['asset'].path_id, mtdt['preloadIndex'], mtdt['preloadSize'], path))))

def print_content():
    
    print(clr(logger('id\t\ttype_id\ttype\t\tname')))
    for id, obj in tabledata.objects.items():
        name = ''
        if hasattr(obj.read(), 'name'):
            name = obj.read().name
        try: print(clr(logger('{}\t{}\t{}\t{}'.format(id, obj.type_id, obj.type, name))))
        except Exception as exc: print(clr('ERROR: ' + str(exc))) 

# main

def main():
    
    global tabledata, xdtdata, cab_name
    
    while True:

        banner()
        print(clr("  - Select Custom Asset Bundle..."))
        
        cab_path = ''
        while not cab_path:
            if "PYTHONHOME" in os.environ:
                cab_path = file_selector("Select Custom Asset Bundle", os.path.join(os.path.dirname(__file__), "dankware.ico")).replace('/','\\').replace('"','')
            else: #cab_path = input(clr("  > Drag and Drop Custom Asset Bundle: ")).replace('/','\\').replace('"','')
                cab_path = file_selector("Select Custom Asset Bundle").replace('/','\\').replace('"','')
        rm_line()
        
        print(clr(logger(f'  > cab_path = "{cab_path}"')))
        cab_name = str(cab_path.split('\\')[-1])
        print(clr(logger(f"  > tabledata = Asset.from_file(open('{cab_path}', 'rb'))")))
        try:
            tabledata = Asset.from_file(open(cab_path, 'rb'))
            tabledata_keys = [str(_) for _ in tabledata.objects.keys()]
            break
        except:
            print(clr(err(sys.exc_info()), 2))
            print(clr("  - Sleeping 10s..."))
            time.sleep(10)

    if input(clr(f"\n  > Print {len(tabledata.objects)} Available TableData Keys? [y/n]: ") + green).lower() == 'y':
        print(clr(logger("  - Available TableData Keys: \n\n" + '\n'.join(tabledata_keys) + "\n")))

    if "CustomAssetBundle-1dca92eecee4742d985b799d8226666d" in cab_name and "7" in tabledata_keys:
        print(clr("  - Suggested Key: 7"))
    elif "CustomAssetBundle-TableData" in cab_name and "2139558964" in tabledata_keys:
        print(clr("  - Suggested Key: 2139558964"))
    elif "CustomAssetBundle-8320bfa70e3f04727bfc405b1fd7efcc" in cab_name and "3" in tabledata_keys:
        print(clr("  - Suggested Key: 3"))
    elif "sharedassets0.assets" in cab_name and "1375" in tabledata_keys:
        print(clr("  - Suggested Key: 1375"))

    while True:    
        key = input(clr(f'  > TableData Key: ') + green)
        try:
            key = int(key)
            xdtdata = tabledata.objects[key].contents
            print(clr(logger(f"  > xdtdata = tabledata.objects[{key}].contents")))
            break
        except: print(clr(logger(f"  - Invalid Key: {key}"),2))
    print(clr("\n  - Pre-defined commands: print-bundle, print-content, dump-xdt, path_id('filename'), fix-bundles, add-mission, add-npc, help, log, save, save-all, clear, exit\n"))
    
    help_msg = """  - Available Shortcuts With Examples:\n
 - audio-import sound.wav, 22.5, sound  -  new_audio = tabledata.add_object(83); import_audio(new_audio.contents,'sound.wav',22.5,'sound'); tabledata.add2ab('sound.wav',new_audio.path_id)
 - audio-swap sound.wav, 22.5, sound  -  import_audio(xdtdata,'sound.wav',22.5,'sound')
 - export example.obj  -  open('example.obj','w').write(OBJMesh(xdtdata).export())
 - imesh npc_alienx.obj npc_alienx  -  import_mesh(xdtdata, 'npc_alienx.obj', 'npc_alienx')
 - key 0  -  xdtdata = tabledata.objects[0].contents 
 - ms-info  -  print(xdtdata['m_pMissionTable']['m_pMissionData'][1])
 - ms-npc 1 2671  -  xdtdata['m_pMissionTable']['m_pMissionData'][1]['m_iHNPCID'] = NPC_INDEX#
 - ms-npc 1  -  print(xdtdata['m_pMissionTable']['m_pMissionData'][1]['m_iHNPCID'])
 - ms-string 11666 = dee dee's herb garden  -  xdtdata['m_pMissionTable']['m_pMissionStringData'][11666] = \"dee dee's herb garden\"
 - ms-string 11666  -  print(xdtdata['m_pMissionTable']['m_pMissionStringData'][11666])
 - ms-task 1 2  -  xdtdata['m_pMissionTable']['m_pMissionData'][1]['m_iHTaskID'] = 2
 - ms-task 1  -  print(xdtdata['m_pMissionTable']['m_pMissionData'][1]['m_iHTaskID'])
 - ms-tasknext 1 2  -  xdtdata['m_pMissionTable']['m_pMissionData'][1]['m_iSUOutgoingTask'] = 2
 - ms-tasknext 1  -  print(xdtdata['m_pMissionTable']['m_pMissionData'][1]['m_iSUOutgoingTask'])
 - mesh 344  -  print(xdtdata['m_pNpcTable']['m_pNpcMeshData'][344]['m_pstrMMeshModelString'])
 - mesh 344 fusion_cheese  -  xdtdata['m_pNpcTable']['m_pNpcMeshData'][344]['m_pstrMMeshModelString'] = \"fusion_cheese\"
 - meshid 2675 2671  -  xdtdata['m_pNpcTable']['m_pNpcData'][2675]['m_iMesh'] = 2671
 - meshid 2677  -  print(xdtdata['m_pNpcTable']['m_pNpcData'][2675]['m_iMesh'])
 - npc-name 3148 = test name  -  xdtdata['m_pNpcTable']['m_pNpcStringData'][3148]['m_strName'] = \"test name\"
 - npc-name 3148  -  print(xdtdata['m_pNpcTable']['m_pNpcStringData'][3148]['m_strName'])
 - objects 1 1000  -  for _ in range(1,1000): print(f'{_} - {tabledata.objects[_].contents}')
 - rename Cone02, DT_MTDB_ETC05  -  xdtdata.name = xdtdata.name.replace('Cone02','DT_MTDB_ETC05')
 - texture 344  -  print(xdtdata['m_pNpcTable']['m_pNpcMeshData'][344]['m_pstrMTextureString'])
 - texture 344 fusion_cheese  -  xdtdata['m_pNpcTable']['m_pNpcMeshData'][344]['m_pstrMTextureString'] = \"fusion_cheese\"
 - texture-import texture 1  -  new_texture = tabledata.add_object(28); import_texture(new_texture._contents,'texture.png','texture','dxt1'); tabledata.add2ab('texture.png',new_texture.path_id)
 - texture-import texture 5  -  new_texture = tabledata.add_object(28); import_texture(new_texture._contents,'texture.png','texture','dxt5'); tabledata.add2ab('texture.png',new_texture.path_id)
 - texture-import-mass 1  -  mass import_texture (fmt='dxt1')
 - texture-import-mass 5  -  mass import_texture (fmt='dxt5')
 - texture-swap texture.png texture 1  -  import_texture(xdtdata,'texture.png','texture','dxt1')
 - texture-swap texture.png texture 5  -  import_texture(xdtdata,'texture.png','texture','dxt5')
 - texture-swap-mass 1  -  mass import_texture (fmt='dxt1')
 - texture-swap-mass 5  -  mass import_texture (fmt='dxt5')"""

    while True:
        try:
            cmd = logger(input(f"  {red}> {green}"))
            print(reset, end='')
            cmd_lower = cmd.lower().strip()

            if cmd_lower == "help": print(clr(help_msg))
            elif cmd_lower == "clear": cls()
            elif cmd_lower == "exit": break
            elif cmd_lower == "fix-bundles": fix_bundles()
            elif cmd_lower == "add-mission": add_mission()
            elif cmd_lower == "add-npc": add_npc()
            elif cmd_lower == "print-bundle": print_bundle()
            elif cmd_lower == "print-content": print_content()
            elif cmd_lower == "log": open("log.txt","w+").write(log)
            
            elif cmd_lower == "dump-xdt": 
                try: dump_xdt()
                except: print(clr(err(sys.exc_info()), 2))
            
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

            elif cmd_lower.startswith('audio-import '):
                cmd = cmd.replace('audio-import ','').split(', ')
                new_audio = tabledata.add_object(83)
                import_audio(new_audio.contents,cmd[0],int(cmd[1]),cmd[2])
                tabledata.add2ab(f"sound/{cmd[0]}",new_audio.path_id)

            elif cmd_lower.startswith('audio-swap '):
                cmd = cmd.replace('audio-swap ','').split(', ')
                import_audio(xdtdata, cmd[0], int(cmd[1]), cmd[2])

            elif cmd_lower.startswith('export '):
                cmd = cmd.replace('export ','').replace(' ','')
                open(cmd,'w').write(OBJMesh(xdtdata).export())

            elif cmd_lower.startswith('imesh '):
                cmd = cmd.replace('imesh ','').split(' ')
                import_mesh(xdtdata, cmd[0], cmd[1])
                
            elif cmd_lower.startswith('key '):
                key = int(cmd.replace('key ',''))
                xdtdata = tabledata.objects[key].contents

            elif cmd_lower.startswith('ms-info '):
                print(xdtdata['m_pMissionTable']['m_pMissionData'][int(cmd.replace('ms-info ',''))])

            elif cmd_lower.startswith('ms-npc '):
                cmd = cmd.replace('ms-npc ','').split(' ')
                to_exec = "xdtdata['m_pMissionTable']['m_pMissionData'][key]['m_iHNPCID']"
                shortcut(2, cmd, to_exec)

            elif cmd_lower.startswith('ms-string '):
                cmd = cmd.replace('ms-string ','')
                to_exec = "xdtdata['m_pMissionTable']['m_pMissionStringData'][key]"
                shortcut(1, cmd, to_exec)

            elif cmd_lower.startswith('ms-task '):
                cmd = cmd.replace('ms-task ','').split(' ')
                to_exec = "xdtdata['m_pMissionTable']['m_pMissionData'][key]['m_iHTaskID']"
                shortcut(2, cmd, to_exec)

            elif cmd_lower.startswith('ms-tasknext '):
                cmd = cmd.replace('ms-tasknext ','').split(' ')
                to_exec = "xdtdata['m_pMissionTable']['m_pMissionData'][key]['m_iSUOutgoingTask']"
                shortcut(2, cmd, to_exec)

            elif cmd_lower.startswith('mesh '):
                cmd = cmd.replace('mesh ','').split(' ')
                to_exec = "xdtdata['m_pNpcTable']['m_pNpcMeshData'][key]['m_pstrMMeshModelString']"
                shortcut(2, cmd, to_exec)

            elif cmd_lower.startswith('meshid '):
                cmd = cmd.replace('meshid ','').split(' ')
                to_exec = "xdtdata['m_pNpcTable']['m_pNpcData'][key]['m_iMesh']"
                shortcut(2, cmd, to_exec)

            elif cmd_lower.startswith('npc-name '):
                cmd = cmd.replace('npc-name ','')
                to_exec = "xdtdata['m_pNpcTable']['m_pNpcStringData'][key]['m_strName']"
                shortcut(1, cmd, to_exec)

            elif cmd_lower.startswith('objects '):
                cmd = cmd.replace('objects ','').split(' ')
                to_exec = f"for _ in range({cmd[0]},{cmd[1]}): print(f'{{_}} - {{tabledata.objects[_].contents}}')"
                exec(to_exec); print()
            
            elif cmd_lower.startswith('rename '):
                cmd = cmd.replace('rename ','').split(', ')
                to_exec = f"xdtdata.name = xdtdata.name.replace('{cmd[0]}','{cmd[1]}')"
                exec(to_exec); print()

            elif cmd_lower.startswith('texture '):
                cmd = cmd.replace('texture ','').split(' ')
                to_exec = "xdtdata['m_pNpcTable']['m_pNpcMeshData'][key]['m_pstrMTextureString']"
                shortcut(2, cmd, to_exec)

            elif cmd_lower.startswith('texture-import '):
                cmd = cmd.replace('texture-import ','').split(' ')
                new_texture = tabledata.add_object(28)
                import_texture(new_texture._contents, f'{cmd[0]}.png', cmd[0], f'dxt{cmd[1]}')
                tabledata.add2ab(f"texture/{cmd[0]}.dds", new_texture.path_id)

            elif cmd_lower.startswith('texture-import-mass '):
                cmd = cmd.replace('texture-import-mass ','').replace(' ','')
                texture_import_mass(cmd)

            elif cmd_lower.startswith('texture-swap '):
                cmd = cmd.replace('texture-swap ','').split(' ')
                import_texture(xdtdata, cmd[0], cmd[1], f'dxt{cmd[2]}')

            elif cmd_lower.startswith('texture-swap-mass '):
                cmd = cmd.replace('texture-swap-mass ','').replace(' ','')
                texture_swap_mass(cmd)

            else:
                exec(cmd)
            
            print()

        except: print(clr(err(sys.exc_info()) + '\n', 2))

def menu():
    
    sys.setrecursionlimit(10000)
    open_workspace()
    
    while True:
        
        banner(); print(clr(f"\n  1 - CAB Explorer / Editor\n  2 - Fix Bundles\n  3 - Change workspace [{os.path.basename(os.getcwd())}]\n  4 - Visit {green}nuclearff.{green}com{white}\n  5 - Exit\n"))
        
        choice = input(clr("  > Choice: ") + green)
        if choice == "1": main()
        elif choice == "2": banner(); fix_bundles()
        elif choice == "3": open_workspace()
        elif choice == "4": os.system('start https://nuclearff.com/')
        elif choice == "5": break
        else: rm_line()

if __name__ == '__main__':

    log = ''
    menu()
