import matplotlib.pyplot as plt
from numpy import nan
from IPython import display

def plot(timehistory, poshistory, velhistory):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(20, 4))
    plt.plot(timehistory, poshistory,'-o',label='displacement')
    plt.plot(timehistory, velhistory,'-*',label='orbital velocity')
    plt.xlabel("Zeit")
    plt.legend()
    plt.show()
