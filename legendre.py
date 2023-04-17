import numpy as np
from sympy import legendre
from sympy import Piecewise, symbols, lambdify, integrate
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import simpledialog
from tkinter import ttk
from functools import partial

def run_approximation(degree):
    x = symbols("x")
    f = Piecewise((0, (x > -1) & (x < 0)), (1, (x > 0) & (x < 1)))
    f_eval = lambdify(x, f)

    coefs = []

    for j in range(degree+1):
        
        C = (2*j + 1) / 2 * integrate(f * legendre(j, x), (x, -1, 1))
        
        coefs.append(C)

    S_n = coefs[0]*legendre(0, x)

    for j in range(1, degree+1):
        
        S_n += coefs[j]*legendre(j, x)

    S_n_eval = lambdify(x, S_n)

    t = np.linspace(-1.5, 1.5, 1000)

    error = float(integrate((f-S_n)**2, (x, -1, 1)))

    fig, ax = plt.subplots()
    fig.canvas.set_window_title(f'Մոտարկում N={degree} դեպքում')
    ax.axhline(y=0, color="black", alpha=0.5)
    ax.axvline(x=0, color="black", alpha=0.5)

    ax.plot(t, f_eval(t), color="red")
    y = S_n_eval(t)

    if isinstance(y, (int, float)):
        y = np.ones_like(t)*y

    ax.plot(t, y, ls="--", color="green")
    ax.set_title(f"Սխալ՝ {error:.4f}")
    ax.axis("equal")
    ax.set_xlim([-1, 1])
    ax.set_ylim([-0.5, 1.5])

    ax.legend(["Ֆունկցիա", "Ինտերպոլյացիա"])
    manager = plt.get_current_fig_manager()
    manager.resize(1600, 800)


    plt.show()

def run_approximation_gui():

    root = tk.Tk()
    root.title("Մոտարկում")
    root.attributes('-fullscreen',True)
    root.update()
    root.withdraw()

    top = tk.Toplevel(root)
    top.update()
    
    x = (root.winfo_width()) // 2  - top.winfo_width()
    y = (root.winfo_height()) // 2  - top.winfo_height()
    top.geometry("+{}+{}".format(x, y))
    top.update()
    

    top.withdraw()


    degree = simpledialog.askinteger("Մուտք","Մուտքագրեք մոտարկման աստիճանը․",
                                     parent=top,
                                     minvalue=0, 
                                     maxvalue=35,
                                     initialvalue=5,
                                     )
    run_approximation(degree)

    if not plt.get_fignums():
        exit()
 
    root.mainloop()

if __name__ == "__main__":
    run_approximation_gui()