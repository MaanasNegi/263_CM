import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

def temperature_ode(t, T, S, T_deep, a, b):
    """ODE for bay water temperature: dT/dt = a*S(t) - b*(T - T_deep)."""
    dTdt = a * S(t) - b * (T - T_deep)
    return dTdt

def load_calibration_data(filename):

    """Read calibration CSV and return (t, T, S_interp)"""
    data = np.genfromtxt(filename, delimiter=',', skip_header=7)

    t = data[:, 0]
    voltage = data[:, 1]
    current = data[:, 2]
    T = data[:, 3]

    q = voltage * current
    q_interp = interp1d(t, q, bounds_error=False, fill_value=(q[0], q[-1]))

    return t, T, q_interp

def solve_temperature_ode(t, a, b, T_0=22):
    """Solve the kettle ODE over array t and return the temperature solution."""

    # Filename for calibration data CSV
    filename = ''

    _, _, q_interp = load_calibration_data(filename)

    sol = solve_ivp(temperature_ode, [t[0], t[-1]], [T_0], args=(q_interp, T_0, a, b), t_eval=t)
    return sol.y[0]
