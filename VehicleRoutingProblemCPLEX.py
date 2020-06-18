import matplotlib.pyplot as plt
import numpy as np
from docplex.mp.model import Model
rnd = np.random
rnd.seed(4)
n = 10  # number of clients
xc = rnd.rand(n + 1) * 20
yc = rnd.rand(n + 1) * 10
# xc = rnd.rand(len(V))*20
# yc = rnd.rand(len(V))*10
# # put on map the Depot coordonates
# plt.plot(xc[0], yc[0], c='r', marker='s')
# # put on map the Clients coordonates
# plt.scatter(xc[1:], yc[1:], c='b')
# set of clients
N = [i for i in range(1, n + 1)]
print("(set of clients) N = ", N)
# union of 0 & N
V = [0] + N
print("(union of 0 & N) V = ", V)
# set of arcs
A = [(i, j) for i in V for j in V if i != j]
print("(set of arcs) A = ", A)
# cost of travel
c = {(i, j): np.hypot(xc[i] - xc[j], yc[i] - yc[j]) for i, j in A}
print("(cost of travel) c = ", c)
# Q = vehicle capacity
Q = 20
print("(vehicle capacity) Q = ", Q)
# the amount that has to be delivered for each custumer
q = {i: rnd.randint(1, 10) for i in N}
print("(the amount that has to be delivered for each custumer) q = ", q)

# print(plt.scatter(loc_x[1:],loc_y[1:],c='b'))
for i in N:
    plt.annotate('$q_%d=%d' % (i, q[i]), (xc[i], yc[i]))
plt.plot(xc[0], yc[0], c='r', marker='s')
plt.axis('equal')
# plt.show()


mdl = Model('MIP Model')
x = mdl.binary_var_dict(A, name='x')
u = mdl.continuous_var_dict(N, ub=Q, name='u')
# print("Afisarea lui x:",x)
# print("Afisarea lui u:",u)

mdl.minimize(mdl.sum(c[i, j] * x[i, j]for i, j in A))
mdl.add_constraints(mdl.sum(x[i, j] for j in V if j != i) == 1 for i in N)
mdl.add_constraints(mdl.sum(x[i, j]for i in V if i != j) == 1 for j in N)
mdl.add_indicator_constraints(mdl.indicator_constraint(
    x[i, j], u[i] + q[j] == u[j]) for i, j in A if i != 0 and j != 0)
mdl.add_constraints(u[i] >= q[i] for i in N)
mdl.parameters.timelimit = 15
solution = mdl.solve(log_output=True)

# print(solution)
# print(solution.solve_status)

active_arcs = [a for a in A if x[a].solution_value > 0.9]
print("Active arcs =  ", active_arcs)

for i in N:
    plt.annotate('$q_%d=%d' % (i, q[i]), (xc[i], yc[i]))

for i, j in active_arcs:
    plt.plot([xc[i], xc[j]], [yc[i], yc[j]], c='g', alpha=0.3)
# put on map the Depot coordonates
plt.plot(xc[0], yc[0], c='r', marker='s')
# put on map the Clients coordonates
plt.scatter(xc[1:], yc[1:], c='b')
# plt.axis('equal')
plt.show()
