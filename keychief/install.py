# usr/bin/python3
import os

def install(directory_name: str = None ) -> None:
    
    if not os.path.exists(directory_name):
        print(f"Creating directory {directory_name}")
        os.mkdir(directory_name)
        return
    print(f"{directory_name} exists")
    return

