import pants
import math
import random
import matplotlib.pyplot as plt
nodes = []
for _ in range(20):
    x = random.uniform(-10, 10)
    y = random.uniform(-10, 10)
    nodes.append((x, y))


def euclidean(a, b):
    return math.sqrt(pow(a[1] - b[1], 2) + pow(a[0] - b[0], 2))


world = pants.World(nodes, euclidean)
solver = pants.Solver()
solution = solver.solve(world)
# or
solutions = solver.solutions(world)
print(solution.distance)
print(solution.tour)    # Nodes visited in order
print(solution.path)    # Edges taken in order
# or
best = float("inf")
for solution in solutions:
    assert solution.distance < best
    best = solution.distance
fig, ax = plt.subplots()
# Pacientii
xPacient = [i[0] for i in nodes]
yPacient = [i[1] for i in nodes]
desenCoordonatePacienti = plt.scatter(
    xPacient, yPacient, c='b')  # pune pacientii pe axa
for z in range(0, len(solution.tour)-1):
    plt.plot([solution.tour[z][0], solution.tour[z+1][0]],
             [solution.tour[z][1], solution.tour[z+1][1]], c='g', alpha=0.6)
plt.show()
