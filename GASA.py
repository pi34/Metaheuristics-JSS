import random
import numpy as np
import math

machNo = 3 # int(input("How many machines do you have? "))
job = 3 # int(input("How many jobs do you have? "))
tasks = 3 #int(input("How many tasks in each job?"))

crRate = 0.8
mutRate = 0.2

machines = []
times = []

for i in range(job):
    curr = []
    currT = []
    for j in range(tasks):
        curr.append(int(input())-1)
        currT.append(int(input()))
    machines.append(curr)
    times.append(currT)

randArr = tasks * [i for i in range(job)]

def encode(popSize):
    finPop = []

    for _ in range(popSize):
        finPop.append(random.sample(randArr, job*tasks))

    return finPop


def fitness(chromosome):
    machT = [0 for _ in range(machNo)]
    jobs = [0 for _ in range(tasks)]

    started = []

    for _ in range(job):
        arr = []
        for _ in range(tasks):
            arr.append(0)
        started.append(arr)

    for i in chromosome:
        machine = machines[i][jobs[i]]
        time = times[i][jobs[i]]
        prevTime = times[i][jobs[i]-1]
        if jobs[i] != 0:
            if (machT[machine] > started[i][jobs[i]-1]+prevTime):
                started[i][jobs[i]] = machT[machine]
                machT[machine] += time
            else:
                started[i][jobs[i]] = started[i][jobs[i]-1]+prevTime
                machT[machine] = started[i][jobs[i]] + time
        else:
            started[i][jobs[i]] = machT[machine]
            machT[machine] += time

        jobs[i] += 1

    makespan = max(machT)

    return makespan


def rouletteWheel (pop, fitnesses):
    invSm = sum([1/k for k in fitnesses])
    probs = [(1/k)/invSm for k in fitnesses]
    
    chc = np.random.choice(range(len(pop)), p=probs)
    return pop[chc]


def crossover (par1, par2):
    child1 = list(par1)
    child2 = list(par2)

    randm = random.randint(0, len(child1))

    if (random.random() <= crRate):
        child1[randm::], child2[randm::] = child2[randm::], child1[randm::]

    return child1, child2


def fixCrossover (child):
    counts = [0 for _ in range(machNo)]

    for i in child:
        counts[i] += 1

    more = []
    less = []

    for i in range(machNo):
        if counts[i] > machNo:
            more.append([i, counts[i] - machNo])
        elif counts[i] < machNo:
            less.append([i, machNo - counts[i]])

    for i in more:
        while i[1] > 0:
            currInd = child.index(i[0])
            currLess = less[0]
            child[currInd] = currLess[0]
            less[0][1] -= 1
            if (less[0][1] == 0):
                less.pop(0)
            i[1] -= 1

    return child


def mutation (child):

    if (random.random() <= mutRate):
        ind1 = random.randint(0, len(child)-1)
        ind2 = random.randint(0, len(child)-1)

        child[ind1], child[ind2] = child[ind2], child[ind1]
        
    return child

# SA

def metropolis (oldF, newF, tmp):
    return math.exp(-abs(newF - oldF) / tmp)


def perturb (old):
    f = random.randint(0, len(old)-1)
    s = random.randint(f, len(old)-1)

    annealed = list(old)
    annealed[f:s] = reversed(annealed[f:s])

    return annealed


def accept (newF, oldF, tmp):
    if (newF < oldF):
        return True
    else:
        if (random.random() < metropolis(oldF, newF, tmp)):
            return True
        else: return False


def simulated (currSol):
    temp = 100
    stopTemp = 0.00001

    rate = 0.9995
    iters = 50

    sols = []

    for _ in range (iters):
        if (temp > stopTemp):

            sols.append(currSol)
            
            neighbour = perturb(currSol)
            if accept(fitness(currSol), fitness(neighbour), temp):
                currSol = neighbour

            temp *= rate

    return currSol

# Driver Code

popSize = 30

# Generate Population
genome = encode(popSize)

# Recording the best makespan
bests = []

for _ in range(30):

    # Calculate Fitness
    fitnesses = []

    for i in genome:
        fitnesses.append(fitness(i))

    #for i in genome:
    #    print (i)

    #print("change")

    bests.append(min(fitnesses))

    # Selection
    selected = [rouletteWheel(genome, fitnesses) for _ in range(popSize)]

    # Crossover and Mutation

    childPop = []

    for i in range(0, popSize, 2):
        par1 = selected[i]
        par2 = selected[i+1]

        children = crossover(par1, par2)
        child1 = mutation(fixCrossover(children[0]))
        child2 = mutation(fixCrossover(children[1]))

        childPop.append(child1)
        childPop.append(child2)

    arr = [(fitness(childPop[i]), i) for i in range(popSize)]
    arr = sorted(arr, reverse=True)

    genome = []

    for j in range(popSize):
        if j <= popSize//2:
            genome.append(simulated(childPop[arr[j][1]]))
        else:
            genome.append(childPop[arr[j][1]])


for i in range(len(bests)):
    print ("Best Makespan for Generation", i, "is:", bests[i])

