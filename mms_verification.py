from functions import *

# parameter values don't matter
a = 1
b = 1
T_deep = 11
T_0 = 2

"""
replace ... with your derived solar radiation function 
"""
S = ...

t = np.linspace(0, 50, 501)

T_model = solve_temperature_ode(t, S, a, b, T_deep, T_0 = T_0)

"""
replace ... with your manufactured solution for T(t)
"""
T_analytical = ...

def plot_data():
    fig, ax = plt.subplots(1, 1, figsize=(9,6), sharex=True)

    ax.plot(t, T_model, color = "r", label = "Numerical Solution")
    ax.plot(t, T_analytical, "--" , color="b", label = "Analytical Solution")
    ax.set_xlabel("t")
    ax.set_ylabel("T")

    """
    replace ... with your manufactured solution for S(t)
    """

    plt.title("Analytical vs Numerical Solution when S(t) = ... using MMS")
    ax.legend()

    plt.tight_layout()
    plt.show()

plot_data()
