import random
import numpy as np
import math

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

def encode():
    return (random.sample(randArr, job*tasks))


def objective(inp):
    machT = [0 for _ in range(machNo)]
    jobs = [0 for _ in range(tasks)]

    started = []

    for _ in range(job):
        arr = []
        for _ in range(tasks):
            arr.append(0)
        started.append(arr)

    for i in inp:
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


temp = 1000
stopTemp = 0.00000001

rate = 0.9995
iters = 1000

currSol = encode()

sols = []

for _ in range (iters):
    if (temp > stopTemp):

        sols.append(currSol)
        
        neighbour = perturb(currSol)
        if accept(objective(currSol), objective(neighbour), temp):
            currSol = neighbour

        temp *= rate
