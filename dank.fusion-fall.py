# Note: dank.fusion-fall.py is meant to be run as an .exe by default, if you would like to execute the script, make the below changes...
#       - uncomment the following line > filepath = os.path.dirname(__file__) # as .py
#       - comment the following line > filepath = os.path.dirname(sys.argv[0]) # as .exe
#       - if both of them were commented already, you do not have to change anything :)

from dankware import align, clr_banner, clr, cls
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
        #print(clr("  > [2] Nano Switcher"))
        print(clr("  > [0] Exit"))
        
        choice = input(clr("\n  > Choice: "))
        if choice == "1": cls(); print(align(clr_banner(banner))); one()
        #if choice == "2": cls(); print(align(clr_banner(banner))); two()
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
            counter = 1
            while os.path.exists(f"NewTable_{counter}"): counter += 1
            exec(f"tabledata.save(open('NewTable_{counter}','wb'))")
        else:
            try: exec(cmd) #exec(f"print({cmd})")
            except Exception as err: print(clr(f"  > ERROR: {err}",2))
            print()

if __name__ == "__main__":
    filepath = os.path.dirname(__file__) # as .py
    #filepath = os.path.dirname(sys.argv[0]) # as .exe
    os.chdir(filepath)
    main()