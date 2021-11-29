from ursina import *
from perlin import Perlin
from random import random
from swirl_engine import SwirlEngine

class MeshTerrain:
    def __init__(self):
        self.block = load_model('assets/models/block.obj')
        self.textureAtlas = load_texture('assets/textures/texture_atlas_3.png')
        self.numVertices = len(self.block.vertices)

        self.subsets = []
        self.numSubsets = 512
        self.subWidth = 8 # Width of chunk
        self.swirlEngine = SwirlEngine(self.subWidth)
        self.currentSubset = 0

        # Our terrain dictionary
        self.td = {} 

        self.perlin = Perlin()

        for i in range(0,self.numSubsets):
            e = Entity(model=Mesh(),
                        texture=self.textureAtlas)
            e.texture_scale*=128/e.texture.width # 128 is the width of the individual texture (32 * 4 bc 4 spaces)
            self.subsets.append(e)

    def genBlock(self,x,y,z): # Extend or add to the vertices of our model - This is what takes time
        model = self.subsets[self.currentSubset].model
        model.vertices.extend([Vec3(x,y,z) + v for v in self.block.vertices])
       
        self.td["x"+str(floor(x))+
                "y"+str(floor(y))+
                "z"+str(floor(z))] = "t" # Records terrain in dictionary

        # Decide random color of block
        c = random()-0.5
        model.colors.extend((Vec4(1-c,1-c,1-c,1),)*self.numVertices)

        uu=8 # This is the texture coords for grass
        uv=7
        if y > 2:
            uu = 8
            uv = 6
        model.uvs.extend([Vec2(uu,uv) + u for u in self.block.uvs])

    def generateTerrain(self):
        # Get current position as we swirl around
        x = floor(self.swirlEngine.pos.x)
        z = floor(self.swirlEngine.pos.y)

        distance = int(self.subWidth*0.5)
        count = 1
        for k in range(-distance,distance):
            for j in range(-distance,distance):
                y = floor(self.perlin.getHeight(x+k,z+j))

                if self.td.get( "x"+str(floor(x+k))+
                                "y"+str(floor(y))+
                                "z"+str(floor(z+j))) !="t":
                    self.genBlock(x+k, y, z+j)
                    count+=1

        print("Blocks generated: ",str(count),str(len(self.td)))

        # Current subset hack
        self.subsets[self.currentSubset].model.generate()
        if self.currentSubset<self.numSubsets-1:
            self.currentSubset+=1
        else: self.currentSubset=0
        self.currentSubset+=1

        self.swirlEngine.move()
