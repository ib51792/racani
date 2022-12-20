import math

def getIntendedPosition(cameraRotation=0, x=0, z=0, angle=90, modifier=1, stepSize=0.05):
    position = [x, 0, z]
    dx =  math.cos(math.radians(cameraRotation + angle))
    dz =  math.sin(math.radians(cameraRotation + angle))
    position[0] += (dx * modifier) * stepSize
    position[2] += (dz * modifier) * stepSize
    return position[0], position[2]
