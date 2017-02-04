#!/usr/bin/python3.4
import sys
import hashlib
import os
import time
from functools import partial

#Ignores all extentions mentioned here
#Do not include the dot
#To ignore all files without extention, add ""
#To ignore all mp4 files etc, add "mp4"
ignore_extentions = [
]


print("Collecting all files to be checked..")
filenames = []
for directory in os.walk('.'):
    dirname = directory[0]
    for filename in directory[2]:
        if len(filename.split('.')) > 1:
            extention = filename.split('.')[-1]
        else:
            extention = ''
        if not extention in ignore_extentions:
            filenames.append(dirname + '/' + filename)
print(len(filenames), "files in total")
hashes = []

print("Collecting hashes for all files..")

i = 0
start = time.time()
for filename in filenames:
    if ((i+1)%10 == 0):
        filesPerSecond = i / (time.time() - start)
        print(int(i/len(filenames)*10000)/100, "percent checked.. Around {} seconds left".format(int((len(filenames)-i)/filesPerSecond)))
    i += 1

    try:
        with open(filename, 'rb') as f:
            d = hashlib.md5()
            for buf in iter(partial(f.read, 128), b''):
                d.update(buf)
            hashes.append([d.hexdigest(), filename])
    except FileNotFoundError as e:
        pass


#Check hashes for duplicates
duplicates = []
for entry in hashes:
    for compare in hashes:
        if entry[0] == compare[0] and entry[1] != compare[1]:
            duplicates.append([entry[1], compare[1]])
            print("File has duplicate:", entry[1], compare[1])


print('\n'*24)
if duplicates:
    print(len(duplicates), "Files have duplicates")
    for duplicate in duplicates:
        print('\t' + duplicate[0] + ' - ' + duplicate[1])
    print(len(duplicates), "duplicates found")
else:
    print("All files are different. Celebrate diversity!")
