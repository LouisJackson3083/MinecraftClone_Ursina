from ursina import *
from perlin import Perlin

class MeshTerrain:
    def __init__(self):
        self.block = load_model('assets/models/block.obj')
        self.textureAtlas = load_texture('assets/textures/texture_atlas_3.png')

        self.subsets = []
        self.numSubsets = 1
        self.subWidth = 16 # Width of chunk

        # Our terrain dictionary
        self.td = {} 

        self.perlin = Perlin()

        for i in range(0,self.numSubsets):
            e = Entity(model=Mesh(),
                        texture=self.textureAtlas)
            e.texture_scale*=128/e.texture.width
            self.subsets.append(e)

    def genBlock(self,x,y,z): # Extend or add to the vertices of our model - This is what takes time
        model = self.subsets[0].model
        model.vertices.extend([Vec3(x,y,z) + v for v in self.block.vertices])
       
        self.td["x"+str(floor(x))+"y"+str(floor(y))+"z"+str(floor(z))] = "t" # Records terrain in dictionary
        uu=8 # This is the texture coords for grass
        uv=7
        if y > 2:
            uu = 8
            uv = 6
        model.uvs.extend([Vec2(uu,uv) + u for u in self.block.uvs])

    def generateTerrain(self):
        x = 0
        z = 0
        distance = int(self.subWidth*0.5)
        count = 1
        for k in range(-distance,distance):
            for j in range(-distance,distance):
                y = floor(self.perlin.getHeight(x+k,z+j))
                self.genBlock(x+k, y, z+j)
                count+=1

        print("Blocks generated: ",str(count))
        self.subsets[0].model.generate()
