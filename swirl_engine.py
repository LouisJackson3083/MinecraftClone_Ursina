from ursina import Vec2

class SwirlEngine:
    def __init__(self,subWidth):
        self.subWidth = subWidth

        self.run = 1
        self.iteration = 0
        self.count = 0

        # Tracks position of terrain subset being generated
        self.pos = Vec2(0,0)

        self.cd = 0 # Current Direction
        self.dir = [Vec2(0,1), # Array of directions
                    Vec2(1,0),
                    Vec2(0,-1),
                    Vec2(-1,0)]

    def changeDirection(self):
        if self.cd < 3:
            self.cd+=1
        else:
            self.cd=0
            self.iteration+=1

        if self.cd < 2:
            self.run = (self.iteration * 2) - 1
        else:
            self.run = self.iteration * 2

    def move(self):
        if self.count < self.run:
            self.pos.x += self.dir[self.cd].x*self.subWidth
            self.pos.y += self.dir[self.cd].y*self.subWidth
            self.count += 1
        else:
            self.count=0
            self.changeDirection()