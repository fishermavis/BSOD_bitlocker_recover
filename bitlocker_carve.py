###Thank you to https://github.com/WithSecureLabs/bitlocker-spi-toolkit for the initial code which made this possible

import re
import os
import sys

def find_keys(file_path): #Check for MEMORY.DMP file
    
    if not os.path.isfile(file_path):
        print(f"[-] File {file_path} not found. Please try again.")
        return []

    print(f"[+] Found {file_path}.")

    try:
        with open(file_path, 'rb') as f:    #Open the BSOD dumo
            binary_data = f.read()          #Read entrie file
        
        data = binary_data.hex()            #Convert the file data to a hex string

        keys = re.findall(                  #Search BSOD for Volume Master Key Header 
            r'2c000[0-6]000[1-9]000[0-1]000[0-5]200000(\w{64})', data)

        filtered_keys = [key for key in keys if not re.search(r'00{5,}', key)] #Remove false possitive with 4 consecutive '00' bytes

        return filtered_keys #Return found keys or empty list
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def main():
    
    if len(sys.argv) != 2:
        print("\nNo file given. Please specify file name.\n")
        print("Command line example: python bitlocker_carve.py MEMORY.DMP\n")
        input("Press Enter to exit...")
        return

    file_path = sys.argv[1]

    keys = find_keys(file_path) #Run the function which finds keys

    if keys:
        print(f'[+] Found {len(keys)} potential BitLocker VMK key(s):') #Display found keys
        for i, key in enumerate(keys, start=1):
            print(f"    {i}: {key}")
    else:
        print('[-] No keys found.')

    input("Press Enter to exit...") #Keep the script open so the user can read the output

if __name__ == "__main__":
    main()
