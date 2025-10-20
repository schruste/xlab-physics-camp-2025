# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 16:58:38 2021

@author: viola
"""
# Pakete, die für die Programmausführung notwendig sind
from scipy.integrate import odeint, cumtrapz
import numpy as np
import matplotlib.pyplot as plt
import math
from mpl_toolkits import mplot3d
from sympy import linsolve, symbols, solve, expand, simplify
from tkinter import *



#Funktion beim Anklicken des Buttons
def button_action():
    plt.close('all')
    anweisungs_label.config(text="Vorher Parameterfile ausfüllen & speichern")

    # Einlesen und Konvertieren des Parameterfiles
    fileName = "Parameterfile.txt"
    fileObj = open(fileName)
    params = {}
    for line in fileObj:
        line = line.strip()
        if not line.startswith("#"):
            key_value =line.split("=")
            if len(key_value) == 2:
                params[key_value[0].strip()] = key_value[1].strip()
        

    params["n"]= int(params["n"])
    params["S"]= int(params["S"])
    params["I"]= int(params["I"])
    params["N"]= int(params["N"])
    params["beta"]= float(params["beta"])
    params["gamma"]= float(params["gamma"])
    params["E"]= float(params["E"])
    params["reduce"]= float(params["reduce"])
    params["nlockdown"]= int(params["nlockdown"])
    params["nvacc"]= int(params["nvacc"])
    params["vaccrate"]= float(params["vaccrate"])
    
    n = int(params["n"])
    s0= int(params["S"])
    i0= int(params["I"])
    N= int(params["N"])
    beta = float(params["beta"])
    gamma= float(params["gamma"])
    E= float(params["E"])
    reduce = float(params["reduce"])
    nlockdown= int(params["nlockdown"])
    nvacc= int(params["nvacc"])
    vaccrate= float(params["vaccrate"])

    r0= N-s0-i0

    print('N:', N, ',S:', params["S"], ', I:', params["I"],
          ', R:', r0, ', beta:', params["beta"], ', gamma:',
          params["gamma"], ', E:', params["E"], ', vaccrate:', params["vaccrate"],
          ', nvacc:', params["nvacc"])

    
        
    # Gitter mit je p Werten für die Intensität und Zeit des Hygiene-Eingriffs
    n=5000
    p=40
    Reduce = np.linspace(0,0.99,p) 
    Nlockdown= np.linspace(0,80,p, dtype=int)
    (X,Y) = np.meshgrid(Nlockdown, Reduce)
    totalI=[]
    
    # Bestimmung des Gesamtanteils der Infizierten für jede Kombination (Reduce, Nlockdown)
    for reduce in Reduce:
        for nlockdown in Nlockdown:

            S=np.zeros(n)
            I=np.zeros(n) 
            R=np.zeros(n) 
            T=np.zeros(n)
            s=s0
            i=i0
            r=r0

            vaccon=0    
            betaold= beta
            nlockdownend= nlockdown + E/(betaold-reduce*betaold)
            #nlockdownend= int(nlockdownend)
            
            for j in np.arange(0,n):
                # Starte den Lockdown/Hygiene ab 
                if j > nlockdown and j < nlockdownend:
                    beta= reduce*betaold
                # Start der Impfung ab, endet nie
                if j > nvacc:
                    vaccon=1
                # Ende der Hygienemaßnahme erreicht,
                #    Änderung der Infektionsrate zum alten Wert
                if j > nlockdownend:  
                    beta= betaold
                # Start der Euler Iteration
                s=s-beta*i*s/N -vaccon*vaccrate*s 
                i=i+(beta*i*s/N-gamma*i)
                r= N-s-i     # alternativ  r+(gamma*i)+vaccon*vaccrate*s
                S[j]=s/N     # Umrechnung der Anzahlen in Anteile zur Zeit j
                I[j]=i/N
                R[j]=r/N
                T[j]=j

            intI=np.sum(I)*gamma      
            totalI.append(intI)
    

    totalInp=np.array(totalI) 
    totalInpgrid=totalInp.reshape((p,p))


    # Plotten der Gesamtanteile in Abhängigkeit des Absenkungsfaktors UND Startzeitpkt   
    fig = plt.figure(figsize=[8, 5])
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(Y, X,totalInpgrid,cmap='rainbow', rstride=1, cstride=1,linewidth=1 )
    ax.set_xlabel('Absenkungsfaktor reduce', fontsize=10)
    ax.set_ylabel('Eingriffsbeginn nlockdown', fontsize=10)
    ax.set_zlabel('Anteil aller Infizierten (summiert)', fontsize=10)
    plt.title("Auswirkung der verschiedenen Kombination von Absenkungsfaktor und \n"
              "Zeitpunkt auf den Gesamtinfiziertenanteil", fontsize= 10)  #Titel

    for angle in range(0, 180):  # Option zum eigenständigen drehen des Plots
        ax.view_init(30, angle)
        plt.draw()
        plt.pause(.001)

    plt.show(block=False)


    # Ausgabe des Minimums
    minI=min(totalI)   # Bestimmung des minimalen Gesamtanteils aller Infizierten
    Indexmin=totalI.index(min(totalI))  # Bestimmung des Indexes dieses Wertes, um dazugehörige Parameter zu finden

    ReduceminIndex=int((Indexmin-(Indexmin % len(Reduce)))/len(Reduce)) # Bestimmung des reduce-Parameter 
    NlockdownminIndex=Indexmin % len(Nlockdown)      # Bestimmung des nlockdown-Parameter

    Reducemin= Reduce[ReduceminIndex]
    Nlockdownmin= Nlockdown[NlockdownminIndex]
    
    print('Das Minimum der Fläche und damit die ideale Hygiene-Strategie ist bei einer Absenkung auf',
          Reducemin, 'ab dem Tag', Nlockdownmin)
    print('Dann werden sich insgesamt:', round(minI*100,2), '% der Population infizieren.')
    
    
    # Abweichung von der idealen Maßnahme
    #   für die Absenkung
    plt.figure(figsize=[6, 4])  #figsize=[breite, höhe des bildes]
    plt.grid() #Gitter im Plot
    plt.xlabel("Eingriffszeitpunkt nlockdown", fontsize=10) #x-Achsen Beschriftung
    plt.ylabel("Anteil aller Infizierten (summiert)", fontsize=10) #y Beschriftung
    plt.title("Auswirkung beim Abweichen vom idealen Absenkfaktor", fontsize= 10)  #Titel
     
    Reducelist=Reduce.tolist()
    for var in [-4,-2,0,2,4]:
        X=Nlockdown
        k=int(ReduceminIndex+var)
        if k>=0:
            Y=totalInpgrid[k]
            plt.plot(X,Y,label='reduce={}'.format(round(Reducelist[k], 4)))
             
    axes = plt.gca()
    plt.legend(fontsize='x-small')
    plt.show(block=False)             


    # Abweichung von der idealen Maßnahme
    #   in der Startzeit
    plt.figure(figsize=[6, 4])  #figsize=[breite, höhe des bildes]
    plt.subplots_adjust(right=0.75)
    plt.grid() #Gitter im Plot
    plt.xlabel("Absenkungsfaktor reduce", fontsize=10) #x-Achsen Beschriftung
    plt.ylabel("Anteil aller Infizierten (summiert)", fontsize=10) #y Beschriftung
    plt.title("Auswirkung beim Abweichen vom idealen Eingriffzeitpunkt", fontsize= 10)  #Titel
             
    Lockdownlist=Nlockdown.tolist()
    for var in [-4,-2,-1,0,1,2,4]:
        X=Reduce.tolist()
        Y=[]
        k=int(NlockdownminIndex+var)
        if k >= 0:
            for x in X:
                Y.append(totalInpgrid[X.index(x)][k])
            plt.plot(X,Y,label='nlockdown={}'.format(round(Lockdownlist[k], 2)))
             
    axes = plt.gca()
    plt.legend(fontsize='x-small')
    #plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='x-small')
    plt.show(block=False)
    
    
    
     
'''

GUI Code: Ei

'''

# Ein Fenster erstellen
fenster = Tk()

# Den Fenstertitle erstellen
fenster.title("SIR Modell- ideale Hygienemaßnahme")

# Label und Buttons erstellen.
change_button = Button(fenster, text="Nächster Plot", command=button_action)
exit_button = Button(fenster, text="Beenden", command=fenster.quit)

anweisungs_label = Label(fenster, text="Vorher Parameterfile ausfüllen & speichern")
info_label = Label(fenster, text="Das Programm beenden.")


# Nun fügen wir die Komponenten unserem Fenster in der gewünschten Reihenfolge hinzu.

anweisungs_label.pack()
change_button.pack()
info_label.pack()
exit_button.pack()

# In der Ereignisschleife auf Eingabe des Benutzers warten.

fenster.mainloop()











