import matplotlib.pyplot as plt
from numpy import nan
from IPython import display

#%matplotlib notebook
import ipywidgets as widgets
import matplotlib.pyplot as plt

def plot(positions,velocities,ax,time):
    if ax.lines:
        for i,line in enumerate(ax.lines):
            if i==0:
                line.set_ydata(positions)
                line.set_label('Auslenkung zum Zeitpunkt'+"{:12.8f}".format(time))
            #else:
            #    line.set_ydata(velocities)
    else:
        ax.plot(positions,'-o',label='Auslenkung '+str(time))
        #ax.plot(velocities,'-',label='Geschwindigkeit · 1')
    ax.legend()
     
def ShowPlots(positions,velocities,time_distance):
    fig, ax = plt.subplots(1,1)
    ax.set_ylim([-1.1,1.1])
    
    fig.set_figheight(3)
    fig.set_figwidth(9)
    
    out = widgets.Output()
    def on_value_change(change):
        with out:
            plot(positions[change['new']],velocities[change['new']],ax, change['new']*time_distance)
            fig.canvas.draw()   
    
    slider = widgets.IntSlider(min=0, max=len(positions)-1, step=1, continuous_update=True)
    
    play = widgets.Play(min=0,  max=len(positions)-1, interval=100)
    
    slider.observe(on_value_change, 'value')
    widgets.jslink((play, 'value'), (slider, 'value'))
    ui = widgets.VBox([play, slider,out])
    #display.display(widgets.VBox([play, slider,out]))
    display.display(ui,out)

def GetSliderPlay(positions,velocities):
    fig, ax = plt.subplots(1,1)
    ax.set_ylim([-1.1,1.1])
    
    fig.set_figheight(3)
    fig.set_figwidth(9)
    
    out = widgets.Output()
    def on_value_change(change):
        with out:
            plot(positions[change['new']],velocities[change['new']],ax, change['new']*time_distance)
            fig.canvas.draw()   
    
    slider = widgets.IntSlider(min=0, max=len(positions)-1, step=1, continuous_update=True)
    
    play = widgets.Play(min=0,  max=len(positions)-1, interval=100)
    
    return slider,play,on_value_change,out
