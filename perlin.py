from perlin_module import PerlinNoise

class Perlin:
    def __init__(self):

        self.seed = self.getSeed("yo")
        self.octaves = 8
        self.freq = 256
        self.amp = 24

        self.pNoise = PerlinNoise(  seed=self.seed,
                                    octaves=self.octaves)
    def getHeight(self,x,z):
        y = 0
        y = self.pNoise([x/self.freq,z/self.freq])*self.amp
        return y

    def getSeed(self, plainText):
        cipherText = 0
        for i in range(len(plainText)):
            cipherText += ord(plainText[i])
        return cipherText