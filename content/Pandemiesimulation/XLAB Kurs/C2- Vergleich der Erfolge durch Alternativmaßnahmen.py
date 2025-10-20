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


# Funktion beim Anklicken des Buttons
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
    params["reduce"]= float(params["reduce"])
    params["nlockdown"]= int(params["nlockdown"])
    params["E"]= float(params["E"])
    params["nvacc"]= int(params["nvacc"])
    params["vaccrate"]= float(params["vaccrate"])

    n = int(params["n"])
    s= int(params["S"])
    i= int(params["I"])
    N= int(params["N"])
    beta = float(params["beta"])
    gamma= float(params["gamma"])
    reduce = float(params["reduce"])
    nlockdown= int(params["nlockdown"])
    E= float(params["E"])
    nvacc= int(params["nvacc"])
    vaccrate= float(params["vaccrate"])

    r= N-s-i

    # Ausgabe der verwendeten Parameter
    print('n:', n, ', N:', N, ', S:', params["S"], ', I:', params["I"],
          ', R:', r, ', beta:', params["beta"], ', gamma:',
          params["gamma"], ', nlockdown:', nlockdown)

    

    #Definition der Euler Iteration in Abhängigkeit der Parameter
    def f(E, vaccrate, args):
        n, s, i, r, N, beta, gamma, reduce, nlockdown, nvacc = args
        
        S=np.zeros(n)
        I=np.zeros(n) 
        R=np.zeros(n) 
        T=np.zeros(n)
    
        vaccon=0    
        betaold= beta
        nlockdownend= nlockdown + E/(betaold-reduce*betaold)
        nlockdownend= int(nlockdownend)
    
        for j in np.arange(0,n):
            # Starte den Lockdown/Hygiene ab 
            if j > nlockdown and j < nlockdownend: 
                beta= reduce*betaold
            # Start der Impfung, endet aber nie
            if j > nvacc:
                vaccon=1
            # Ende der Hygienemaßnahme erreicht,
            #    Änderung der Infektionsrate zum alten Wert    
            if j > nlockdownend:  
                beta= betaold
            # Start der Euler-Iteration 
            s=s-beta*i*s/N -vaccon*vaccrate*s 
            i=i+(beta*i*s/N-gamma*i)
            r= N-s-i     # alternativ  r=r+(gamma*i)+vaccon*vaccrate*s
            S[j]=s/N     # Umrechnung der Anzahlen in Anteile zur Zeit j
            I[j]=i/N
            R[j]=r/N
            T[j]=j
      
        return(S,I,R,T)
    
    args=  n, s, i, r, N, beta, gamma, reduce, nlockdown, nvacc

    # Ergebnis für die unkontrollierte Epidemie
    #   (keine Ressource= kein Einsatz, keine Impfrate= kein Impfen)
    S,I,R,T= f(0, 0, args)
        
    # Gesamtanteil der Erkrankten für unkontrollierte Epidemie
    g = np.sum(I)       #alternativ np.trapz(I, dx=1)


    # Prozentualer Erfolg für verschiedene Hygienemaßnahmen (+Plot)
    RESSOURCE = [1, 2, 3, 5, 7, 10, 20, 50, 60, 80, 200]
    REDUCE = np.linspace(0,0.99,10)
    GI_E = []

    fig = plt.figure(facecolor='w')   
    ax = fig.add_subplot(111, axisbelow=True)
    ax.grid()                                    
    ax.set_xlabel("reduce ",  fontsize=10)
    ax.set_ylabel("Erfolg in Prozent", fontsize=10)
    plt.title("Erfolg von verschiedene Hygienemaßnahmen für nlockdown={}".format(nlockdown), fontsize=10)

    for E in RESSOURCE:
        GI_reduce = []
        for reduce in REDUCE:
            args= [n, s, i, r, N, beta, gamma, reduce, nlockdown, nvacc]
            Sr,Ir,Rr,T= f(E, 0, args)
            gi_r = np.sum(I-Ir)/g*100
            GI_reduce.append(gi_r)
        GI_E.append(GI_reduce)
        ax.plot(REDUCE, GI_reduce, alpha=0.8, lw=2, label='E={}'.format(E))    


    axes = plt.gca()
    ax.legend(loc='best')
    plt.show(block=False)
  

    # Prozentualer Erfolg für verschiedene Impfkampagnen (+Plot)
    VACCRATE = [0.001, 0.003, 0.005, 0.007 ,0.01, 0.015, 0.02, 0.05, 0.1, 0.25, 0.5, 0.75]
    NVACC = np.linspace(0,100,100)
    GI_VACCRATE = []

    fig = plt.figure(facecolor='w')   
    ax = fig.add_subplot(111, axisbelow=True)
    ax.grid()                                    
    ax.set_xlabel("nvacc [Tagen]",  fontsize=10)
    ax.set_ylabel("Erfolg in Prozent", fontsize=10)
    plt.title("Erfolg von verschiedenen Impfkampagnen", fontsize=10)


    for vaccrate in VACCRATE:
        GI_NVACC = []
        for nvacc in NVACC:
            args= [n, s, i, r, N, beta, gamma, reduce, nlockdown, nvacc]
            Si,Ii,Ri,T= f(0, vaccrate, args)
            gi_v = np.sum(I-Ii)/g*100
            GI_NVACC.append(gi_v)
        GI_VACCRATE.append(GI_NVACC)
        ax.plot(NVACC, GI_NVACC, alpha=0.8, lw=2, label='vaccrate={}'.format(vaccrate))    

    axes = plt.gca()
    ax.legend(loc='best')
    plt.show(block=False)


    
'''

GUI Code: Ei

'''

# Ein Fenster erstellen
fenster = Tk()

# Den Fenstertitle erstellen
fenster.title("SIR Modell- Erfolg verschiedener Alternativmaßnahmen")

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











