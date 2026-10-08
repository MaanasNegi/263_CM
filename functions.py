import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

def fmt(x):
    """Helper for formatting numbers nicely"""
    return f'{x:.3e}' if abs(x) < 0.001 or abs(x) >= 1000 else f'{x:.4g}'

def temperature_ode(t, T, S, T_deep, a, b):
    """ODE for bay water temperature: dT/dt = a*S(t) - b*(T - T_deep)."""
    dTdt = a * S(t) - b * (T - T_deep)
    return dTdt

def biomass_ode(t, B, g, T, mortality, heat_threshold, harvest, smolt_stocking):
    """ODE for stock biomass: dB/dt = g * T * B - mortality * max(T - T_c, 0) * B - h(t) * B + s(t)"""
    dBdt = g * T(t) * B - mortality * max(T(t) - heat_threshold, 0) * B - harvest(t) * B + smolt_stocking(t)
    return dBdt

def load_benchmark_data(filename):
    """Read benchmark_pen CSV and return (t, T, S_interp)"""
    data = np.genfromtxt(filename, delimiter=',', skip_header=1)

    t = data[:, 0]

    # convert MJ to J
    solar = 1e6 * data[:,1]
    T = data[:, 2]
    mass = data[:, 3]

    solar_interp = interp1d(t, solar, bounds_error=False, fill_value=(solar[0], solar[-1]))
    return t, T, solar_interp, mass

def load_sounds_data(filename):
    """Read salmon_sounds_data CSV and return (t, T, S_interp)"""
    data = np.genfromtxt(filename, delimiter=',', skip_header=1)

    t = data[:, 0]
    solar = 1e6 * data[:,2]
    T = data[:, 5] 

    # convert MJ to J
    data = np.array([t,solar, T])
    cleaned_data = data[:, ~np.isnan(data).any(axis=0)]

    solar_interp = interp1d(cleaned_data[0], cleaned_data[1], bounds_error=False, fill_value=(cleaned_data[1][0], cleaned_data[1][-1]))
    return cleaned_data[0], cleaned_data[2], solar_interp

def load_mass_data(filename):
    """Read salmon_sounds_data CSV and return (t, T, S_interp)"""
    data = np.genfromtxt(filename, delimiter=',', skip_header=1)

    t = data[:, 0]
    stocking = data[:, 3]
    harvest = data[:, 4]
    biomass = data[:, 6]

    # convert MJ to J
    data = np.array([t, stocking, harvest, biomass])
    cleaned_data = data[:, ~np.isnan(data).any(axis=0)]

    stocking_interp = interp1d(t, stocking, kind='previous', bounds_error=False, fill_value=(stocking[0], 0.0))
    harvest_interp  = interp1d(t, harvest,  kind='previous', bounds_error=False, fill_value=(harvest[0], harvest[-1]))

    return cleaned_data[0], stocking_interp, harvest_interp, cleaned_data[3]

def solve_temperature_ode(t, solar_interp, a, b, T_deep, T_0=22):
    """Solve the temperature ODE over array t and return the temperature solution."""

    sol = solve_ivp(temperature_ode, [t[0], t[-1]], [T_0], args=(solar_interp, T_deep, a, b), t_eval=t, method="RK45", rtol=1e-6, atol=1e-9)
    return sol.y[0]

def solve_biomass_ode(t, g, T, mortality, heat_threshold, harvest, smolt_stocking, B_0 = 4000):
    """Solve the temperature ODE over array t and return the temperature solution."""

    sol = solve_ivp(biomass_ode, [t[0], t[-1]], [B_0], args=(g, T, mortality, heat_threshold, harvest, smolt_stocking), t_eval=t, method="RK45", rtol=1e-6, atol=1e-9)
    return sol.y[0]

def plot_temp_callibration(a, b, T_deep, T_0=22):
    """Plot measured data with ODE model; optionally add a misfit contour map.

    Returns (fig, ax) normally, or (fig, (ax1, ax2)) when show_misfit_contour=True.
    """

    filename = 'salmon_sounds_data.csv'
    t_data, T_data, solar_interp = load_sounds_data(filename)
    t_model = np.arange(t_data[0], t_data[-1] + 1, 1)
    T_model = solve_temperature_ode(t_model, solar_interp, a, b, T_deep, T_0=T_0)

    fig, ax1 = plt.subplots(figsize=(6, 5))
    # Temperature fit
    ax1.scatter(t_data, T_data, label='Measured', zorder=3)
    label = f'Model (a={fmt(a)}, b={fmt(b)}, T_0={fmt(T_0)})'
    ax1.plot(t_model, T_model, label=label, color='tab:orange')
    ax1.set_xlabel('day')
    ax1.set_ylabel('Bay Temperature (°C)')
    ax1.set_title(f'Calibrated Temperature Model')
    ax1.legend()
    
    fig.tight_layout()
    plt.show()
    return fig, ax1

def plot_mass_callibration(T, growth, mortality, threshold, B_0=4000):
    """Plot measured data with ODE model; optionally add a misfit contour map.

    Returns (fig, ax) normally, or (fig, (ax1, ax2)) when show_misfit_contour=True.
    """

    filename = 'salmon_sounds_data.csv'
    t_data, stocking_interp, harvest_interp, biomass = load_mass_data(filename)
    
    t_model = np.arange(t_data[0], t_data[-1] + 1, 1)

    B_model = solve_biomass_ode(t_model, growth, T, mortality, threshold, harvest_interp, stocking_interp, B_0 = B_0)

    fig, ax1 = plt.subplots(figsize=(6, 5))

    # Biomass fit
    ax1.scatter(t_data, biomass, label='Measured', zorder=3)
    label = f'Model (growth={fmt(growth)}, mortality={fmt(mortality)})'

    ax1.plot(t_model, B_model, label=label, color='tab:orange')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Biomass (t)')
    ax1.set_title(f'Calibrated Time vs Mass model')
    ax1.legend()
    
    fig.tight_layout()
    plt.show()
    return fig, ax1 
