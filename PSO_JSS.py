from math import inf
import random 
import numpy as np

machNo = 3 # int(input("How many machines do you have? "))
job = 3 # int(input("How many jobs do you have? "))
tasks = 3 #int(input("How many tasks in each job?"))

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

def generateSwarm(popSize):
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


def positionUpdate (sc, sb, sg, wc, wb, wg, leng):

    newPart = []
    ccount = 0
    bcount = 0
    gcount = 0
    
    genU = random.uniform(0, 1)

    while (len(newPart) < leng):

        if genU <= wc:
            newPart.append(sc[ccount])
            ccount+=1
        elif genU <= (wb + wg):
            newPart.append(sb[bcount])
            bcount+=1
        elif (wc + wb) <= genU:
            newPart.append(sg[gcount])
            gcount+=1

    return newPart

# Driver Code

iters = 20
swarmS = 10

wc = 0.2
wb = 0.3
wg = 0.5

swarm = generateSwarm(swarmS)

gBest = []
gFit = 1e99

for i in swarm:
    f = fitness(i)
    if f < gFit:
        gFit = f
        gBest = i

indBest = [swarm[i] for i in range(swarmS)]
indBF = [inf for _ in range(swarmS)]

for _ in range(iters):

    newPop = []

    for i in range(swarmS):
        curr = swarm[i]
        new = positionUpdate(curr, indBest[i], gBest, wc, wb, wg, tasks*job)
        fit = fitness(new)
        if fit <= indBF[i]:
            indBF[i] = fit
            indBest[i] = new
        newPop.append(new)

    for i in range(swarmS):
        if (indBF[i] <= gFit):
            gFit = indBF[i]
            gBest = indBest[i]

    swarm = list(newPop)
