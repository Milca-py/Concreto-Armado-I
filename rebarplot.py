import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D


def plot_varillac(p1, p2, diameter, ax, color='blue'):
    # Vector del cilindro
    vector = np.array(p2) - np.array(p1)
    length = np.linalg.norm(vector)

    # Normalizamos el vector
    vector_normalized = vector / length

    # Ángulo para rotar
    angle = np.arccos(vector_normalized[2])
    axis = np.cross([0, 0, 1], vector_normalized)
    axis_length = np.linalg.norm(axis)
    if axis_length > 0:
        axis = axis / axis_length
        rotation_matrix = np.array([
            [np.cos(angle) + axis[0]**2 * (1 - np.cos(angle)),
             axis[0] * axis[1] * (1 - np.cos(angle)) - axis[2] * np.sin(angle),
             axis[0] * axis[2] * (1 - np.cos(angle)) + axis[1] * np.sin(angle)],
            [axis[1] * axis[0] * (1 - np.cos(angle)) + axis[2] * np.sin(angle),
             np.cos(angle) + axis[1]**2 * (1 - np.cos(angle)),
             axis[1] * axis[2] * (1 - np.cos(angle)) - axis[0] * np.sin(angle)],
            [axis[2] * axis[0] * (1 - np.cos(angle)) - axis[1] * np.sin(angle),
             axis[2] * axis[1] * (1 - np.cos(angle)) + axis[0] * np.sin(angle),
             np.cos(angle) + axis[2]**2 * (1 - np.cos(angle))]
        ])
    else:
        rotation_matrix = np.eye(3)

    # Crear los puntos del cilindro
    theta = np.linspace(0, 2 * np.pi, 30)
    z = np.linspace(0, length, 30)
    theta, z = np.meshgrid(theta, z)
    x = (diameter / 2) * np.cos(theta)
    y = (diameter / 2) * np.sin(theta)

    # Aplicar la rotación
    points = np.vstack([x.ravel(), y.ravel(), z.ravel()])
    rotated_points = np.dot(rotation_matrix, points).reshape((3, *x.shape))

    # Trasladar el cilindro
    rotated_points[0, :, :] += p1[0]
    rotated_points[1, :, :] += p1[1]
    rotated_points[2, :, :] += p1[2]

    # Graficar
    ax.plot_surface(rotated_points[0], rotated_points[1],
                    rotated_points[2], color=color)


# # Parámetros del cilindro
# p1 = (0.0, 0, 0)
# p2 = (0.7, 0, 0)
# dc = 0.1   # diámetro del cilindro

# # Crear la figura
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# # Graficar el cilindro
# plot_varilla(p1, p2, dc, ax, color='blue')

# # Ajustar límites
# ax.set_xlim([min(p1[0], p2[0]) - dc, max(p1[0], p2[0]) + dc])
# ax.set_ylim([min(p1[1], p2[1]) - dc, max(p1[1], p2[1]) + dc])
# ax.set_zlim([min(p1[2], p2[2]) - dc, max(p1[2], p2[2]) + dc])

# plt.show()


def plot_varillal(p1, p2, diameter, ax, color='blue'):
    # Coordenadas de los puntos
    x = [p1[0], p2[0]]
    y = [p1[1], p2[1]]
    z = [p1[2], p2[2]]
    # Dibujar la línea
    ax.plot(x, y, z, color=color, linewidth=diameter*100)

# # Crear una figura y un eje 3D
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# b = 1         # base
# L = 1           # Luz de la viga
# h = 1         # peralte
# r = 0.55        # recubrimiento
# p1 = (r, 0, r)
# p2 = (r, L, r)
# dc = 0.2
# ax.set_xlim([0, b])
# ax.set_ylim([0, L])
# ax.set_zlim([0, h])
# ax.set_box_aspect([b, L, h])

# plot_varillal(p1, p2, dc / 2, ax, color='blue')

# plt.show()


# linewidth = 300 = 1 div


def plot_estribol(p1, p2, p3, p4, diameter, ax, color='blue'):
    # Coordenadas de los puntos
    points = [p1, p2, p3, p4, p1]  # Cerrar el polígono volviendo a p1

    # Dibujar las líneas entre los puntos
    for i in range(len(points) - 1):
        x = [points[i][0], points[i+1][0]]
        y = [points[i][1], points[i+1][1]]
        z = [points[i][2], points[i+1][2]]
        ax.plot(x, y, z, color=color, linewidth=diameter*100)


# # Ejemplo de uso
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# p1 = (0, 0, 0)
# p2 = (1, 0, 0)
# p3 = (1, 1, 0)
# p4 = (0, 1, 0)
# diameter = 0.05

# plot_estribol(p1, p2, p3, p4, diameter, ax, color='blue')

# # Configurar límites y etiquetas
# ax.set_xlim([0, 1])
# ax.set_ylim([0, 1])
# ax.set_zlim([0, 1])
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')

# # Mostrar la gráfica
# plt.show()

# 3


def plot_estriboc(p1, p2, p3, p4, diameter, ax, color='blue'):
    plot_varillac(p1, p2, diameter, ax, color)
    plot_varillac(p2, p3, diameter, ax, color)
    plot_varillac(p3, p4, diameter, ax, color)
    plot_varillac(p1, p4, diameter, ax, color)


# # Ejemplo de uso
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# # Puntos del polígono
# p1 = (0, 0, 0)
# p2 = (1, 0, 0)
# p3 = (1, 1, 0)
# p4 = (0, 1, 0)
# diameter = 0.05

# # Plotear el estribo
# plot_estriboc(p1, p2, p3, p4, diameter, ax, color='blue')

# # Configurar límites y etiquetas
# ax.set_xlim([0, 1.5])
# ax.set_ylim([0, 1.5])
# ax.set_zlim([0, 1.5])
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')

# # Mostrar la gráfica
# plt.show()


def plot_rebarl(points, diameter, ax, color='blue'):
    # Iterar sobre la lista de puntos y dibujar líneas entre cada par consecutivo
    for i in range(len(points) - 1):
        p1 = points[i]
        p2 = points[i + 1]

        # Coordenadas de los puntos
        x = [p1[0], p2[0]]
        y = [p1[1], p2[1]]
        z = [p1[2], p2[2]]

        # Dibujar la línea
        ax.plot(x, y, z, color=color, linewidth=diameter * 100)


# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# # Lista de puntos
# points = [(0, 0, 0), (1, 1, 1), (2, 0, 2), (3, 1, 3)]

# # Llamar a la función con la lista de puntos
# plot_varillal(points, diameter=0.1, ax=ax, color='red')

# plt.show()


def plot_rebarc(points, diameter, ax, color="red"):
    for i in range(len(points)-1):
        plot_varillac(points[i], points[i+1],  diameter, ax, color=color)


# # Ejemplo de uso
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# # Lista de puntos
# points = [(0, 0, 0), (1, 1, 1), (2, 0, 2), (3, 1, 3), (3, 4, 5)]

# # Llamar a la función con la lista de puntos

# plot_rebarc(points, 0.05, ax, color='red')
# plt.show()


# def plot_rebarr(p1, p2, p3, p4, diameter, ax, color='blue'):
#     plot_varillac(p2, p1, diameter, ax, color)
#     plot_varillac(p2, p3, diameter, ax, color)
#     plot_varillac(p3, p4, diameter, ax, color)


def plot_rebarr(p1, p2, p3, p4, diameter, ax, color='blue'):
    plot_varillac(p2, p1, diameter, ax, color)
    plot_varillac(p2, p3, diameter, ax, color)
    plot_varillac(p3, p4, diameter, ax, color)
