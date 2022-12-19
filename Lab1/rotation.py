import numpy as np

def rotation(currOrient, newOrient):
    dotCurrNext = np.dot(currOrient, newOrient)
    currNorm = np.linalg.norm(currOrient)
    nextNorm = np.linalg.norm(newOrient)
    rotAngle = np.rad2deg(np.arccos(dotCurrNext / (currNorm * nextNorm)))
    return np.cross(currOrient, newOrient), rotAngle

def rotationDCM(tangent, d2):
    tangent = tangent / np.linalg.norm(tangent)
    d2 = d2 / np.linalg.norm(d2)
    allZeros = not np.any(d2)
    w = tangent
    if allZeros:
        u = tangent
    else:
        u = np.cross(tangent, d2)
    v = np.cross(w, u)
    R = np.array([[w[0], u[0], v[0], 0], [w[1], u[1], v[1], 0], [w[2], u[2], v[2], 0], [0, 0, 0, 1]])
    return np.linalg.inv(R)