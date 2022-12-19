import numpy as np

def readFile(self, filepath):
    for line in filter(None, open(filepath, 'r').read().splitlines()):
        line = line.split(); vf = line.pop(0)
        
        match vf:
            case "v": self.vertices.append(list(np.float_(line)))
            case "f": self.polygons.append(list(np.int_(line)))
        