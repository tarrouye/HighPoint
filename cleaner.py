import os
from os import listdir
import sys

current_path = os.path.dirname(os.path.realpath(__file__)) + "/"

yes = []
nope = []

loop1 = True

protected = ['requirements', 'companies']

for file_name in listdir(current_path):
    trip = False
    for p in protected: # don't give the option of removing protected files
        if p in file_name:
            trip = True
    if trip:
        continue
        
    if (file_name.endswith('.txt') or file_name.endswith('.csv')): # we are only concerned with cleaning .txt and .csv files
        nope.append(file_name)
        
        if loop1:
            ask = input("Would you like to remove '" + current_path + file_name + "'? [y/n/q]: ")
        
            if (ask == 'q' or ask == 'Q'):
                loop1 = False
                continue
            
            loop2 = True
            while (loop2):
                if (ask == 'y' or ask == 'Y'):
                    os.remove(current_path + file_name)
                    yes.append(file_name)
                    nope.remove(file_name)
                    loop2 = False
                elif (ask == 'n' or ask == 'N'):
                    loop2 = False
                else:
                    print("Invalid input. ")
                
# output a log so the user knows what happened
print()
print("------------------------")

for y in yes:
    print("Removed: " + y)
    
print("------------------------")
    
for n in nope:
    print("Untouched: " + n)
    
print("------------------------")
    
print("Exiting cleaner.")
print()