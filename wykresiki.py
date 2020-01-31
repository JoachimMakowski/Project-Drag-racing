import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

slope = 0.4
meta = 402
# animate plots?
animate=True # True / False

# define model
def vehicle(v,t,u,load):
    # inputs
    #  v    = vehicle velocity (m/s)
    #  t    = time (sec)
    #  u    = gas pedal position (-50% to 100%)
    #  load = passenger load + cargo (kg)
    Cd = 0.24    # drag coefficient
    rho = 1.225  # air density (kg/m^3)
    A = 5.0      # cross-sectional area (m^2)
    Fp = 5000      # siła ciągu samochodu
    m = 500      # vehicle mass (kg)
    # calculate derivative of the velocity
    dv_dt = (Fp - 0.5*rho*Cd*A*v**2-(m+load)*10*slope)/(m+load)
    return dv_dt

tf = 60.0                 # final time for simulation
delta_t = 0.1   # how long is each time step?
nsteps = int(tf/delta_t+1)
print(nsteps)
ts = np.linspace(0,tf,nsteps) # linearly spaced time vector

# simulate step test operation
# passenger(s) + cargo load
load = 200.0 # kg
# velocity initial condition
v01 = 0.0
v02 = 0.0
# set point
#sp = 25.0
# for storing the results
vs1 = np.zeros(nsteps)
vs2 = np.zeros(nsteps)
#sps = np.zeros(nsteps)
dst1 = np.zeros(nsteps)
dst2 = np.zeros(nsteps)

plt.figure(1,figsize=(5,4))
if animate:
    plt.ion()
    plt.show()

i=0
u=0
# simulate with ODEINT
while True:
    if dst1[i]<meta and dst2[i]<meta:
        v1 = odeint(vehicle,v01,[0,delta_t],args=(u,load))
        v2 = odeint(vehicle,v02,[0,delta_t],args=(u,300))
        if v1[-1]<0:
            v1[-1]=0
        if v2[-1]<0:
            v2[-1]=0
        if v1[-1]==0 and v2[-1]==0:
            print("Oba samochody się zatrzymały")
            break
        v01 = v1[-1]   # take the last value
        v02 = v2[-1]
        vs1[i+1] = v01 # store the velocity for plotting
        vs2[i+1] = v02
        #sps[i+1] = sp
        dst1[i+1] = dst1[i]+v01*delta_t
        dst2[i+1] = dst2[i]+v02*delta_t

        # plot results
        #if animate:
        plt.clf()       #clf=wyczyść wszystko
        plt.subplot(2,1,1)
        plt.plot(ts[0:i+1],vs1[0:i+1],'b-',linewidth=3)
        plt.plot(ts[0:i+1],vs2[0:i+1],'k--',linewidth=2)
        plt.ylabel('Velocity (m/s)')
        plt.legend(['Velocity1','Velocity2'],loc=2)
        plt.subplot(2,1,2)
        plt.plot(ts[0:i+1],dst1[0:i+1],'b--',linewidth=3)
        plt.plot(ts[0:i+1],dst2[0:i+1],'k--',linewidth=3)
        plt.ylabel('Distance (m)')
        plt.legend(['Distance1','Distance2'],loc=2)
        plt.pause(0.01)
    else:
        if dst1[i]>dst2[i]:
            print("Wygrał 1szy")
            print(dst1[i],vs1[i],i)
        else:
            print("Wygrał drugi")
        break
    i+=1

if not animate:
    # plot results
    plt.subplot(2,1,1)
    plt.plot(ts,vs1,'b-',linewidth=3)
    plt.plot(ts,vs2,'k--',linewidth=2)
    plt.ylabel('Velocity (m/s)')
    plt.legend(['Velocity1','Velocity2'],loc=2)
    plt.subplot(2,1,2)
    plt.plot(ts,dst1,'b--',linewidth=3)
    plt.plot(ts,dst2,'k--',linewidth=3)
    plt.ylabel('Distance (m)')
    plt.legend(['Distance1','Distance2'],loc=2)
    plt.show()