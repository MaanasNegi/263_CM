from functions import *
from scipy.optimize import curve_fit

num = 100
threshold = 17.5

T_deep = 11 
t_data, T_data, solar_interp = load_sounds_data('salmon_sounds_data.csv')
_, stocking_interp, harvest_interp, biomass = load_mass_data('salmon_sounds_data.csv')

a = 1.3496401472122314e-08
b = 0.03634018916919134

g = 0.000379747938239228
m = 0.0031317842843983223
B_0 = 4037.9198683702884

cov1 = [[1.22156366e-18, 3.27050975e-12],
 [3.27050975e-12, 9.06857193e-06]]

cov2 = [[ 9.02438923e-12, 3.45010575e-10, -2.16073070e-05], 
 [ 3.45010575e-10,  1.42782342e-08, -1.91727536e-04],
 [-2.16073070e-05, -1.91727536e-04,  5.87005026e+02]]

T_0 = T_data[0]
B_0_scenario = B_0

fig, ax1 = plt.subplots(figsize=(6, 5))
ax1.scatter(t_data, T_data, label='Measured', zorder=3)

for i in range(num):
    sample = np.random.multivariate_normal([a,b], cov1)
    T_sample = solve_temperature_ode(t_data, solar_interp, sample[0], sample[1], T_deep, T_0)
    
    if i < num - 1:
        ax1.plot(t_data, T_sample, linewidth = 0.5, alpha = 0.2, color="orange")
    else:
        ax1.plot(t_data, T_sample, linewidth = 0.5, alpha = 0.2, label = "Sample", color="orange")

ax1.legend()
plt.show()

T_model = solve_temperature_ode(t_data, solar_interp, a, b, T_deep, T_0 = T_0)
T = interp1d(t_data, T_model)

fig, ax1 = plt.subplots(figsize=(6, 5))

for i in range(num):
    sample = np.random.multivariate_normal([g, m, B_0], cov2)
    #B_sample = solve_biomass_ode(t_data, sample[0], T, sample[1], threshold, harvest_interp, stocking_interp, B_0 = sample[2])
    B_sample = solve_biomass_ode(t_data, sample[0], T, sample[1], threshold, harvest_interp, stocking_interp, B_0 = B_0_scenario)

    if i < num - 1:
        ax1.plot(t_data, B_sample, linewidth = 0.5, alpha = 0.2, color="orange")
    else:
        ax1.plot(t_data, B_sample, linewidth = 0.5, alpha = 0.2, label = "Sample", color="orange")

ax1.legend()
plt.show()
