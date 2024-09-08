import os 
import pathlib
from operator import itemgetter

#Name your current Jfin playlist location here. The default location for Windows installations is listed below
rootdir = r'C:\ProgramData\Jellyfin\Server\root\default'
#Name your new paths here. If the root dir of your libraries currently sits in Windows style "C:/Media", and you want it to end up in Unix style "media/", then [C:/Media, /media]
#If you have multiple locations for your libraries, you can specify individual locations or migrate them all together. Up to you. 
newpathlist = [["E:", "/media"], ["G:", "/media"], ["%AppDataPath%", "/data/data"]]

def main():
    pathdictlist = []
    for root, dirs, files in os.walk(rootdir):
        for file in files:
            filename, fileext = os.path.splitext(file)
            if fileext == ".mblink":
                with open(os.path.join(root, file)) as f:
                    wosix = ((((pathlib.PurePosixPath(repr(f.read()))).as_posix()).replace('\\','/')).replace("//", "/")).replace("'","")
                    linkdepthcount = wosix.count('/')
                    for pathlist in newpathlist:
                        if wosix.startswith(pathlist[0]): 
                            newpath = wosix.replace(pathlist[0], pathlist[1])
                    pathdict = {'wpath': wosix, 'lpath': newpath, 'depth': linkdepthcount}
                    if pathdict not in pathdictlist:
                        pathdictlist.append(pathdict)      
    
    newlist = sorted(pathdictlist, key=itemgetter('depth'), reverse=True)
    
    print("\n\n---BEGINNING path_replacements LIBRARY LOOKUP---\n\n")
    for dict in newlist:
        try: 
            print('"' + dict.get('wpath') + '" : "' + dict.get('lpath') + '",')
        except UnicodeEncodeError:
            print("---LIBRARY PASSED DUE TO UNICODE ERROR---")
    
    print("\n\n---BEGINNING fs_path_replacements REVERSE LIBRARY LOOKUP---\n\n")
    for dict in newlist:
        try: 
            print('"' + dict.get('lpath') + '" : "' + dict.get('wpath') + '",')
        except UnicodeEncodeError:
            print("---LIBRARY PASSED DUE TO UNICODE ERROR---")
    
if __name__ == "__main__":
    main()