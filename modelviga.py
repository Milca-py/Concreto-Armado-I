import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import rebarplot as vp


def modelar_viga(b, L, h, rr, dc, nc, dt, nt, de, ei, e1, n1, e2, n2, e3, rebarExtrude=False):
    """Modela una viga de concreto reforzado con varillas longitudinales y estribos.
    todos los de distancia deben ingresarse en metros.

    Args:
        b (float):  (m) :   base de la seccion de la viga
        L (float):  (m) :   luz de la viga
        h (float):  (m) :   peralte de la viga
        rr (float): (m) :   recubrimiento (espesor del concreto no confinado) constructivo
        dc (float): (m) :   diámetro de las varillas en compresion
        nc (int):   (num) : numero de varillas longitudinales en compresión
        dt (float): (m) :   diámetro de las varillas en tracción
        nt (int):   (num) : numero de varillas longitudinales en tracción
        de (float): (m) :   diámetro de los estribos
        ei (float): (m) :   espaciamiento inicial (generalmente 5cm)
        e1 (float): (m) :   primer espaciamiento de los estribos
        n1 (int):   (num) : número de estribos con espaciamiento e1
        e2 (float): (m) :   segundo espaciamiento de los estribos
        n2 (int):   (num) : número de estribos con espaciamiento e2
        e3 (float): (m) :   tercer espaciamiento de los estribos (resto)
        rebarExtrude (bool, optional): True para extruir las varillas. Defaults to False.
    """
    n3 = (L/2 - ei - (n1 - 1)*e1 - n2*e2) / e3

    # recubrimientos (esta para metrizado en funcio a rr, pero si se necesita tener otros valores cambiar
    # la formula por valores numericos)
    # recubrimiento del acero a tracción (hasta el eje de la varilla) r
    r = dt/2 + de + rr
    # recubrimiento del acero a compresión (hasta el eje de la varilla) d'
    dd = dc/2 + de + rr
    # recubrimiento lateral (hasta la cara interior del estribo)
    rl = de + rr

    # varillas a flexion
    varillas_t = []
    for i in range(1, nt+1):
        e = (b - 2 * (rl + dt/2)) / (nt - 1)
        pi = (rl + dt/2 + (i - 1) * e, 0, r)
        pf = (rl + dt/2 + (i - 1) * e, L, r)
        varillas_t.append([pi, pf])

    # varillas a compresion
    varillas_c = []
    for i in range(1, nc+1):
        e = (b - 2 * (rl + dc/2)) / (nc - 1)
        pi = (rl + dc/2 + (i - 1) * e, 0, h-dd)
        pf = (rl + dc/2 + (i - 1) * e, L, h-dd)
        varillas_c.append([pi, pf])

    # estribos
    # a L/2
    # estribos tramo1
    estribost1 = []
    for i in range(1, int(n1)+1):
        y1 = ei + (i - 1)*e1
        yf = L - y1
        p1 = (rr + de/2,        y1, rr + de/2)
        p2 = (b - rr - de/2,    y1, rr + de/2)
        p3 = (b - rr - de/2,    y1, h - rr - de/2)
        p4 = (rr + de/2,        y1, h - rr - de/2)
        estribost1.append([p1, p2, p3, p4])
        p1 = (rr + de/2,        yf, rr + de/2)
        p2 = (b - rr - de/2,    yf, rr + de/2)
        p3 = (b - rr - de/2,    yf, h - rr - de/2)
        p4 = (rr + de/2,        yf, h - rr - de/2)
        estribost1.append([p1, p2, p3, p4])

    # estribos tramo2
    estribost2 = []
    for i in range(1, int(n2)+1):
        y1 = ei + (n1 - 1)*e1
        y2 = y1 + i*e2
        yf = L - y2
        p1 = (rr + de/2,        y2, rr + de/2)
        p2 = (b - rr - de/2,    y2, rr + de/2)
        p3 = (b - rr - de/2,    y2, h - rr - de/2)
        p4 = (rr + de/2,        y2, h - rr - de/2)
        estribost2.append([p1, p2, p3, p4])
        p1 = (rr + de/2,        yf, rr + de/2)
        p2 = (b - rr - de/2,    yf, rr + de/2)
        p3 = (b - rr - de/2,    yf, h - rr - de/2)
        p4 = (rr + de/2,        yf, h - rr - de/2)
        estribost2.append([p1, p2, p3, p4])

    # estribos tramo3
    estribost3 = []
    for i in range(1, int(n3)+1):
        y1 = ei + (n1 - 1)*e1
        y2 = y1 + n2*e2
        y3 = y2 + i*e3
        yf = L - y3
        p1 = (rr + de/2,        y3, rr + de/2)
        p2 = (b - rr - de/2,    y3, rr + de/2)
        p3 = (b - rr - de/2,    y3, h - rr - de/2)
        p4 = (rr + de/2,        y3, h - rr - de/2)
        estribost3.append([p1, p2, p3, p4])
        p1 = (rr + de/2,        yf, rr + de/2)
        p2 = (b - rr - de/2,    yf, rr + de/2)
        p3 = (b - rr - de/2,    yf, h - rr - de/2)
        p4 = (rr + de/2,        yf, h - rr - de/2)
        estribost3.append([p1, p2, p3, p4])

    # Vértices de la viga
    vertices = np.array([
        [0, 0, 0],  # p1
        [b, 0, 0],  # p2
        [b, L, 0],  # p3
        [0, L, 0],  # p4
        [0, 0, h],  # p5
        [b, 0, h],  # p6
        [b, L, h],  # p7
        [0, L, h]   # p8
    ])

    # Define las caras de la viga
    caras = [
        [vertices[0], vertices[1], vertices[5], vertices[4]],  # cara inferior
        [vertices[7], vertices[6], vertices[2], vertices[3]],  # cara superior
        [vertices[0], vertices[3], vertices[7], vertices[4]],  # cara frontal
        [vertices[1], vertices[2], vertices[6], vertices[5]],  # cara trasera
        [vertices[0], vertices[1], vertices[2], vertices[3]],  # cara inferior
        [vertices[4], vertices[5], vertices[6], vertices[7]]   # cara superior
    ]

    # Ploteo de la viga
    fig = plt.figure(figsize=(8, 8))  # tamaño en pulgadas
    ax = fig.add_subplot(111, projection='3d')

    if rebarExtrude:
        # dibujar las varillas longitudinales
        for pi, pf in varillas_t:
            vp.plot_varillac(pi, pf, dt, ax, color='red')
            # vp.plot_varillal(pi, pf, 5*dt/L, ax, color='red')

        for pi, pf in varillas_c:
            vp.plot_varillac(pi, pf, dc, ax, color='blue')
            # vp.plot_varillal(pi, pf, 5*dc/L, ax, color='blue')

        # dibujar los estribos
        # tramo 1
        for p1, p2, p3, p4 in estribost1:
            vp.plot_estriboc(p1, p2, p3, p4, de, ax, color='blue')
            # vp.plot_estribol(p1, p2, p3, p4, 5*de/L, ax, color='blue')
        # tramo 2
        for p1, p2, p3, p4 in estribost2:
            vp.plot_estriboc(p1, p2, p3, p4, de, ax, color='red')
            # vp.plot_estribol(p1, p2, p3, p4, 5*de/L, ax, color='red')
        # tramo 3
        for p1, p2, p3, p4 in estribost3:
            vp.plot_estriboc(p1, p2, p3, p4, de, ax, color='green')
            # vp.plot_estribol(p1, p2, p3, p4, 5*de/L, ax, color='green')
    else:
        # dibujar las varillas longitudinales
        for pi, pf in varillas_t:
            vp.plot_varillal(pi, pf, 5*dt/L, ax, color='red')

        for pi, pf in varillas_c:
            vp.plot_varillal(pi, pf, 5*dc/L, ax, color='blue')

        # dibujar los estribos
        # tramo 1
        for p1, p2, p3, p4 in estribost1:
            vp.plot_estribol(p1, p2, p3, p4, 5*de/L, ax, color='blue')
        # tramo 2
        for p1, p2, p3, p4 in estribost2:
            vp.plot_estribol(p1, p2, p3, p4, 5*de/L, ax, color='red')
        # tramo 3
        for p1, p2, p3, p4 in estribost3:
            vp.plot_estribol(p1, p2, p3, p4, 5*de/L, ax, color='green')

    # Añadir las caras de la viga
    poly3d = Poly3DCollection(caras, alpha=0.2, linewidths=1,
                              edgecolors='black', facecolors='#e1ddd6')
    ax.add_collection3d(poly3d)

    # Configurar límites y etiquetas
    ax.set_xlim([0, b+0.1])
    ax.set_ylim([0, L+0.05])
    ax.set_zlim([0, h+0.1])
    ax.set_xlabel('Base (m)', fontweight='bold', fontsize=7)
    ax.set_ylabel('Luz (m)', fontweight='bold', fontsize=7, labelpad=70)
    ax.set_zlabel('Peralte (m)', fontweight='bold', fontsize=7)

    # Configurar los ticks de los ejes
    ax.set_xticks(np.arange(0, b + 0.1, 0.1))
    ax.set_yticks(np.arange(0, L + 0.5, 0.5))
    ax.set_zticks(np.arange(0, h + 0.1, 0.1))

    # Formato de las etiquetas de los ejes
    ax.tick_params(axis='both', which='major', labelsize=6)

    # Configurar la escala igual para todos los ejes
    # Relación de aspecto [ancho, alto, profundidad]
    ax.set_box_aspect([b, L, h])

    ax.set_facecolor((1, 1, 1, 0.1))
    # ax.set_facecolor('#282c34')

    # Mostrar la gráfica
    plt.show()

    # for i in range(len(estribost2)):
    #     list = [round(y, 2) for y in estribost2[i]]
    #     print(f"estribos2: {i+1} : {list}")

    # for i in range(len(estribost1)):
    #     for j in range(len(estribost1[i])):
    #         estribost1[i][j] = [round(y, 2) for y in estribost1[i][j]]
    #     print(f"estribo1 {i+1} : {estribost1[i]}")

    # for i in range(len(estribost2)):
    #     for j in range(len(estribost2[i])):
    #         estribost2[i][j] = [round(y, 2) for y in estribost2[i][j]]
    #     print(f"estribo2 {i+1} : {estribost2[i]}")

    # for i in range(len(estribost3)):
    #     for j in range(len(estribost3[i])):
    #         estribost3[i][j] = [round(y, 2) for y in estribost3[i][j]]
    #     print(f"estribo3 {i+1} : {estribost3[i]}")


# # Parámetros de la geometria de la zapata
# b = 0.3         # base
# L = 7           # Luz de la viga
# h = 0.6         # peralte
# rr = 0.06       # recubrimiento (espesor del concreto no confinado)


# # varillas longitudinales (acero por flexión)
# dc = 0.0199      # diámetro de las varillas en compresion
# nc = 2          # numero de varillas longitudinales en compresión
# dt = 0.0254      # diámetro de las varillas en tracción
# nt = 3          # numero de varillas longitudinales en tracción

# # estribos
# de = 0.02      # diámetro de los estribos
# ei = 0.05       # espaciamiento inicial
# e1 = 0.05       # primer espaciamiento de los estribos (generalmente 5cm)
# n1 = 1.00       # número de estribos con espaciamiento e1
# e2 = 0.10       # segundo espaciamiento de los estribos
# n2 = 4.00       # número de estribos con espaciamiento e2
# e3 = 0.25       # tercer espaciamiento de los estribos (resto)

# modelar_viga(b, L, h, rr, dc, nc, dt, nt, de, ei,
#              e1, n1, e2, n2, e3, rebarExtrude=False)


# print(modelar_viga.__doc__)


# def dibujar_plano(b, L, h, rr, dc, nc, dt, nt, de, ei, e1, n1, e2, n2, e3, rebarExtrude=False):
#     n3 = (L/2 - ei - (n1 - 1)*e1 - n2*e2) / e3

#     # recubrimientos (esta para metrizado en funcio a rr, pero si se necesita tener otros valores cambiar
#     # la formula por valores numericos)
#     # recubrimiento del acero a tracción (hasta el eje de la varilla) r
#     r = dt/2 + de + rr
#     # recubrimiento del acero a compresión (hasta el eje de la varilla) d'
#     dd = dc/2 + de + rr
#     # recubrimiento lateral (hasta la cara interior del estribo)
#     rl = de + rr
#     ###########################################################
#     # puntos de la geometria
#     V = 0.75
#     H = 0.25
#     pc1 = (-H*h, -V*h)
#     pc2 = (0, -V*h)
#     pc3 = (0, 0)
#     pc4 = (L, 0)
#     pc5 = (L, -V*h)
#     pc6 = (L+H*h, -V*h)
#     pc7 = (L+H*h, (1+V)*h)
#     pc8 = (L, (1+V)*h)
#     pc9 = (L, h)
#     pc10 = (0, h)
#     pc11 = (0, (1+V)*h)
#     pc12 = (-H*h, (1+V)*h)

#     ###########################################################

#     # varillas a flexion
#     varillas_t = []
#     for i in range(1, nt+1):
#         e = (b - 2 * (rl + dt/2)) / (nt - 1)
#         pi = (rl + dt/2 + (i - 1) * e, 0, r)
#         pf = (rl + dt/2 + (i - 1) * e, L, r)
#         varillas_t.append([pi, pf])

#     # varillas a compresion
#     varillas_c = []
#     for i in range(1, nc+1):
#         e = (b - 2 * (rl + dc/2)) / (nc - 1)
#         pi = (rl + dc/2 + (i - 1) * e, 0, h-dd)
#         pf = (rl + dc/2 + (i - 1) * e, L, h-dd)
#         varillas_c.append([pi, pf])

#     # estribos
#     # a L/2
#     # estribos tramo1
#     estribost1 = []
#     for i in range(1, int(n1)+1):
#         y1 = ei + (i - 1)*e1
#         yf = L - y1
#         p1 = (rr + de/2,        y1, rr + de/2)
#         p2 = (b - rr - de/2,    y1, rr + de/2)
#         p3 = (b - rr - de/2,    y1, h - rr - de/2)
#         p4 = (rr + de/2,        y1, h - rr - de/2)
#         estribost1.append([p1, p2, p3, p4])
#         p1 = (rr + de/2,        yf, rr + de/2)
#         p2 = (b - rr - de/2,    yf, rr + de/2)
#         p3 = (b - rr - de/2,    yf, h - rr - de/2)
#         p4 = (rr + de/2,        yf, h - rr - de/2)
#         estribost1.append([p1, p2, p3, p4])

#     # estribos tramo2
#     estribost2 = []
#     for i in range(1, int(n2)+1):
#         y1 = ei + (n1 - 1)*e1
#         y2 = y1 + i*e2
#         yf = L - y2
#         p1 = (rr + de/2,        y2, rr + de/2)
#         p2 = (b - rr - de/2,    y2, rr + de/2)
#         p3 = (b - rr - de/2,    y2, h - rr - de/2)
#         p4 = (rr + de/2,        y2, h - rr - de/2)
#         estribost2.append([p1, p2, p3, p4])
#         p1 = (rr + de/2,        yf, rr + de/2)
#         p2 = (b - rr - de/2,    yf, rr + de/2)
#         p3 = (b - rr - de/2,    yf, h - rr - de/2)
#         p4 = (rr + de/2,        yf, h - rr - de/2)
#         estribost2.append([p1, p2, p3, p4])

#     # estribos tramo3
#     estribost3 = []
#     for i in range(1, int(n3)+1):
#         y1 = ei + (n1 - 1)*e1
#         y2 = y1 + n2*e2
#         y3 = y2 + i*e3
#         yf = L - y3
#         p1 = (rr + de/2,        y3, rr + de/2)
#         p2 = (b - rr - de/2,    y3, rr + de/2)
#         p3 = (b - rr - de/2,    y3, h - rr - de/2)
#         p4 = (rr + de/2,        y3, h - rr - de/2)
#         estribost3.append([p1, p2, p3, p4])
#         p1 = (rr + de/2,        yf, rr + de/2)
#         p2 = (b - rr - de/2,    yf, rr + de/2)
#         p3 = (b - rr - de/2,    yf, h - rr - de/2)
#         p4 = (rr + de/2,        yf, h - rr - de/2)
#         estribost3.append([p1, p2, p3, p4])

#     # Vértices de la viga
#     vertices = np.array([
#         [0, 0, 0],  # p1
#         [b, 0, 0],  # p2
#         [b, L, 0],  # p3
#         [0, L, 0],  # p4
#         [0, 0, h],  # p5
#         [b, 0, h],  # p6
#         [b, L, h],  # p7
#         [0, L, h]   # p8
#     ])

#     # Define las caras de la viga
#     caras = [
#         [vertices[0], vertices[1], vertices[5], vertices[4]],  # cara inferior
#         [vertices[7], vertices[6], vertices[2], vertices[3]],  # cara superior
#         [vertices[0], vertices[3], vertices[7], vertices[4]],  # cara frontal
#         [vertices[1], vertices[2], vertices[6], vertices[5]],  # cara trasera
#         [vertices[0], vertices[1], vertices[2], vertices[3]],  # cara inferior
#         [vertices[4], vertices[5], vertices[6], vertices[7]]   # cara superior
#     ]

#     # Ploteo de la viga
#     fig = plt.figure(figsize=(8, 8))  # tamaño en pulgadas
#     ax = fig.add_subplot(111, projection='3d')

#     if rebarExtrude:
#         # dibujar las varillas longitudinales
#         for pi, pf in varillas_t:
#             vp.plot_varillac(pi, pf, dt, ax, color='red')
#             # vp.plot_varillal(pi, pf, 5*dt/L, ax, color='red')

#         for pi, pf in varillas_c:
#             vp.plot_varillac(pi, pf, dc, ax, color='blue')
#             # vp.plot_varillal(pi, pf, 5*dc/L, ax, color='blue')

#         # dibujar los estribos
#         # tramo 1
#         for p1, p2, p3, p4 in estribost1:
#             vp.plot_estriboc(p1, p2, p3, p4, de, ax, color='blue')
#             # vp.plot_estribol(p1, p2, p3, p4, 5*de/L, ax, color='blue')
#         # tramo 2
#         for p1, p2, p3, p4 in estribost2:
#             vp.plot_estriboc(p1, p2, p3, p4, de, ax, color='red')
#             # vp.plot_estribol(p1, p2, p3, p4, 5*de/L, ax, color='red')
#         # tramo 3
#         for p1, p2, p3, p4 in estribost3:
#             vp.plot_estriboc(p1, p2, p3, p4, de, ax, color='green')
#             # vp.plot_estribol(p1, p2, p3, p4, 5*de/L, ax, color='green')
#     else:
#         # dibujar las varillas longitudinales
#         for pi, pf in varillas_t:
#             vp.plot_varillal(pi, pf, 5*dt/L, ax, color='red')

#         for pi, pf in varillas_c:
#             vp.plot_varillal(pi, pf, 5*dc/L, ax, color='blue')

#         # dibujar los estribos
#         # tramo 1
#         for p1, p2, p3, p4 in estribost1:
#             vp.plot_estribol(p1, p2, p3, p4, 5*de/L, ax, color='blue')
#         # tramo 2
#         for p1, p2, p3, p4 in estribost2:
#             vp.plot_estribol(p1, p2, p3, p4, 5*de/L, ax, color='red')
#         # tramo 3
#         for p1, p2, p3, p4 in estribost3:
#             vp.plot_estribol(p1, p2, p3, p4, 5*de/L, ax, color='green')

#     # Añadir las caras de la viga
#     poly3d = Poly3DCollection(caras, alpha=0.2, linewidths=1,
#                               edgecolors='black', facecolors='#e1ddd6')
#     ax.add_collection3d(poly3d)

#     # Configurar límites y etiquetas
#     ax.set_xlim([0, b+0.1])
#     ax.set_ylim([0, L+0.05])
#     ax.set_zlim([0, h+0.1])
#     ax.set_xlabel('Base (m)', fontweight='bold', fontsize=7)
#     ax.set_ylabel('Luz (m)', fontweight='bold', fontsize=7, labelpad=70)
#     ax.set_zlabel('Peralte (m)', fontweight='bold', fontsize=7)

#     # Configurar los ticks de los ejes
#     ax.set_xticks(np.arange(0, b + 0.1, 0.1))
#     ax.set_yticks(np.arange(0, L + 0.5, 0.5))
#     ax.set_zticks(np.arange(0, h + 0.1, 0.1))

#     # Formato de las etiquetas de los ejes
#     ax.tick_params(axis='both', which='major', labelsize=6)

#     # Configurar la escala igual para todos los ejes
#     # Relación de aspecto [ancho, alto, profundidad]
#     ax.set_box_aspect([b, 0.5*L, h])

#     ax.set_facecolor((1, 1, 1, 0.1))
#     # ax.set_facecolor('#282c34')

#     # Mostrar la gráfica
#     plt.show()

#     # for i in range(len(estribost2)):
#     #     list = [round(y, 2) for y in estribost2[i]]
#     #     print(f"estribos2: {i+1} : {list}")

#     # for i in range(len(estribost1)):
#     #     for j in range(len(estribost1[i])):
#     #         estribost1[i][j] = [round(y, 2) for y in estribost1[i][j]]
#     #     print(f"estribo1 {i+1} : {estribost1[i]}")

#     # for i in range(len(estribost2)):
#     #     for j in range(len(estribost2[i])):
#     #         estribost2[i][j] = [round(y, 2) for y in estribost2[i][j]]
#     #     print(f"estribo2 {i+1} : {estribost2[i]}")

#     # for i in range(len(estribost3)):
#     #     for j in range(len(estribost3[i])):
#     #         estribost3[i][j] = [round(y, 2) for y in estribost3[i][j]]
#     #     print(f"estribo3 {i+1} : {estribost3[i]}")


# # Parámetros de la geometria de la zapata
# b = 0.3         # base
# L = 7           # Luz de la viga
# h = 0.6         # peralte
# rr = 0.06       # recubrimiento (espesor del concreto no confinado)


# # varillas longitudinales (acero por flexión)
# dc = 0.0199      # diámetro de las varillas en compresion
# nc = 2          # numero de varillas longitudinales en compresión
# dt = 0.0254      # diámetro de las varillas en tracción
# nt = 3          # numero de varillas longitudinales en tracción

# # estribos
# de = 0.02      # diámetro de los estribos
# ei = 0.05       # espaciamiento inicial
# e1 = 0.05       # primer espaciamiento de los estribos (generalmente 5cm)
# n1 = 1.00       # número de estribos con espaciamiento e1
# e2 = 0.10       # segundo espaciamiento de los estribos
# n2 = 4.00       # número de estribos con espaciamiento e2
# e3 = 0.25       # tercer espaciamiento de los estribos (resto)

# modelar_viga(b, L, h, rr, dc, nc, dt, nt, de, ei,
#              e1, n1, e2, n2, e3, rebarExtrude=False)


# print(modelar_viga.__doc__)
