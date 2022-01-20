import argparse
import os
import ctypes, sys
import re
from pprint import pprint

ANIME_PATH = 'D:\ビデオ\アニメ'
IGNORE_FILES = ['.parts', '映画', 'desktop.ini', 'ICO']

def tryint(s):
    try:
        return int(s)
    except:
        return s

def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]

def sort_nicely(l):
    """ Sort the given list in the way that humans expect.
    """
    l.sort(key=alphanum_key)

def arg_parsing():
    parser = argparse.ArgumentParser(
        description='Share Anki cards through google drive.')
    parser.add_argument(
        '-i',
        '--input',
        help='Takes name of anime in your database',
        action='store')
    args = parser.parse_args()
    if args.input == None:
        return(input('Name of the anime you would like renamed:'))
    return args.input   

def get_anime_dir():
    anime_list = os.listdir(ANIME_PATH)
    [anime_list.remove(anime) for ig in IGNORE_FILES for anime in reversed(anime_list) if ig in anime]
    return anime_list

def rename_subs(input_anime, anime_list):
    found_anime = [anime for anime in anime_list if input_anime.lower() in anime.lower()] 
    if len(found_anime) > 1:
        print('Found more than one anime with that name please choose which one you mean.') 
        for i, extra in enumerate(found_anime):
            print(f'[{i}] {extra}') 
        num = int(input())
        found_anime = [found_anime[num]]
    
    path = ANIME_PATH + '\\' + found_anime[0]
    
    sub_format = str(input("Extension of subtitle files(ex: .sub, .srt, etc): "))
    
    vidFiles = [name for name in os.listdir(path) if name.endswith('.mp4') or name.endswith('.mkv') or name.endswith('.avi')]
    subFiles = [name for name in os.listdir(path) if name.endswith(sub_format)]
    
    sort_nicely(vidFiles)
    sort_nicely(subFiles)
    
    # vidFiles.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    # subFiles.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))

    os.chdir(path)
    
    # sync_bool = input('Would you like to sync the files as well?(y/n):')
    try:
        assert(len(subFiles)==len(vidFiles))
        # if sync_bool == 'y':
        #     os.mkdir('OLD_SUBS')
        #     for i,vname in enumerate(vidFiles):
        #         os.system(f'ffs "{vname}" -i "{subFiles[i]}" -o "{os.path.splitext(vname)[0]+sub_format}"')
        #         os.rename(subFiles[i], 'OLD_SUBS' + '\\' + subFiles[i])

        #     print('Done syncing and renaming!')
        #     return
        for i,vname in enumerate(vidFiles):
            print("{0} renamed to {1} ".format(subFiles[i], os.path.splitext(vname)[0]))
            os.rename(subFiles[i], os.path.splitext(vname)[0]+sub_format)
    except AssertionError:
        print(len(subFiles))
        print(len(vidFiles))
    #print("\nPress Q to Quit")
    #msvcrt.getch()
    print('Done renaming!')
    return 

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def main():
    if is_admin():
        rename_subs(arg_parsing(), get_anime_dir())
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    
if __name__ == "__main__":
    main()
    

