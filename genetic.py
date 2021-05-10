
import random


class Color:
    def __init__(self,rgb):
        self.rgb=rgb
        self.parent=[]

    def set_parent(self, clr):
        self.parent.append(clr)
    
    def set_rgb(self,rgb):
        self.rgb = rgb
    
    def get_rgb(self):
        return self.rgb
    
    def get_parent(self):
        return self.parent

class Fitness:
    def __init__(self,clr):
        self.clr = clr
        self.rgb = None
        self.newColor = []
        self.fitness = 0.0
    
    def mixing(self):
        if self.rgb == None:
            mix = [0,0,0]
            newClr = Color((0,0,0))
            currClr = self.clr[0]
            nextClr = self.clr[1]
            # red
            mix[0] = random.choice([currClr.rgb[0],nextClr.rgb[0]])
            #green
            mix[1] = random.choice([currClr.rgb[1],nextClr.rgb[1]])
            #blue
            mix[2] = random.choice([currClr.rgb[2],nextClr.rgb[2]])
            #set parent
            newClr.set_parent(currClr)
            newClr.set_parent(nextClr)
            # print(mix,nextClr.rgb)
            newClr.set_rgb(tuple(mix))
        
            self.rgb=tuple(mix)
            self.newColor.append(newClr)
            return self.rgb

    def fitness_score(self):
        if self.fitness == 0:
            self.mixing()
            self.fitness = 1/float(self.rgb[0]+self.rgb[1]+self.rgb[2])
        return self.fitness

def initalPopulation(popSize):
    population = []

    for i in range(0,popSize):
        r = random.randint(0,255)
        g = random.randint(0,255)
        b = random.randint(0,255)
        population.append((r,g,b))
    return population

def rankColor(population):
    fitnessResults={}
    newColor=[]
    choice=[]
    
    for i in range(0,len(population)):
        idx1 = random.randint(0,len(population)-1)
        idx2 = random.randint(0,len(population)-1)

        choice.append(population[idx1])
        choice.append(population[idx2])
       
        c1 = random.choice(choice)
        c2 = random.choice(choice)
        clr1 = Color(c1)
        clr2 = Color(c2)

        parent =[clr1,clr2]
        fit = Fitness(parent)
        fitnessResults[i]= fit.fitness_score()
        newColor.append(fit.newColor[0])

    return fitnessResults, newColor

def cleanDict(score,newClr):
    newDict={}
    count = 0
    for k in score.keys():
        # print(newClr[count].rgb,newClr[count].parent[0].rgb,newClr[count].parent[1].rgb)
        newDict[newClr[count]] = score[k]
        count += 1
    return newDict

def clr2List(clr):
    ret = []
    for c in clr:
        ret.append(c.rgb)
    return ret

def rgb2hex(r,g,b):
     return '#%02x%02x%02x' % (r, g, b)

# populate = initalPopulation(10)
# score, newClr = rankColor(populate)

# # print(cleanDict(score,newClr))
# # print(len(newClr))
# nextGen = clr2List(newClr)
# score1, newClr1 = rankColor(nextGen)
# retDict = {k: v for k, v in sorted(cleanDict(score1, newClr1).items(), key=lambda item: item[1])}
# clr = list(retDict.keys())[-1]
# r = clr.rgb[0]
# g = clr.rgb[1]
# b = clr.rgb[2]
# parent1r = clr.parent[0].rgb[0]
# parent1g = clr.parent[0].rgb[1]
# parent1b = clr.parent[0].rgb[2]
# parent2r = clr.parent[1].rgb[0]
# parent2g = clr.parent[1].rgb[1]
# parent2b = clr.parent[1].rgb[2]
# print(rgb2hex(r,g,b) + " descendant of : "+ rgb2hex(parent1r,parent1b,parent1b) + " and " + rgb2hex( parent2r, parent2g, parent2b))