from milca import vigas as vt
# b = 50
# h = 20
# r = 4
# fc = 350
# fy = 4200
# Mu = 1
# vig = vt.VigaR(Mu, b, h, r, fc, fy)
# print(f"Asmin = {vig.Asmin()}")
# print(f"Area de acero = {vig.As()}")
# print(f"Asmax = {vig.Asmax()}")
# vig.plot()


# DATOS
from math import sqrt
Vumax = 17.27    # ton
Øcorte = 0.85
b = 0.30    # m
h = 0.70    # m
r = 0.06    # m
fc = 210    # kg/cm2
fy = 4200   # kg/cm2
de = 0.0095  # m
n = 2       # nuemero de ramas
L = 3.5     # m
SE = "Dual2"    # *Dual1, Dual2*tipo de sistema estructural
dt = 0.0159  # m

zona_es_sismica = True

tramos = vt.calcular_estribos(Vumax, b, h, r, L, fc, fy, de, dt, n, SE)
print(f"xd : {tramos}")
