from __future__ import division
from visual import *
from visual.graph import *

#x is in nm and E is in eV
E_rest=0.511e6
hc=1240
E=hc*hc/8/E_rest/1
#E=0.9611825 #ground state for L=0.5
E=0.29766 #ground state for L=1
E=2.6525

#values of x
N=1000

#left edge
x_left=-1

#right edge
x_right=1

#dx
dx=(x_right-x_left)/N

#Define and graph V
V=[]
Vmax=10

GraphWindow = gdisplay(x=0,y=0,width=400, ymax=Vmax, ymin=-Vmax, xmin=2*x_left, xmax=2*x_right)
Vgraph=gcurve()

PsiGraphWindow = gdisplay(x=0,y=400,width=400,ymin=0, xmin=x_left, xmax=x_right)
Psigraph=gcurve(color=color.cyan)

Psi2GraphWindow = gdisplay(x=0,y=400,width=400,ymin=0, ymax=2, xmin=x_left, xmax=x_right)
Psi2graph=gcurve(color=color.magenta)


for x in arange(x_left,x_right,dx):
    leftWall=-0.5
    rightWall=0.5
    if(x<leftWall):
        V.append(Vmax)
        Vgraph.plot(pos=(x,Vmax))
    elif(x>rightWall):
        V.append(Vmax)
        Vgraph.plot(pos=(x,Vmax))
    else:
        V.append(0)
        Vgraph.plot(pos=(x,0))

#Define and graph Psi
Psi_0=0
Psi_1=1e-5

Psi=[]
i=0
for x in arange(x_left,x_right,dx):
    if(i==0):
        Psi.append(Psi_0)
        Psigraph.plot(pos=(x,Psi_0))
    elif(i==1):
        Psi.append(Psi_1)
        Psigraph.plot(pos=(x,Psi_1))
    else:
        f=2*Psi[i-1]-Psi[i-2]-8*pi*pi*E_rest/(hc*hc)*dx*dx*(E-V[i-1])*Psi[i-1]
        Psi.append(f)
        Psigraph.plot(pos=(x,f))
    i=i+1

#find the integral of Psi^2 dx
integral=0
for j in arange(0,len(Psi),1):
    integral=integral+Psi[j]*Psi[j]*dx

#calculate the constant A^2 that normalizes the integral of Psi^2 dx
Asquared=1/integral
A=sqrt(Asquared)

#calculate the normalized Psi
PsiNormalized=[]
for j in arange(0,len(Psi),1):
    PsiNormalized.append(A*Psi[j])

#graph the normalized Psi
i=0
for x in arange(x_left,x_right,dx):
    Psi2graph.plot(pos=(x,PsiNormalized[i]))
    i=i+1

#find the integral of Normalized Psi^2 dx and show it is 1
integral=0
for j in arange(0,len(PsiNormalized),1):
    integral=integral+PsiNormalized[j]*PsiNormalized[j]*dx

print(PsiNormalized[len(PsiNormalized)-1])
