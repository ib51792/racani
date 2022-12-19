#!/usr/bin/env python

import json
from src.scene import Scene


if __name__ == "__main__":
    
    # read setup json file
    with open('setup.json', 'r') as file: 
        _json = json.load(file)
        
    Scene(_json).main()
