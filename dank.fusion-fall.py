# Note: dank.fusion-fall.py is meant to be run as an .exe by default, if you would like to execute the script, make the below changes...
#       - uncomment the following line > filepath = os.path.dirname(__file__) # as .py
#       - comment the following line > filepath = os.path.dirname(sys.argv[0]) # as .exe
#       - if both of them were commented already, you do not have to change anything :)

from dankware import align, clr_banner, clr, cls
import json
import sys
import os

'''if not os.path.exists("unitypack"):
    print(clr("\n  > ERROR: unitypack missing!",2))
    print(clr("  > Download it from: https://github.com/dongresource/UnityPackFF",2))
    print(clr("  > Exiting in 10s...",2))
    time.sleep(10); sys.exit()'''

from unitypack.asset import Asset

def main():

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

def one():
    
    exec("cab_path = input(clr('  > Drag and Drop Custom Asset Bundle: ')).replace('\"',''); index = int(input(clr('  > TableData Object Index [7]: ')))")
    print(clr("\n  > f = open(cab_path, 'rb')"))
    exec("f = open(cab_path, 'rb')")
    print(clr("  > tabledata = Asset.from_file(f)"))
    exec("tabledata = Asset.from_file(f)")
    print(clr("  > xdtdata = tabledata.objects[index].contents"))
    exec("xdtdata = tabledata.objects[index].contents")
    print(clr("\n  > Successfully loaded XDT data! You can now start running functions!\n"))

    while True:
        cmd = input(clr("  > ")); print()
        if cmd == "exit": break
        elif cmd == "save":
            exec("tabledata.save(open(str(cab_path.split('\\\\')[-1]),'wb'))")
        elif cmd == "dump-xdt":
            exec('out = {}\nfor tname, table in xdtdata.items():\n    out[tname] = {}\n    try:\n        for dname, data in table.items(): out[tname][dname] = data\n    except: out[tname] = "<err>"\njson.dump(out, open("xdt.json", "w+"), indent=4)')
        else:
            try: exec(cmd) #exec(f"print({cmd})")
            except Exception as err: print(clr(f"  > ERROR: {err}",2))
            print()

if __name__ == "__main__":
    filepath = os.path.dirname(__file__) # as .py
    #filepath = os.path.dirname(sys.argv[0]) # as .exe
    os.chdir(filepath)
    if not os.path.exists("dank.ff"): os.mkdir("dank.ff")
    os.chdir("dank.ff")
    main()