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
    params["S"]= float(params["S"])
    params["I"]= float(params["I"])
    params["N"]= float(params["N"])
    params["beta"]= float(params["beta"])
    params["gamma"]= float(params["gamma"])
    params["reduce"]= float(params["reduce"])
    params["nlockdown"]= float(params["nlockdown"])
    params["E"]= float(params["E"])
    params["nvacc"]= float(params["nvacc"])
    params["vaccrate"]= float(params["vaccrate"])

    n = int(params["n"])
    s= float(params["S"])
    i= float(params["I"])
    N= float(params["N"])
    beta = float(params["beta"])
    gamma= float(params["gamma"])
    reduce = float(params["reduce"])
    nlockdown= float(params["nlockdown"])
    E= float(params["E"])
    nvacc= float(params["nvacc"])
    vaccrate= float(params["vaccrate"])
    
    r=N-s-i

    # Ausgabe der verwendeten Parameter
    print('n:', n, ', N:', N, ', S:', params["S"], ', I:', params["I"],
          ', R:', r, ', beta:', params["beta"], ', gamma:',
          params["gamma"], ', E:', params["E"], ', reduce:', reduce,
          ', nlockdown:', nlockdown, ', vaccrate:', params["vaccrate"],
          ', nvacc:', params["nvacc"])


    # Listen für die Ergebnissicherung
    S=np.zeros(n)
    I=np.zeros(n) 
    R=np.zeros(n) 
    T=np.zeros(n)

    betaold= beta # krankheitsspezifische Infektionsrate für vor & nach Eingriff
    vaccon=0 #Impfung aus, bei eingestellter Impfrate und Zeitpkt dann an
    nlockdownend= nlockdown + E/(betaold-reduce*betaold) #Definition des Endes des Hygiene-Eingriffs


    # Bestimmung des zeitlichen Verlaufs, über die Euler Iteration
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
    

    # Plotten der Anteile
    plt.figure(figsize=[6, 4])      #figsize=[Breite, Höhe des Bildes]
    plt.plot(T, S, label="s(t)")    #plot(x-Achse, y-Achse, Beschriftung)
    plt.plot(T, I, label="i(t)")
    plt.plot(T, R, label= "r(t)")

    plt.grid()          #Gitter im Plot
    plt.legend()        #Legende im Plot
    plt.xlabel("Zeit t [Tagen]", fontsize=10)        #x-Achsen Beschriftung
    plt.ylabel("Anteil der Individuen", fontsize=10) #y-Achsen Beschriftung
    plt.title("Zeitlicher Verlauf einer kontrollierten Epidemie", fontsize= 10)  #Titel
    axes = plt.gca()
    axes.set_ylim([-0.05,1.05])

    # Einstellung für die Grenze des Gesundheitssystem
    if v.get()==1: 
        plt.axhline(y=0.01, color='r', linestyle='--', label="Gesundheitssystemgrenze")

    
    plt.show(block=False)
    
    print('Zur Zeit', n , 'sind', I[-1]* N, 'Menschen infiziert.')
    
    
    
    itmax= T[np.argmax(I)]
    imax= I.max()
    print('Das maximale I tritt mit diesem Eingriff am', itmax, 'Tag ein und entspricht', imax)


    # Berechnung einer 7-Tages Inzidenz
    incidence= np.convolve(I, np.ones(7)/7, mode='same')
    incidence= N/100000*incidence 
    plt.figure(figsize=[6, 4])
    plt.plot(T, incidence, label= "7-Tage-Inzidenz")
    plt.grid() 
    plt.legend()
    plt.xlabel("Zeit t [Tagen]", fontsize=10) 
    plt.ylabel("Zahl der Neuinfizierten in einer Woche \n pro 100.000 Einwohner", fontsize=10) #y-Achsen Beschriftung
    plt.title("Inzidenzzahl Entwicklung bei einer kontrollierten Epidemie" , fontsize= 10)  #Titel

    plt.show(block=False)


    # Berechnung der Gesamtzahl der Infizierten bis zur Zeit T
    gi =cumtrapz(I, dx=1, initial=0 )

    # Plotten des Gesamtanteils aller jemals Infizierten
    #   (Multiplikation mit Gamma, um mehrfach Zählung zu verhindern) 
    plt.figure(figsize=[6, 4])
    plt.plot(T,gi*gamma,label= r'$\nu_i$ (T)') 
    
    axes = plt.gca()
    plt.grid() 
    plt.legend() 
    plt.xlabel("Zeit T [Tagen]", fontsize=10) 
    plt.ylabel("Anteil aller Infizierten (summiert)", fontsize=10)
    plt.title("Entwicklung des Anteils der jemals Erkrankten \n in einer kontrollierten Epidemie", fontsize= 10)
    plt.rc('xtick', labelsize=10)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=10) 
    plt.rc('legend', fontsize=11)

    plt.show(block=False)
    
    print('Bis zum Tag', n, 'haben sich insgesamt', gi[-1]*gamma,
          '(umrechnen in Prozent!) Individuenen mit der Infektion angesteckt.')



    



'''

GUI Code: Ei

'''

# Ein Fenster erstellen
fenster = Tk()

# Den Fenstertitle erstellen
fenster.title("SIR Modell- Kontrollstrategien in einer Epidemie")

# Label und Buttons erstellen.
change_button = Button(fenster, text="Nächster Plot", command=button_action)
exit_button = Button(fenster, text="Beenden", command=fenster.quit)

anweisungs_label = Label(fenster, text="Vorher Parameterfile ausfüllen & speichern")
info_label = Label(fenster, text="Das Programm beenden.")

v = IntVar()
radio_label= Label(fenster, text="Maximale Auslastung des Gesundheitssystem", justify = LEFT, padx = 20)
radio_button1= Radiobutton(fenster, text="berücksichtigen",  variable=v, value=1)
radio_button2= Radiobutton(fenster, text="vernachlässigen",  variable=v, value=0)


# Nun fügen wir die Komponenten unserem Fenster in der gewünschten Reihenfolge hinzu.
radio_label.pack(side=TOP, pady=3)
radio_button1.pack(side=TOP)
radio_button2.pack(side=TOP)

anweisungs_label.pack(side=TOP, pady=3)
change_button.pack(side=TOP, pady=3)
info_label.pack(side=TOP, pady=3)
exit_button.pack(side=TOP, pady=3)

# In der Ereignisschleife auf Eingabe des Benutzers warten.

fenster.mainloop()











