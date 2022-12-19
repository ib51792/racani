
class Collision:

    def testCollision(self, maze, x, z, pad=0.3, cubeSize=2):

        row, col = (0, 0)
        wallX, wallZ = (0.0, 0.0)

        hitBox = ((cubeSize / 2) + pad)

        for i in maze:

            wallZ = (row * (cubeSize * -1))

            for j in i:
                if (j == 0):
                    col += 1
                    continue

                wallX = (col * (cubeSize * -1))

                # collision with cube
                if ((z == wallZ) or ((z > (wallZ - hitBox)) and (z < (wallZ + hitBox)))) and \
                   ((x == wallX) or ((x > (wallX - hitBox)) and (x < (wallX + hitBox)))):
                    return True

                col += 1

            row += 1
            col = 0

        return False
    