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

def load_benchmark_data(filename):
    """Read calibration CSV and return (t, T, S_interp)"""
    data = np.genfromtxt(filename, delimiter=',', skip_header=1)

    t = data[:, 0]
    solar = 1e6 * data[:,1]
    T = data[:, 2]

    solar_interp = interp1d(t, solar, bounds_error=False, fill_value=(solar[0], solar[-1]))
    return t, T, solar_interp

def solve_temperature_ode(t, solar_interp, a, b, T_deep, T_0=20):
    """Solve the temperature ODE over array t and return the temperature solution."""

    # Filename for calibration data CSV
    sol = solve_ivp(temperature_ode, [t[0], t[-1]], [T_0], args=(solar_interp, T_deep, a, b), t_eval=t)
    return sol.y[0]

def plot_calibration(a, b, T_deep, T_0=20, show_misfit_contour=True):
    """Plot measured data with ODE model; optionally add a misfit contour map.

    Returns (fig, ax) normally, or (fig, (ax1, ax2)) when show_misfit_contour=True.
    """

    filename = 'benchmark_pen.csv'
    t_data, T_data, solar_interp = load_benchmark_data(filename)

    def misfit_at(ai, bi):
        sol = solve_ivp(temperature_ode, [t_data[0], t_data[-1]], [T_0], args=(solar_interp, T_deep, ai, bi), t_eval=t_data)

        return np.linalg.norm(sol.y[0] - T_data)**2

    t_model = np.arange(t_data[0], t_data[-1] + 1, 1)
    T_model = solve_temperature_ode(t_model, solar_interp, a, b, T_deep, T_0=T_0)
    misfit = misfit_at(a, b)

    if show_misfit_contour:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    else:
        fig, ax1 = plt.subplots(figsize=(6, 5))

    # Temperature fit
    ax1.scatter(t_data, T_data, label='Measured', zorder=3)
    label = f'Model (a={fmt(a)}, b={fmt(b)})'
    if abs(T_0 - 20) >= 1e-4:
        label += f', T0={fmt(T_0)}'
    ax1.plot(t_model, T_model, label=label, color='tab:orange')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Temperature (°C)')
    ax1.set_title(rf'$\Psi$ = {fmt(misfit)}')
    ax1.legend()

    if show_misfit_contour:
        # Build log-spaced grid ±1 order of magnitude around (a, b)
        n = 100
        a_vals = np.logspace(np.log10(a) - 1, np.log10(a) + 1, n)
        b_vals = np.logspace(np.log10(b) - 1, np.log10(b) + 1, n)
        A, B = np.meshgrid(a_vals, b_vals)
        PSI = np.vectorize(misfit_at)(A, B)

        log_PSI = np.log10(PSI)
        cf = ax2.contourf(A, B, log_PSI, levels=20, cmap='viridis')
        ax2.contour(A, B, log_PSI, levels=20, colors='k', linewidths=0.4, alpha=0.4)
        fig.colorbar(cf, ax=ax2, label=r'$\log_{10}(\Psi)$')
        ax2.plot(a, b, 'rx', markersize=6, zorder=5, label=f'({fmt(a)}, {fmt(b)})')
        ax2.set_xscale('log')
        ax2.set_yscale('log')
        ax2.set_xlabel('a')
        ax2.set_ylabel('b')
        ax2.set_title('Misfit landscape')
        ax2.legend()

        fig.tight_layout()
        return fig, (ax1, ax2)

    plt.show()
    fig.tight_layout()
    return fig, ax1
