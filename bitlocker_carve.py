###Thank you to https://github.com/WithSecureLabs/bitlocker-spi-toolkit for the initial code which made this possible
##Added functionality so that only 100mb of a file is loaded to memory at any given type so tool can be used for large disk dumps

import re
import os
import sys

def find_keys(file_path):
    if not os.path.isfile(file_path):
        print(f"[-] File {file_path} not found. Please try again.")
        return []

    print(f"[+] Found {file_path}.")

    chunk_size = 100 * 1024 * 1024  # 100MB
    overlap = 1 * 1024 * 1024  # 1MB
    found_keys = set()

    try:
        with open(file_path, 'rb') as f:
            while True:
                current_pos = f.tell()
                chunk = f.read(chunk_size)
                if not chunk:
                    break

                data = chunk.hex()

                keys = re.findall(
                    r'2c000[0-6]000[1-9]000[0-1]000[0-5]200000(\w{64})', data)

                for key in keys:
                    if not re.search(r'00{5,}', key):
                        found_keys.add(key)

                if f.tell() < os.path.getsize(file_path):
                    f.seek(current_pos + chunk_size - overlap)
                
        return list(found_keys)
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
