import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#ovo racuna vektor izvoda (tetaprim_1, ..., tetaprim_n)
def kuramoto(theta, K, omega):
  N = len(theta)
  dtheta_dt = np.zeros(N)
  for i in range (N):
    sum = 0
    for j in range (N):
      sum += np.sin(theta[j] - theta[i])
    dtheta_dt[i] = omega[i] + K/N * sum
  return dtheta_dt

print("Input parameters for differential equation : ")
N = int(input("number of oscillators : "))
timesteps = int(input("simulation time : ")) # vreme simulacije
h = float(input("timestep : "))
K = float(input("strenght of coupling : ")) # jacina uticaja medju oscilatorima

theta = np.random.uniform(0, 2 * np.pi, N)
# omega = np.random.uniform(0.5, 2, N)
omega_value = float(input("angle speed : "))
omega = np.repeat(omega_value, N)

fig, ax = plt.subplots()
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.set_xlabel('X')
ax.set_ylabel('Y')
#prazna linija
oscillators, = ax.plot([], [], lw=2)

def init():
    oscillators.set_data([], [])
    return oscillators,

#rk4 metod
def update(frame):
    global theta
    t = frame * h
    k1 = h * kuramoto(theta, K, omega)
    k2 = h * kuramoto(theta + 0.5 * k1, K, omega)
    k3 = h * kuramoto(theta + 0.5 * k2, K, omega)
    k4 = h * kuramoto(theta + k3, K, omega) #k1,k2,k3,k4 ce biti vektori dimenzije n
    theta = theta + (1.0/6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
    x = np.cos(theta)
    y = np.sin(theta)
    oscillators.set_data(x, y)
    return oscillators,

oscillators, = ax.plot([], [], 'bo')

ani = animation.FuncAnimation(fig, update, frames=int(timesteps/h), init_func=init, blit=True, interval=50)
plt.show()

