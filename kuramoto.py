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
K = 7 # jacina uticaja medju oscilatorima

theta = np.random.uniform(0, 2*np.pi, N)
# omega = np.random.uniform(0.5, 2, N)
# omega_value = float(input("angle speed : "))
omega = np.repeat(5, N)

fig, (ax_anim, ax_controls) = plt.subplots(1, 2, figsize=(12, 6), gridspec_kw={'width_ratios': [2, 1]})
fig_manager = plt.get_current_fig_manager()
fig_manager.set_window_title('Kuramoto Oscillator Model')  # Set window title



ax_anim.set_xlim(-1.2, 1.2)
ax_anim.set_ylim(-1.2, 1.2)
ax_anim.set_xlabel("cosθ")
ax_anim.set_ylabel("sinθ")
#ax_anim.axis('off')
oscillators, = ax_anim.plot([], [], 'bo')

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

def resetParameters(event):
    global N, K, omega, theta
    N = 10 
    K = 7 
    omega = np.repeat(5, N)
    theta = np.random.uniform(0, 2*np.pi, N)
    sliderK.set_val(K) 
    sliderN.set_val(N)
    sliderOmega.set_val(5)

ani_running = True
def pauseSimulation(event):
    global ani_running
    if ani_running:
        ani.event_source.stop()
        buttonPause.label.set_text('Resume animation')
    else:
        ani.event_source.start()
        buttonPause.label.set_text('Pause animation')
    ani_running = not ani_running

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


sliderN_ax = plt.axes([0.7, 0.8, 0.15, 0.03])
sliderN = widgets.Slider(sliderN_ax, 'Number of oscillators', 1, 100, valinit=N, valstep=1)
sliderN.on_changed(updateN)


sliderK_ax = plt.axes([0.7, 0.7, 0.15, 0.03])
sliderK = widgets.Slider(sliderK_ax, 'Strength of coupling', 0.1, 100.0, valinit=K)
sliderK.on_changed(updateK)


sliderOmega_ax = plt.axes([0.7, 0.6, 0.15, 0.03])
sliderOmega = widgets.Slider(sliderOmega_ax, 'Angular speed', 0.1, 100.0, valinit=omega[0])
sliderOmega.on_changed(updateOmega)


buttonReset_ax = plt.axes([0.7, 0.4, 0.15, 0.1])
buttonReset = widgets.Button(buttonReset_ax, 'Reset simulation', color='yellow')
buttonReset.on_clicked(resetSimulation)

buttonPause_ax = plt.axes([0.7, 0.2, 0.15, 0.1])
buttonPause = widgets.Button(buttonPause_ax, 'Pause animation', color='red')
buttonPause.on_clicked(pauseSimulation)

buttonResetParams_ax = plt.axes([0.7, 0.0, 0.15, 0.1])
buttonResetParams = widgets.Button(buttonResetParams_ax, "Reset parameters", color='blue')
buttonResetParams.on_clicked(resetParameters)

ax_controls.axis('off')


#check ???
oscilators = init()
ani = animation.FuncAnimation(fig, update, frames=int(timesteps/h), init_func=init, blit=True, interval=50)

plt.show()