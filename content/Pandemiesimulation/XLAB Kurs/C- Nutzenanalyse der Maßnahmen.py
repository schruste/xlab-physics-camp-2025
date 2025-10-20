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
          params["gamma"], ', E:', params["E"], ', reduce:', reduce,
          ', nlockdown:', nlockdown, ', vaccrate:', params["vaccrate"],
          ', nvacc:', params["nvacc"])




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

    # Ergebnis für die Kontrollmaßnahme
    Sm, Im, Rm, T= f(E, vaccrate, args)
    

    # Bestimmung des Maximums der gleichzeitig infizierten
    print('')
    itmax= T[np.argmax(I)]
    imax= I.max()
    print('Das maximale I ohne Eingriff tritt nach', itmax, 'Tagen ein und entspricht', imax)


    # Plotten des Nutzens: Die Differenz aus ohne Eingriff und mich Eingriff verdeutlicht den Unterschied
    fig = plt.figure(facecolor='w')   
    ax = fig.add_subplot(111, axisbelow=True)
    ax.plot( T, I, 'yellow',  alpha=0.8, lw=2, label='i(t) ohne Eingriff')
    ax.plot( T, Im, 'red',  alpha=0.5, lw=2, label='i(t) mit Eingriff')
    ax.plot( T, I-Im, 'blue',  alpha=0.5, lw=2, label='zeitabh. Abweichung')
    
    ax.grid()                                    
    ax.set_xlabel("Zeit t [Tagen]",  fontsize=10)
    ax.set_ylabel("Anteil d. Individuen", fontsize=10)
    plt.title("Nutzenanalyse der Kontrollstrategie", fontsize=10)
    axes = plt.gca()
    ax.legend(loc='best')

    plt.show(block=False)

    # Nutzen wird nun identifiziert über die Differenz der Gesamtanteile aller Infizierten
    g = np.sum(I)       #alternativ np.trapz(I, dx=1) 
    G = np.sum(Im)      #alternativ np.trapz(Im, dx=1)
    gi = np.sum(I-Im)   #alternativ np.trapz(I-Im, dx=1)
    print('Die Gesamtanteil aller Infizierter ohne Eingriff beträgt:', g*gamma,
          '. Das entspricht etwa', int(g*gamma*N), 'Menschen aus der Bevölkerung')
    print('Die Gesamtanteil aller Infizierter mit Eingriff beträgt:', G*gamma,
          '. Das entspricht etwa', int(G*gamma*N), 'Menschen aus der Bevölkerung')
    print('So infizieren sich etwa', int(gi*gamma*N), ' weniger Menschen aus der',
          'Bevölkerung als ohne Eingriff.')
    print('Damit ist diese Strategie um:', round((1-G/g)*100, 3), '% besser.')      
    print('')


'''

GUI Code: Ei

'''

# Ein Fenster erstellen
fenster = Tk()

# Den Fenstertitle erstellen
fenster.title("SIR Modell- Nutzenanalyse der Kontrollmaßnahmen")

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











