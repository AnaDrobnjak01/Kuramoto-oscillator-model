import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.widgets as widgets

#ovo racuna vektor izvoda (tetaprim_1, ..., tetaprim_n)
def kuramoto(theta, K, omega):
    N = len(theta)
    dtheta_dt = np.zeros(N)
    for i in range(N):
        sum = 0
        for j in range(N):
            sum += np.sin(theta[j] - theta[i])
        dtheta_dt[i] = omega[i] + K/N*sum
    return dtheta_dt

N = 10 # broj oscilatora
timesteps = 1000 # vreme simulacije
h = 0.001 # korak
K = 100 # jacina uticaja medju oscilatorima

theta = np.random.uniform(0, 2*np.pi, N)
# omega = np.random.uniform(0.5, 2, N)
# omega_value = float(input("angle speed : "))
omega = np.repeat(5, N)

fig, ax = plt.subplots()
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.set_xlabel('X')
ax.set_ylabel('Y')
#prazna linija
oscillators, = ax.plot([], [], 'bo')

def init():
    oscillators.set_data([], [])
    return oscillators,

def update(frame):
    global theta
    t = frame*h
    k1 = h*kuramoto(theta, K, omega)
    k2 = h*kuramoto(theta + 0.5* k1, K, omega)
    k3 = h*kuramoto(theta + 0.5* k2, K, omega)
    k4 = h*kuramoto(theta + k3, K, omega)
    theta = theta + (1.0/6.0)*(k1 + 2*k2 + 2*k3 + k4)
    x = np.cos(theta)
    y = np.sin(theta)
    oscillators.set_data(x, y)
    return oscillators,

def resetSimulation(event):
    global theta
    theta = np.random.uniform(0, 2*np.pi, N)

def updateK(val):
    global K 
    K = sliderK.val 

def updateOmega(val):
    global omega
    omega[:] = np.repeat(sliderOmega.val, N)

def updateN(val):
    global N, theta, omega
    N = int(sliderN.val)
    theta = np.random.uniform(0, 2*np.pi, N)
    omega = np.repeat(sliderOmega.val, N)

ani = animation.FuncAnimation(fig, update, frames=int(timesteps/h), init_func=init, blit=True, interval=50)

#treba podesiti ovo da vizuelno izgleda pristojno sad samo dodajem da radi 
axes_reset = plt.axes([0.8, 0.025, 0.1, 0.04])
bt_reset_sim = widgets.Button(axes_reset, 'Reset simulation', color='yellow')
bt_reset_sim.on_clicked(resetSimulation)

axes_K = plt.axes([0.8, 0.15, 0.1, 0.02])
sliderK = widgets.Slider(axes_K, 'Strenght of coupling', 0.1, 100.0, valinit=K)
sliderK.on_changed(updateK)

axes_omega = plt.axes([0.8, 0.1, 0.1, 0.02])
sliderOmega = widgets.Slider(axes_omega, 'Angular speed', 0.1, 100.0, valinit=omega[0])
sliderOmega.on_changed(updateOmega)

axes_N = plt.axes([0.8, 0.2, 0.1, 0.02])
sliderN = widgets.Slider(axes_N, 'Number of oscillators', 1, 100, valinit=N, valstep=1)
sliderN.on_changed(updateN)

plt.show()