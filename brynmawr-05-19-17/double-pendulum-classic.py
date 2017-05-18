# Converted from the VPython program 03_doublependula
from __future__ import division, print_function
from visual import *
from visual.graph import *
import wx

# Written by Bruce Sherwood, licensed under Creative Commons 4.0.
# All uses permitted, but you must not claim that you wrote it, and
# you must include this license information in any copies you make.
# For details see http://creativecommons.org/licenses/by/4.0

# Two double pendula, to illustrate high sensitivity to initial conditions
# in a simple system. Fall 2002.

# The analysis is in terms of Lagrangian mechanics.
# The Lagrangian variables are angle of upper bar, angle of lower bar,
# measured from the vertical.
#
# Corrections to the Lagrangian calculations by Owen Long, UC Riverside

scene.height = scene.width = 600
scene.background = color.white

g = 9.8
M1 = 2
M2 = 1
d = 0.05 # thickness of each bar
gap = 2*d # distance between two parts of upper, U-shaped assembly
L1 = 0.5 # physical length of upper assembly; distance between axles
L1display = L1+d # show upper assembly a bit longer than physical, to overlap axle
L2 = 1 # physical length of lower bar
L2display = L2+d/2 # show lower bar a bit longer than physical, to overlap axle
I1 = M1*L1**2/12 # moment of inertia of upper assembly
I2 = M2*L2**2/12 # moment of inertia of lower bar

hpedestal = 1.3*(L1+L2) # height of pedestal
wpedestal = 0.1 # width of pedestal
tbase = 0.05 # thickness of base
wbase = 8*gap # width of base
offset = 2*gap # from center of pedestal to center of U-shaped upper assembly
topofbar = vector(0,0,0) # top of inner bar of U-shaped upper assembly
scene.center = topofbar-vector(0,L1,0)

pedestal = box(pos=topofbar-vector(0,hpedestal/2,0), height=1.1*hpedestal, length=wpedestal, width=wpedestal, color=vector(0.4,0.4,0.5))
base = box(pos=topofbar-vector(0,hpedestal+tbase/2,0), height=tbase, length=wbase, width=wbase, color=pedestal.color)
axle = cylinder(pos=topofbar-vector(0,0,offset-gap/2+d/5), axis=vector(0,0,2*(offset-gap/2+d/5)), radius=d/4, color=color.yellow)

class pendulum:
# theta1 initial upper angle (from vertical)
# theta1dot initial rate of change of theta1
# theta2 initial lower angle (from vertical)
# theta2dot initial rate of change of theta2        
    def __init__(self, pos=topofbar, theta1=1, theta1dot=0, theta2=0, theta2dot=0):
        self.initial_pos = vector(pos)
        self.pos = pos
        self.frame1 = frame(pos=pos)
        self.initial_theta1 = theta1
        self.initial_theta1dot = theta1dot
        self.initial_theta2 = theta2
        self.initial_theta2dot = theta2dot
        b1 = box(frame=self.frame1, pos=vector(L1display/2-d/2,0,-(gap+d)/2), size=vector(L1display,d,d), color=color.red)
        b2 = box(frame=self.frame1, pos=vector(L1display/2-d/2,0,(gap+d)/2), size=vector(L1display,d,d), color=color.red)
        c = cylinder(frame=self.frame1, pos=vector(L1,0,-(gap+d)/2), axis=vector(0,0,gap+d), radius=axle.radius, color=axle.color)
        self.frame1.initial_pos = self.frame1.pos = vector(pos)
        self.frame1.rotate(angle=self.initial_theta1-pi/2, axis=vector(0,0,1))
        self.frame1.initial_axis = vector(self.frame1.axis)
        
        self.frame2 = frame()
        self.frame2.pos = pos+self.frame1.axis*L1
        self.frame2.initial_pos = vector(self.frame2.pos)
        b3 = box(frame=self.frame2, pos=vector(L2display/2-d/2,0,0), size=vector(L2display,d,d), color=color.green)
        self.frame2.initial_pos = self.frame2.pos = pos+self.frame1.axis*L1
        self.frame2.rotate(angle=self.initial_theta2-pi/2, axis=vector(0,0,1))
        self.frame2.initial_axis = vector(self.frame2.axis)
        self.__visible = True
        self.reset()
        
    def update(self, dtheta1=0, dtheta2=0):
        self.theta1 += dtheta1
        self.theta2 += dtheta2
        self.frame1.rotate(angle=dtheta1, axis=vector(0,0,1))
        self.frame2.pos = self.pos+self.frame1.axis*L1
        self.frame2.rotate(angle=dtheta2, axis=vector(0,0,1))
        
    def reset(self):
        self.pos = self.initial_pos
        self.frame1.pos = self.frame1.initial_pos
        self.frame2.pos = self.frame2.initial_pos
        self.theta1 = self.initial_theta1
        self.theta1dot = self.initial_theta1dot
        self.theta2 = self.initial_theta2
        self.theta2dot = self.initial_theta2dot
        self.frame1.axis = self.frame1.initial_axis
        self.frame2.axis = self.frame2.initial_axis
        
    def get_visible(self):
        return self.__visible
    
    def set_visible(self, vis):
        self.__visible = self.frame1.visible = self.frame2.visible = vis

pend1 = pendulum(topofbar+vector(0,0,offset), 2.1, 0, 2.4, 0)
pend2 = pendulum(topofbar+vector(0,0,-offset), 2.1, 0, 2.4, 0)
pend2.initial_theta1 += 0.001
pend2.reset()
pend2.set_visible(False)

pendula = [pend1, pend2]
scene.autoscale = False

run = False

def reset():
    global t, gd, energy_check
    t = 0
    ResetRunbutton()
    for pend in pendula:
        pend.reset()
    if gd:
        gd.display.delete()
        gd = None
        energy_check = False
        Graphbutton.SetLabel("Graph energy")

def ResetRunbutton():
    global run
    run = False
    Runbutton.SetLabel("Run")

def B_Runbutton(evt):
    global run
    run = not run
    if run:
        Runbutton.SetLabel("Pause")
    else:
        Runbutton.SetLabel("Run")

def B_Resetbutton(evt):
    reset()

def Menu_choose(evt):
    val = evt.GetSelection()
    if val == 0: # one double pendulum
        if not pendula[1].get_visible(): return
        pendula[1].set_visible(False)
    else:        # two double pendula
        if pendula[1].get_visible(): return
        pendula[1].set_visible(True)
    reset()

energy_check = False # if True, graph kinetic, potential, and total energy
gd = None
gK = None
gU = None
gE = None

def B_Graphbutton(evt):
    global energy_check, gd, gK, gU, gE, t
    energy_check = not energy_check
    if energy_check:
        if not gd:
            if pendula[1].get_visible:
                Casemenu.SetSelection(0)
                pendula[1].set_visible(False)
            gd = gdisplay(x=scene.width, width=scene.width, height=300, 
                          ytitle="K is green, U is blue, E = K+U is red",
                          foreground=color.black, background=color.white)
            t = 0
        gK = gcurve(color=color.green)
        gU = gcurve(color=color.blue)
        gE = gcurve(color=color.red)
        Graphbutton.SetLabel("Pause graph")
    else:
        Graphbutton.SetLabel("Graph energy")

controls = window(x=0, y=scene.height, width=scene.width, height=165, title='Controls')
p = controls.panel
Runbutton = wx.Button(p, label='Run', pos=(10,10))
Runbutton.Bind(wx.EVT_BUTTON, B_Runbutton)
Resetbutton = wx.Button(p, label='Reset', pos=(110,10))
Resetbutton.Bind(wx.EVT_BUTTON, B_Resetbutton)
t = wx.StaticText(p, pos=(10,55), label='Choose a situation:')
font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
t.SetFont(font)
    
menus = []
menus.append("One double pendulum")
menus.append("Two double pendula, starting with angles that differ by only 0.001 radian")
Casemenu = wx.Choice(p, choices=menus, pos=(130,50))
Casemenu.Bind(wx.EVT_CHOICE, Menu_choose)
Casemenu.SetSelection(0)

Graphbutton = wx.Button(p, label='Graph energy', pos=(10,90))
Graphbutton.Bind(wx.EVT_BUTTON, B_Graphbutton)

dt = 0.0002
t = 0
n = 0

C11 = (0.25*M1+M2)*L1**2+I1
C22 = 0.25*M2*L2**2+I2

while True:
    rate(1/dt)
    if not run: continue
    for pend in pendula:
        # Calculate accelerations of the Lagrangian coordinates:
        C12 = C21 = 0.5*M2*L1*L2*cos(pend.theta1-pend.theta2)
        Cdet = C11*C22-C12*C21
        a = .5*M2*L1*L2*sin(pend.theta1-pend.theta2)
        A = -(.5*M1+M2)*g*L1*sin(pend.theta1)-a*pend.theta2dot**2
        B = -.5*M2*g*L2*sin(pend.theta2)+a*pend.theta1dot**2
        pend.atheta1 = (C22*A-C12*B)/Cdet
        pend.atheta2 = (-C21*A+C11*B)/Cdet
        # Update velocities of the Lagrangian coordinates:
        pend.theta1dot += pend.atheta1*dt
        pend.theta2dot += pend.atheta2*dt
        # Update Lagrangian coordinates:
        dtheta1 = pend.theta1dot*dt
        dtheta2 = pend.theta2dot*dt
        pend.update(dtheta1, dtheta2)

    t += dt
    n += 1

    if energy_check and n >= 100:
        n = 0
        K = .5*((.25*M1+M2)*L1**2+I1)*pend1.theta1dot**2+.5*(.25*M2*L2**2+I2)*pend1.theta2dot**2+\
               .5*M2*L1*L2*cos(pend1.theta1-pend1.theta2)*pend1.theta1dot*pend1.theta2dot
        U = -(.5*M1+M2)*g*L1*cos(pend1.theta1)-.5*M2*g*L2*cos(pend1.theta2)
        gK.plot(pos=(t,K))
        gU.plot(pos=(t,U))
        gE.plot(pos=(t,K+U))
