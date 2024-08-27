import sys
import os
import comtypes.client
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time


def connect_to_etabs():
    helper = comtypes.client.CreateObject('ETABSv1.Helper')
    helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
    try:
        myETABSObject = helper.GetObject("CSI.ETABS.API.ETABSObject")
        print("Connected to ETABS model")
    except (OSError, comtypes.COMError):
        print("No running instance of the program found or failed to attach.")
        sys.exit(-1)
    SapModel = myETABSObject.SapModel
    return SapModel, myETABSObject, helper


def envolvente_maxima(piso, nombre_viga, combinacion, plotear_envelope=False):
    SapModel, myETABSObject, helper = connect_to_etabs()
    start_time = time.time()

    ton_m_C = 12
    ret = SapModel.SetPresentUnits(ton_m_C)

    table = SapModel.DatabaseTables.GetTableForDisplayArray(
        "Element Forces - Beams", GroupName="")
    cols = table[2]
    noOfRows = table[3]
    vals = np.array_split(table[4], noOfRows)
    df = pd.DataFrame(vals)
    df.columns = cols

    # piso = ["NIVEL 5"]
    # nombre_viga = ["B16"]
    # combinacion = ["ENVOLVENTE"]
    max = ["Max"]
    min = ["Min"]
    df = df[df.Story.isin(piso)]
    df = df[df.Beam.isin(nombre_viga)]
    df = df[df.OutputCase.isin(combinacion)]

    df["M3"] = df["M3"].astype(float)
    df["Station"] = df["Station"].astype(float)

    df1 = df[df.StepType.isin(max)]
    df2 = df[df.StepType.isin(min)]

    df1 = df1.sort_values(by=['Station'])

    end_time = time.time()
    elapsed_time = end_time - start_time
    # print("Tiempo de ejecución: ", round(elapsed_time,2), "segundos")

    Mis = df1.iloc[0, 9]
    Mii = df2.iloc[0, 9]
    Mds = df1.iloc[-1, 9]
    Mdi = df2.iloc[-1, 9]
    # momentos = np.array([Mis, Mii, Mds, Mdi])
    # Mu = abs(np.max(momentos))

    L = df2["Station"].max()
    if plotear_envelope:
        plt.figure(figsize=(12, 5))
        plt.plot(df1["Station"].values, df1["M3"].values,
                 "b")        # plotear maximo
        plt.plot(df2["Station"].values, df2["M3"].values,
                 "b")        # plotear minimo
        # plotear eje de la viga
        plt.plot([0, L], [0, 0], "k", lw=2)
        plt.plot([0, 0], [Mis, Mii], "b")
        plt.plot([L, L], [Mds, Mdi], "b")
        plt.title("Diagrama de Momento Flector"+"\n" +
                  piso[0]+" "+nombre_viga[0]+" "+combinacion[0], fontsize=15, fontweight="bold")
        plt.xlabel("Distancia $m$")
        plt.ylabel("Momento $ton.m$")
        # anotaciones
        plt.annotate(str(round(Mis, 2))+" $ton.m$",
                     xy=(0, Mis), xytext=(0.05, 1.05*Mis))
        plt.annotate(str(round(Mds, 2))+" $ton.m$",
                     xy=(L, Mds), xytext=(0.85*L, Mds))
        plt.annotate(str(round(Mii, 2))+" $ton.m$",
                     xy=(0, Mii), xytext=(0.05, 1.05*Mii))
        plt.annotate(str(round(Mdi, 2))+" $ton.m$",
                     xy=(L, Mdi), xytext=(0.85*L, 1.05*Mdi))
        plt.gca().invert_yaxis()
        plt.grid(linestyle='-', linewidth=0.2)

        # achurar area de la grafica
        plt.fill_between(df1["Station"].values,
                         df1["M3"].values, 0, color="blue", alpha=0.4)
        plt.fill_between(df2["Station"].values,
                         df2["M3"].values, 0, color="blue", alpha=0.4)

        plt.savefig("M3.svg", dpi=1080, bbox_inches='tight')

        plt.show()
    else:
        pass
    return Mis, elapsed_time
