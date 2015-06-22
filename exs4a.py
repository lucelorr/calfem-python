# example exs4a 
# ----------------------------------------------------------------
# PURPOSE 
#    Analysis of a plane truss using loops.
# ----------------------------------------------------------------

# REFERENCES
#     P-E Austrell 1994-03-08 
#     K-G Olsson 1995-09-28
#     O Dahlblom 2004-08-31
#     J Lindemann 2009-01-25
# ----------------------------------------------------------------

from numpy import *
from calfem.core import *

# ----- Topology matrix Edof -------------------------------------

Edof = array([
    [1, 2, 5, 6],
    [3, 4, 7, 8],
    [5, 6, 9, 10],
    [7, 8, 11, 12],
    [7, 8, 5, 6],
    [11, 12, 9, 10],
    [3, 4, 5, 6],
    [7, 8, 9, 10],
    [1, 2, 7, 8],
    [5, 6, 11, 12]
])
 
# ----- Stiffness matrix K and load vector f ---------------------

K=zeros([12,12])
f=zeros([12,1])
f[10]=0.5e6*sin(pi/6)
f[11]=-0.5e6*cos(pi/6)

# ----- Element properties ---------------------------------------

A=25.0e-4
E=2.1e11
ep=[E,A]

# ----- Element coordinates --------------------------------------

ex = array([
    [0., 2.],
    [0., 2.],
    [2., 4.],
    [2., 4.],
    [2., 2.],
    [4., 4.],
    [0., 2.],
    [2., 4.],
    [0., 2.],
    [2., 4.]
])

ey = array([
    [2., 2.],
    [0., 0.],
    [2., 2.],
    [0., 0.],
    [0., 2.],
    [0., 2.],
    [0., 2.],
    [0., 2.],
    [2., 0.],
    [2., 0.]
])
 
# ----- Create element stiffness matrices Ke and assemble into K -

for elx, ely, eltopo in zip(ex, ey, Edof):
    Ke = bar2e(elx, ely,ep)
    assem(eltopo,K,Ke)
   
print("Stiffness matrix K:")
print(K)

# ----- Solve the system of equations ----------------------------

bc = array([1,2,3,4])
a, r = solveq(K,f,bc)

print("Displacements a:")
print(a)

print("Reaction forces r:")
#print(r)

# ----- Element forces -------------------------------------------

ed=extractEldisp(Edof,a);
N=zeros([Edof.shape[0]])

print("Element forces:")

i = 0
for elx, ely, eld in zip(ex, ey, ed):
    N[i] = bar2s(elx,ely,ep,eld);
    print("N%d = %g" % (i+1,N[i]))
    i+=1
 
