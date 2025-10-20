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
from tkinter import *



#Funktion beim Anklicken des Buttons
def button_action():
    plt.close('all')
    anweisungs_label.config(text="Parameterfile ausfüllen & speichern")

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
            if key_value[0] == "gamma":
                break

    params["n"]= int(params["n"])
    params["S"]= int(params["S"])
    params["I"]= int(params["I"])
    params["N"]= int(params["N"])
    params["beta"]= float(params["beta"])
    params["gamma"]= float(params["gamma"])

    n = int(params["n"])
    s= int(params["S"])
    i= int(params["I"])
    N= int(params["N"])
    beta = float(params["beta"])
    gamma= float(params["gamma"])

    r= N-s-i

    # Ausgabe der verwendeten Parameter
    print('n:', n, ', N:', N, ', S:', params["S"], ', I:', params["I"],
          ', R:', r, ', beta:', params["beta"], ', gamma:',
          params["gamma"])


    # Listen für die Ergebnissicherung
    S=np.zeros(n)
    I=np.zeros(n) 
    R=np.zeros(n) 
    T=np.zeros(n) 
    

    # Bestimmung des zeitlichen Verlaufs, über die Euler Iteration
    for j in np.arange(0,n):        
        s=s-beta*i*s/N 
        i=i+(beta*i*s/N-gamma*i)
        r= N-s-i    #alternativ  r=r+(gamma*i)
        S[j]=s/N    #Umrechnung der Anzahlen in Anteile zur Zeit j
        I[j]=i/N
        R[j]=r/N
        T[j]=j
    
    # Plotten der Anteile
    plt.figure(figsize=[6, 4])      #figsize=[Breite, Höhe des Bildes]
    plt.plot(T, S, label="s(t)")    #plot(x-Achse, y-Achse, Beschriftung)
    plt.plot(T, I, label="i(t)")
    plt.plot(T, R, label= "r(t)")
    plt.grid()                      #Gitter im Plot
    plt.legend()                    #Legende im Plot
    plt.xlabel("Zeit t [Tagen]", fontsize=10) #x-Achsen Beschriftung
    plt.ylabel("Anteil d. Individuen", fontsize=10) #y-Achsen Beschriftung
    plt.title(r"SIR- Modell: zeitliche Entwicklung einer unkontrollierte Epidemie", fontsize= 10) #Titel
    axes = plt.gca()
    axes.set_ylim([-0.05,1.05]) 
    

    plt.show(block=False)

    
    # Berechnung des Maximus der Infizierten
    itmax= T[np.argmax(I)]
    imax= I.max()
    print('Das maximale I der Epidemie tritt am', itmax, 'Tag ein und entspricht', imax)


    # Berechnung einer 7-Tages Inzidenz
    incidence= np.convolve(I, np.ones(7)/7, mode='same')
    incidence= N/100000*incidence 
    plt.figure(figsize=[6.5, 4])
    plt.plot(T, incidence, label= "7-Tage-Inzidenz")
    plt.grid() 
    plt.legend()
    plt.xlabel("Zeit t [Tagen]", fontsize=10) 
    plt.ylabel("Zahl der Neuinfizierten in einer Woche \n pro 100.000 Einwohner", fontsize=10) #y-Achsen Beschriftung
    plt.title("Inzidenzzahl Entwicklung bei einer unkontrollierten Epidemie" , fontsize= 10)  #Titel




    # Berechnung der Gesamtzahl der Infizierten bis zur Zeit T
    gi =cumtrapz(I, dx=1, initial=0 )
    
    # Plotten des Gesamtanteils aller jemals Infizierten
    #   (Multiplikation mit Gamma, um mehrfach Zählung zu verhindern) 
    plt.figure(figsize=[6, 4])   
    plt.plot(T,gi*gamma,label=r'$\nu_i$ (T)')

    axes = plt.gca()
    plt.grid() 
    plt.legend()
    plt.xlabel("Zeit T [Tagen]", fontsize=10) 
    plt.ylabel("Anteil aller Infizierten (summiert)", fontsize=10)
    plt.title("Entwicklung des Anteils der jemals Erkrankten \n in einer unkontrollierten Epidemie", fontsize=10)
    

    plt.show(block=False)
    
    print('Bis zum Tag', n, 'haben sich insgesamt', gi[-1]*gamma, '(umrechnen in Prozent!) Individuenen mit der Infektion angesteckt.')



    

'''

GUI Code: Ei

'''

# Ein Fenster erstellen
fenster = Tk()

# Den Fenstertitle erstellen
fenster.title("SIR Modell- unkontrollierte Epidemie")

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











