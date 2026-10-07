
from functions import *

# callibrated temperature values
a = 1.3591743433705313e-08
b = 0.03660952646482794
T_0 = 17.212442761350136
T_deep = 11
T_constant = 15

# random parameters 
g = 0.1
mortality = 0
heat_threshold = 15
B_0 = 1

t, T_data, solar_interp = load_sounds_data("salmon_sounds_data.csv")

zero_forcing_func = lambda t: 0

T = lambda t: T_constant

B_model = solve_biomass_ode(t, g, T, mortality, heat_threshold, zero_forcing_func, zero_forcing_func, B_0 = B_0)

"""
replace ... with your solved function for the zero forced ODE where s(t) = 0, h(t) = 0 and mortality = 0, and T(t) is a constant
"""
B_analytical = ...

def mms():
    """
    replace ... with s(t) which comes from rearranging dB/dt
    """
    stocking_func = lambda t: ...

    B_model = solve_biomass_ode(t, g, T, mortality, heat_threshold, zero_forcing_func, stocking_func, B_0 = B_0)

    B_analytical = ...

def plot_data():
    fig, ax = plt.subplots(1, 1, figsize=(9,6), sharex=True)

    ax.plot(t, B_model, color = "r", label = "Numerical Solution")
    ax.plot(t, B_analytical, "--" , color="b", label = "Analytical Solution")
    ax.set_xlabel("t")
    ax.set_ylabel("B")
    plt.title("Analytical vs Numerical Solution for Mass ODE when mortality, h(t) and s(t) = 0, T(t) = 15")
    ax.legend()

    plt.tight_layout()
    plt.show()

#mms()
plot_data()
