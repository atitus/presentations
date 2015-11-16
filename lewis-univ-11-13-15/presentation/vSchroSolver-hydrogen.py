from __future__ import division
from visual import *
from visual.graph import *

#x is in nm and E is in eV
E_rest=0.511e6
hc=1240
E=-3.39 

####Calculate and Plot V
#values of x in plot
N=1000

#left edge
x_left=0.05 #nm

#right edge
x_right=2 #nm

#dx
dx=(x_right-x_left)/N

#Define and graph V
VGraphWindow = gdisplay(x=0,y=0,width=400, ymin=-15, xmin=0)
Vgraph=gcurve()

for x in arange(x_left,x_right,dx):
    Vvalue=-8.98755179e9*(1.602e-19)**2/(x*1e-9)/1.602e-19
    Vgraph.plot(pos=(x,Vvalue))


#Define and graph Psi
Psi_0=0
Psi_1=1e-5

#left edge
x_left=0.00001 #nm

#right edge
x_right=1.5 #nm

#values of x
N=10000

#dx
dx=(x_right-x_left)/N

#create graph window for Psi
PsiGraphWindow = gdisplay(x=0,y=400,width=400, xmin=0)
Psigraph=gcurve(color=color.cyan)


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
        Vvalue=-8.98755179e9*(1.602e-19)**2/(x*1e-9)/1.602e-19
        f=2*Psi[i-1]-Psi[i-2]-8*pi*pi*E_rest/(hc*hc)*dx*dx*(E-Vvalue)*Psi[i-1]
        Psi.append(f)
        Psigraph.plot(pos=(x,f))
    i=i+1

###find the integral of Psi^2 dx
##integral=0
##for j in arange(0,len(Psi),1):
##    integral=integral+Psi[j]*Psi[j]*dx
##
###calculate the constant A^2 that normalizes the integral of Psi^2 dx
##Asquared=1/integral
##A=sqrt(Asquared)
##
###calculate the normalized Psi
##PsiNormalized=[]
##for j in arange(0,len(Psi),1):
##    PsiNormalized.append(A*Psi[j])
##
###create graph window for Psi
##Psi2GraphWindow = gdisplay(x=0,y=400,width=400, xmin=0)
##Psi2graph=gcurve(color=color.magenta)
##
###graph the normalized Psi
##i=0
##for x in arange(x_left,x_right,dx):
##    Psi2graph.plot(pos=(x,PsiNormalized[i]))
##    i=i+1
##
###find the integral of Normalized Psi^2 dx and show it is 1
##integral=0
##for j in arange(0,len(PsiNormalized),1):
##    integral=integral+PsiNormalized[j]*PsiNormalized[j]*dx
##
##print(PsiNormalized[len(PsiNormalized)-1])
##
