import parameter as pm
from Geo import *
import Simulation as sim
import json
import os

from ipywidgets import interact, interactive_output, interact_manual, Button, Output
from ipywidgets import FloatSlider, IntSlider, IntText, FloatLogSlider, FloatRangeSlider, Text, Dropdown, BoundedFloatText,IntRangeSlider,ToggleButtons
from ipywidgets import interactive, fixed, dlink, link, HBox, Box, VBox, Layout,Button
from IPython.display import clear_output,display, Javascript





### layout optionsb
style = {'description_width': 'initial'}
layout_button_left = Layout(width='400px', height='32px')
layout_button = Layout(width='575px', height='32px')
style_widget = {'description_width': '120px'}
layout_widget = Layout(width='575px', height='32px')
layout_left = Layout(width='400px', height='32px')

##TODO anpassen der widgetgrößen layout_mobile = Layout(width='90%', height='32px')


### define widgets and dictionaries of widgets
allfiles = []
for file in os.listdir("."):
    if file.endswith(".json"): 
        allfiles.append(file)

allfiles = sorted(allfiles)


#button1 = Button(description="Auswertung starten",layout=layout_button_left)
# options for Dropdown-Widgets
options_todo = ['Geometrie laden', 'Geometrie speichern', 'Objekt hinzufügen', 'Objekt bearbeiten', 'Objekt entfernen', 'Alle Objekte entfernen']
options_material = ['Luft','Acrylglas','Wachs','Sand','Aluminium','freies Material']
options_boundary = ['Perfekt elektrisch (Dirichlet)']
options_specialobj = ["Sender","Wachslinse","Prisma"]
options_evaluation =["Punkt","Gerade","Kreisbogen" ]
options_objects = Dropdown(description='Objekttyp', options=['Spezialelemente','Block','Kreis'],style={'description_width': '125px'},layout=Layout(width='580px', height='32px'))

#########################################################################################################################
## Widgets for function start()
slider_maxh = FloatLogSlider(description='Gitterbreite', base=2,min=-10,max=-1,step=0.1, value=0.05, readout_format='.3f',disabled=False, style=style_widget,layout=layout_left)
slider_todo=Dropdown(description=' ',options=options_todo,value='Geometrie laden',disabled=False, style=style,layout=layout_left)


## Output-Widgets for print objects
dummy_btn = Button(description='',disabled=True,layout=layout_button_left,style = {'button_color': 'transparent'})
output = Output()
output2 = Output()
output3 = Output()
output4 = Output()
outputdraw = Output()
outputplot = Output()
outputplt = Output()
num_obj = IntText(description='Anzahl Elemente', value=len(Geo.allnames),disabled=True,style=style_widget,layout=layout_left)

## Widgets to generate/change objects
slider_name = Text(placeholder= 'Name', description='Name eingeben', disabled=False, style=style_widget,layout=layout_widget)
slider_refrac = BoundedFloatText(description=' n ',value=1,min=0, max=200,step=0.01,disabled =True,style = style)
slider_refrac2 = BoundedFloatText(description=' n ',value=1,min=-3, max=200,step=0.01,disabled =False,style = style)
slider_refrac3 = Dropdown(description='Randbedingungen',value=None, options=options_boundary,style=style_widget)
slider_material = Dropdown(description='Material', value =None, options=options_material, style=style_widget,layout=Layout(width='450px', height='32px'))
slider_rotation = IntSlider(description='Rotationswinkel',value=0, min=0,max=360,step=1,disabled=False, style=style_widget,layout=layout_widget)
slider_xcoordinate = FloatSlider(description='x-Koordinate', value=0.0,min=(-pm.current_rpml+0.02),max=(pm.current_rpml-0.02),step=0.001,readout_format='.3f', disabled=False, style=style_widget,layout=layout_widget)
slider_ycoordinate = FloatSlider(description='y-Koordinate', value=0.0,min=(-pm.current_rpml+0.02),max=(pm.current_rpml-0.02),step=0.001,readout_format='.3f', disabled=False, style=style_widget,layout=layout_widget)

## specific object widgets
sender ={
    "Name" : Text(placeholder= 'Name eingeben', value='Objekt',description='Name', disabled=False, style=style_widget,layout=layout_widget),
    "Sonderobjekt" : Dropdown(description='Objekt',options=options_specialobj,disable=False, style=style_widget,layout=layout_widget),
}
block ={        
    "Name" : Text(value ='Block',placeholder= 'Name eingeben', description='Name', disabled=False, style=style_widget,layout=layout_widget),
    "Positionx" : FloatRangeSlider(description='x-Koordinaten', value=[-0.1,0.1],min=(-pm.current_rpml+0.02),max=(pm.current_rpml-0.02),step=0.001, readout_format='.3f',disabled=False, style=style_widget,layout=layout_widget),
    "Positiony" : FloatRangeSlider(description='y-Koordinaten', value=[-0.1,0.1],min=(-pm.current_rpml+0.02),max=(pm.current_rpml-0.02),step=0.001, readout_format='.3f',disabled=False, style=style_widget,layout=layout_widget),
    "Rotationspunktx" : BoundedFloatText(description="Rotationsmittelpunkt"+5*" "+"x",value = 0, step=0.001,readout_format='.3f',min=(-pm.current_rpml+0.02),max=(pm.current_rpml-0.02),disabled=True, style={'description_width': '137px'},layout=Layout(width='345px', height='32px')),
    "Rotationspunkty" : BoundedFloatText(description='y',value = 0, step=0.001,readout_format='.3f',min=(-pm.current_rpml+0.02),max=(pm.current_rpml-0.02),disabled=True, style=style,layout=Layout(width='225px', height='32px'))
}

circle ={        
    "Name" : Text(value ='Kreis',placeholder= 'Name eingeben', description='Name', disabled=False, style=style_widget,layout=layout_widget),
    "Radius" : FloatSlider(description='Radius',value=0.01,min=0.005,max=0.3*pm.scale_domain,step=0.001, disabled=False, readout_format='.3f',style=style_widget,layout=layout_widget),
}

## Widgets for load/save geometry
slider_change = Dropdown(description='Vorhandene Objekte',value=None,options=Geo.allnames, style=style_widget,layout=layout_widget)
slider_remove = Dropdown(description='Vorhandene Objekte',value=None,options=Geo.allnames, style=style_widget,layout=layout_widget)
file_load = Dropdown(options=allfiles, description='Dateien',style=style_widget,layout=layout_widget)
file_save = Text(value='Geometrie',placeholder= 'Datei', description='Dateiname', disabled=False,style=style_widget,layout=layout_widget)


#########################################################################################################################
## Widgets for function solve_pde()
slider_wave=FloatLogSlider(description='Wellenlänge',base=2,value=0.028,min=-10,max=1,disabled=False, readout_format='.4f',style=style_widget,layout=layout_widget)
slider_degree = IntSlider(description='Polynomgrad',value=3,min=1,max=6,disabled=False, style=style_widget,layout=layout_widget)
slider_maxh2=FloatLogSlider(description='Gitterbreite', base=2,value=0.01,min=-10,max=-5.1,step=0.01, readout_format='.3f',disabled=False, style=style_widget,layout=layout_widget)
btn = Button(description='Gleichung lösen')

#########################################################################################################################
## Widgets for function evaluate()
slider_evaluate = Dropdown(description='Auswertung an',value=None,options=options_evaluation,style=style_widget,layout=layout_left)
x1 = FloatSlider(description='Punkt 1: x', value=-0.023,min=(-pm.current_rpml),max=(pm.current_rpml),step=0.001, readout_format='.3f',disabled=False, style=style_widget,layout=layout_widget)
x2 = FloatSlider(description='Punkt 2: x', value=0.0,min=(-pm.current_rpml),max=(pm.current_rpml),step=0.001, readout_format='.3f',disabled=False, style=style_widget,layout=layout_widget)
y1 = FloatSlider(description='Punkt 1: y', value=0.0,min=(-pm.current_rpml),max=(pm.current_rpml),step=0.001, readout_format='.3f', disabled=False, style=style_widget,layout=layout_widget)
y2 = FloatSlider(description='Punkt 2: y', value=0.0,min=(-pm.current_rpml),max=(pm.current_rpml),step=0.001, readout_format='.3f',disabled=False, style=style_widget,layout=layout_widget)
rad = FloatSlider(description='Radius',value=0.4,min=0.005,max=pm.current_rpml,step=0.001, disabled=False, readout_format='.3f',style=style_widget,layout=layout_widget)
angle1 = IntSlider(description='Winkel 1:', value=300, min=0, max=360,disabled=False, style=style_widget,layout=layout_widget)
angle2 = IntSlider(description='Winkel 2:', value=60, min=0, max=360,disabled=False, style=style_widget,layout=layout_widget)
#angle = IntRangeSlider(description='Winkelspanne', value=[0,180],min=0,max=360, disabled=False,style=style_widget,readout=False,layout=Layout(width='400px', height='32px'))
#show_angle1 = IntText(description='von', value=0, min=0,max=360,disabled=True, style=style,layout=Layout(width='75px', height='32px'))
#show_angle2 = IntText(description='bis', value=180, min=0,max=360,disabled=True, style=style,layout=Layout(width='75px', height='32px'))
#angle_box = HBox([angle,show_angle1,show_angle2]) 


def make_mobile(val = True):	
    if val:
        print("Switched to mobile version.")
    else:
        print("Switched to desktop version.")
    pm.isMobile=val
    return

def angle_area(*args):  ##not used
    """function that creates an admissible range for circle sector
        Parameter: observes the values of the slider for the angle

            - slider has 2 values: start and end
            - show these values in associated show_angle widget so that angle is between 0 and 359
            - the maximal angle value is start + 360°
            - if angle value is minimal angle value: decrease minimal/maximal angle value by 1 """
    start,end = angle.value
    show_angle1.disabled=False
    show_angle1.value=start%360
    show_angle1.disabled=True
    show_angle2.disabled=False
    show_angle2.value=end%360
    show_angle2.disabled=True
    
    angle.max = start+360
    if angle.value[0] == angle.min and start > 0:
        angle.value = (start,end)
        angle.min = start-1
        angle.max = end+360-1



##################################################################################################################################

## functions need for function start()
#### observations of buttons/sliders

def init_slider():
    slider_xcoordinate.min = -pm.current_rpml+0.02
    slider_ycoordinate.min = -pm.current_rpml+0.02
    block["Rotationspunktx"].min = -pm.current_rpml+0.02
    block["Rotationspunkty"].min = -pm.current_rpml+0.02
    block["Positionx"].min = -pm.current_rpml+0.02
    block["Positiony"].min = -pm.current_rpml+0.02
    x1.min = -pm.current_rpml+0.02
    x2.min = -pm.current_rpml+0.02
    y1.min = -pm.current_rpml+0.02
    y2.min = -pm.current_rpml+0.02
    slider_xcoordinate.max = pm.current_rpml-0.02
    slider_ycoordinate.max = pm.current_rpml-0.02
    block["Rotationspunktx"].max = pm.current_rpml-0.02
    block["Rotationspunkty"].max = pm.current_rpml-0.02
    block["Positionx"].max = pm.current_rpml-0.02
    block["Positiony"].max = pm.current_rpml-0.02
    x1.max = pm.current_rpml
    x2.max = pm.current_rpml
    y1.max = pm.current_rpml
    y2.max = pm.current_rpml
    rad.max = pm.current_rpml
    return

def reset_values():
    """observe buttons of add/change circle/block
        whenever button is clicked set parameters to default"""
    slider_refrac3.value=None
    slider_refrac3.layout.visibility = "hidden"
    slider_refrac3.layout.height = "0%"
    
    sender["Name"].value = "Objekt"
    block["Name"].value = "Block"
    circle["Name"].value = "Kreis"
    
    slider_refrac2.value=1
    slider_material.value=None
    slider_rotation.value = 0
    slider_xcoordinate.value = 0.0
    slider_ycoordinate.value = 0.0
    block["Positionx"].observe(rotation_pointx, 'value')
    block["Positiony"].observe(rotation_pointy, 'value')
    block["Positionx"].value = [-0.1,0.1]
    block["Positiony"].value = [-0.1,0.1]
    circle["Radius"].value = 0.1


def print1(*args):
    """called function whenever an button to added/changed/remove an object was clicked
        function to print list of current objects and set an counter for number of current objects"""
    reset_values()
    num_obj.disabled = False
    num_obj.value = len(Geo.allnames)
    num_obj.disabled = True
    sim.draw_geometry(slider_maxh.value)
    with output:
        output.clear_output()
        Geo.printObjects(False)
    with output2:
        output2.clear_output() ### clear detailed current objects
        
def print2():
    """called function of interactive-printall
        function to print detailed current objects"""
    with output2:
        output2.clear_output()
        Geo.printObjects(True)


def update_list(var):
    """observe all buttons:
        whenever an object is added/changed/remove:
                call the function to update the output that prints all current objects"""
    var.on_click(print1)
    
    return

def update_objects1(*args):
    """observe button of remove object
        whenever an object is removed, update dropdown list of widget, so that only current objects are shown"""
    slider_remove.value = None
    slider_remove.options=Geo.allnames
    return

def update_objects2(*args):
    """observe button of remove object
        whenever an object is removed, update dropdown list of widget, so that only current objects are shown"""
    slider_change.value = None
    slider_change.options=Geo.allnames
    return


def disable_rot(*args):
    """observer slider_rotation
        if rotation angle is zero, then rotation point of block cannot be changed and rotation midpoint is block midpoint"""
    x1,x2=block["Positionx"].value
    y1,y2=block["Positiony"].value
    if slider_rotation.value == 0:
        block["Rotationspunktx"].disabled = False
        block["Rotationspunkty"].disabled = False
        valx = format((x1+x2)/2, '.3f')
        valy = format((y1+y2)/2, '.3f')
        block["Rotationspunktx"].value=valx
        block["Rotationspunkty"].value=valy
        block["Rotationspunktx"].disabled = True
        block["Rotationspunkty"].disabled = True
    else:
        block["Rotationspunktx"].disabled = False
        block["Rotationspunkty"].disabled = False
        block["Rotationspunktx"].max=x2
        block["Rotationspunktx"].min=x1
        block["Rotationspunkty"].max=y2
        block["Rotationspunkty"].min=y1



def rotation_pointx(*args):
    """observe x-coordinates of block
        set admissble range so that x coordinate of the rotation point is inside the block
        if block is not rotated, rotation point cannot be changed
    """
    x1,x2=block["Positionx"].value
    block["Rotationspunktx"].disabled = False
    
    if block["Rotationspunktx"].max<x1:
        block["Rotationspunktx"].max=x2
        val = format((x1+x2)/2, '.3f')
        block["Rotationspunktx"].value=val
        block["Rotationspunktx"].min=x1
    else:
        block["Rotationspunktx"].min=x1
        val = format((x1+x2)/2, '.3f')
        block["Rotationspunktx"].value=val
        block["Rotationspunktx"].max=x2
    if slider_rotation.value == 0:
        block["Rotationspunktx"].disabled = True


def rotation_pointy(*args):
    """observe y-coordinates of block
        set admissble range so that y coordinate of the rotation point is inside the block
        if block is not rotated, rotation point cannot be changed
    """
    y1,y2=block["Positiony"].value
    block["Rotationspunkty"].disabled = False
    if block["Rotationspunkty"].max<y1:
        block["Rotationspunkty"].max=y2
        val = format((y1+y2)/2, '.3f')
        block["Rotationspunkty"].value=val
        block["Rotationspunkty"].min=y1
    else:
        block["Rotationspunkty"].min=y1
        val = format((y1+y2)/2, '.3f')
        block["Rotationspunkty"].value=val
        block["Rotationspunkty"].max=y2
    
    if slider_rotation.value == 0:
        block["Rotationspunkty"].disabled = True




def set_values_specialobj(obj):
    slider_xcoordinate.value = obj["Bezugspunkt"][0]
    slider_ycoordinate.value = obj["Bezugspunkt"][1]
    slider_rotation.value = obj["Rotationswinkel"]

def set_values_block(i):
    matold = i["Material"]
    if matold == i["Name"]:
        matold = "freies Material"
    if matold == "Aluminium":
        slider_refrac2.value = -2
    #if matold == "Leitend (Neumann)":
     #   matold = "Außerhalb"
      #  slider_refrac2.value = -3
    slider_material.value = matold
    if matold != "Aluminium":
        slider_refrac2.value=i["Brechungsindex"]

    slider_rotation.value = i["Rotationswinkel"]
    block["Positionx"].observe(rotation_pointx, 'value')
    block["Positiony"].observe(rotation_pointy, 'value')
    block["Positionx"].value = [i["Koordinaten"][0][0],i["Koordinaten"][1][0]]
    block["Positiony"].value = [i["Koordinaten"][0][1],i["Koordinaten"][1][1]]


    if slider_rotation.value != 0:
        block["Rotationspunktx"].value = i["Rotationsmittelpunkt"][0]
        block["Rotationspunkty"].value = i["Rotationsmittelpunkt"][1]

def set_values_circle(i):
    matold = i["Material"]
    if matold == i["Name"]:
        matold = "freies Material"
    if matold == "Aluminium":
        slider_refrac2.value = -2
#    if matold == "Leitend (Neumann)":
 #       matold = "Außerhalb"
  #      slider_refrac2.value = -3
    slider_material.value = matold
    if matold != "Aluminium":
        slider_refrac2.value=i["Brechungsindex"]

    slider_xcoordinate.value = i["Mittelpunkt"][0]
    slider_ycoordinate.value = i["Mittelpunkt"][1]
    circle["Radius"].value = i["Radius"]




### needed functions to show slider-menu depending on selection of todo-slider
    
def new_object(myobject):

    """create a new object
        depending on kind of object show different sliders"""

    #Sliders of refraction are only shown whenever corresponding material is selected
    slider_refrac.layout.visibility = "hidden"
    slider_refrac2.layout.visibility = "hidden"
    slider_refrac3.layout.visibility = "hidden"
    slider_refrac.layout.width = "0%"
    slider_refrac2.layout.width = "0%"
    slider_refrac3.layout.height = "0%"

    
    def update2(*args):
        """observe refraction3 widget with boundary conditions
                set passed parameter (slider_refrac2) to add object 
        """
        if slider_refrac3.value == "Perfekt elektrisch (Dirichlet)":
            slider_refrac2.value = -2.0
        else:
            slider_refrac2.value = -3.0

    def update(*args):
        """observe material dropdown widget
                depending on selected material: set the values of the refraction (slider_refrac and slider_refrac2)widget
                slider_refrac2 is passed parameter to add object
                show slider_refrac which is disabled (cannot change the value)
                    only for free parameter: show slider_refrac2 to choose a refraction value"""
        
        slider_refrac.layout.visibility = "hidden"
        slider_refrac2.layout.visibility = "hidden"
        slider_refrac3.layout.visibility = "hidden"
        slider_refrac.layout.width = "0%"
        slider_refrac2.layout.width = "0%"
        slider_refrac3.layout.height = "0%"
        slider_refrac2.min = 0.0
        if slider_material.value == "Luft":
            slider_refrac.layout.visibility = "visible"
            slider_refrac.layout.width = "115px"
            slider_refrac.diabled = False
            slider_refrac.value = 1
            slider_refrac2.value = slider_refrac.value
        elif slider_material.value == "Acrylglas":
            slider_refrac.layout.visibility = "visible"
            slider_refrac.layout.width = "115px"
            slider_refrac.diabled = False
            slider_refrac.value = 1.57
            slider_refrac2.value = slider_refrac.value
        elif slider_material.value == "Wachs":
            slider_refrac.layout.visibility = "visible"
            slider_refrac.layout.width = "115px"
            slider_refrac.diabled = False
            slider_refrac.value = 1.57
            slider_refrac2.value = slider_refrac.value
        elif slider_material.value == "Sand":
            slider_refrac.layout.visibility = "visible"
            slider_refrac.layout.width = "115px"
            slider_refrac.diabled = False
            slider_refrac.value = 1.65
            slider_refrac2.value = slider_refrac.value
        elif slider_material.value == "freies Material":
            slider_refrac2.layout.visibility = "visible"
            slider_refrac2.layout.width = "115px"
            slider_refrac2.value = 1.0
            slider_refrac2.min = 0.0
        else :
            #slider_refrac3.layout.visibility = "visible"
           # slider_refrac3.layout.heigth = "32px"
           # slider_refrac3.layout.width = "575px"
            slider_refrac2.min = -3.0
            


    
    if myobject == 'Spezialelemente' :
        out = interactive(Geo.sender,{'manual': True, 'manual_name':'Objekt hinzufügen'},update=fixed(False),typ=sender["Sonderobjekt"],name=sender["Name"],x=slider_xcoordinate,y=slider_ycoordinate,rotation=slider_rotation)
        out.children[-2].layout=layout_button
        vbox=VBox([out.children[0],out.children[1],out.children[2],out.children[3],out.children[4],out.children[5]])
        display(vbox)
        
        update_list(out.children[-2])
        #out.children[-2].on_click(reset_values)
        
    elif myobject == 'Kreis':
        out = interactive(Geo.circle,{'manual': True, 'manual_name':'Kreis hinzufügen'},update=fixed(False),name=circle["Name"],x=slider_xcoordinate,y=slider_ycoordinate,rad=circle["Radius"],mat=slider_material,refrac=slider_refrac2)
        out.children[-2].layout=layout_button

        #slider_refrac3.observe(update2, 'value')
        slider_material.observe(update, 'value')
        
        hbox = HBox([out.children[4],slider_refrac2,slider_refrac])
        vbox = VBox([out.children[0],out.children[1],out.children[2],out.children[3],hbox,out.children[6]])
        display(vbox)
       ## display(out.children[-1]) ###display if function had an output, eg error

        update_list(out.children[-2])
        #out.children[-2].on_click(reset_values)
        
    elif myobject == 'Block':
        out = interactive(Geo.block,{'manual': True, 'manual_name':'Block hinzufügen'},update=fixed(False),name=block["Name"],x=block["Positionx"],y=block["Positiony"],rotation=slider_rotation,rotx=block["Rotationspunktx"],roty=block["Rotationspunkty"],mat=slider_material,refrac=slider_refrac2)
        out.children[-2].layout=layout_button

        slider_material.observe(update, 'value')
        #slider_refrac3.observe(update2, 'value')
        slider_rotation.observe(disable_rot, 'value')
        block["Positionx"].observe(rotation_pointx, 'value')
        block["Positiony"].observe(rotation_pointy, 'value')
        slider_rotation.observe(disable_rot, 'value')
        
        hbox = HBox([out.children[6],out.children[7],slider_refrac])
        rot_point = HBox([out.children[4],out.children[5]])
        vbox = VBox([out.children[0],out.children[1],out.children[2],out.children[3],rot_point,hbox,out.children[8]])
        display(vbox)
   ##     display(out.children[-1]) ###display if function had an output, eg error

        update_list(out.children[-2])
        #out.children[-2].on_click(reset_values)
        
    else:
        return
   
    return 



def changeObject(myobject):
    """ Change the existing object 
            depending on kind of object show different sliders and set slider values to values of object
            
            Args: name (String): name of the object
            Returns: None"""

    
    #Sliders of refraction are only shown whenever corresponding material is selected
    slider_refrac.layout.visibility = "hidden"
    slider_refrac2.layout.visibility = "hidden"
    slider_refrac3.layout.visibility = "hidden"
    slider_refrac.layout.width = "0%"
    slider_refrac2.layout.width = "0%"
    slider_refrac3.layout.height = "0%"


    def update2(*args):
        """observe refraction3 widget with boundary conditions
                set passed parameter (slider_refrac2) to add object 
        """
        if slider_refrac3.value == "Perfekt elektrisch (Dirichlet)":
            slider_refrac2.value = -2.0
        else:
            slider_refrac2.value = -3.0

    def update(*args):
        """observe material dropdown widget
                depending on selected material: set the values of the refraction (slider_refrac and slider_refrac2)widget
                slider_refrac2 is passed parameter to add object
                show slider_refrac which is disabled (cannot change the value)
                    only for free parameter: show slider_refrac2 to choose a refraction value"""
        
        slider_refrac.layout.visibility = "hidden"
        slider_refrac2.layout.visibility = "hidden"
        slider_refrac3.layout.visibility = "hidden"
        slider_refrac.layout.width = "0%"
        slider_refrac3.layout.height = "0%"
        slider_refrac2.layout.height = "0%"
        
        if slider_material.value == "Luft":
            slider_refrac.layout.visibility = "visible"
            slider_refrac.layout.width = "115px"
            slider_refrac.diabled = False
            slider_refrac.value = 1
            slider_refrac2.value = slider_refrac.value
        elif slider_material.value == "Acrylglas":
            slider_refrac.layout.visibility = "visible"
            slider_refrac.layout.width = "115px"
            slider_refrac.diabled = False
            slider_refrac.value = 1.57
            slider_refrac2.value = slider_refrac.value
        elif slider_material.value == "Wachs":
            slider_refrac.layout.visibility = "visible"
            slider_refrac.layout.width = "115px"
            slider_refrac.diabled = False
            slider_refrac.value = 1.57
            slider_refrac2.value = slider_refrac.value
        elif slider_material.value == "Sand":
            slider_refrac.layout.visibility = "visible"
            slider_refrac.layout.width = "115px"
            slider_refrac.diabled = False
            slider_refrac.value = 1.65
            slider_refrac2.value = slider_refrac.value
        elif slider_material.value == "freies Material":
            slider_refrac2.layout.visibility = "visible"
            slider_refrac2.layout.width = "115px"
            slider_refrac2.value = 1.0
            slider_refrac2.min = 0.0
            #slider_refrac.diabled = False
        else :
            #slider_refrac3.layout.visibility = "visible"
            #slider_refrac3.layout.heigth = "32px"
            #slider_refrac3.layout.width = "575px"
            slider_refrac2.min = -3.0
            
    ### find selected object to show sliders according to the object type and set slider values
    if myobject == None:
        dummy = Button(layout=Layout(width='1px', height='1px'))
        display(dummy)
   # else:
    for i in Geo.allobjects: 
        if i["Name"] == myobject:
            if i["Typ"] == "Sender":
                #set changable parameters for sender with objects values
                set_values_specialobj(i)
                
                out = interactive(Geo.sender,{'manual': True, 'manual_name':'Objekt ändern'}, name=fixed(myobject),typ=fixed("Sender"),update=fixed(True),x=slider_xcoordinate,y=slider_ycoordinate,rotation=slider_rotation)
                out.children[-2].layout=layout_button
                vbox=VBox([out.children[0],out.children[1],out.children[2],out.children[3]])
                display(vbox)
                update_list(out.children[-2])
                out.children[-2].on_click(update_objects2)
                

            if i["Typ"] == "Wachslinse":
                #set changable parameters for lens with objects values 
                set_values_specialobj(i)

                out = interactive(Geo.sender,{'manual': True, 'manual_name':'Objekt ändern'},name=fixed(myobject),typ=fixed("Wachs"),update=fixed(True),x=slider_xcoordinate,y=slider_ycoordinate,rotation=slider_rotation)
                out.children[-2].layout=layout_button
                vbox=VBox([out.children[0],out.children[1],out.children[2],out.children[3]])
                display(vbox)
                update_list(out.children[-2])
                out.children[-2].on_click(update_objects2)
                

            if i["Typ"] == "Prisma":
                #set changable parameters for prism with objects values
                set_values_specialobj(i)

                out = interactive(Geo.sender,{'manual': True, 'manual_name':'Objekt ändern'},name=fixed(myobject),typ=fixed("Sand"),update=fixed(True),x=slider_xcoordinate,y=slider_ycoordinate,rotation=slider_rotation)
                out.children[-2].layout=layout_button
                vbox=VBox([out.children[0],out.children[1],out.children[2],out.children[3]])
                display(vbox)
                update_list(out.children[-2])
                out.children[-2].on_click(update_objects2)
                

            elif  i["Typ"]== "Block":
                #set changable parameters for block with objects values
                set_values_block(i)


                out = interactive(Geo.block, {'manual': True, 'manual_name':'Objekt ändern'},name=fixed(myobject),update=fixed(True),refrac=slider_refrac2,x=block["Positionx"],y=block["Positiony"],rotation=slider_rotation,mat=slider_material,rotx=block["Rotationspunktx"],roty=block["Rotationspunkty"])
                out.children[-2].layout=layout_button
                
                block["Positionx"].observe(rotation_pointx, 'value')
                block["Positiony"].observe(rotation_pointy, 'value')
                #slider_refrac3.observe(update2, 'value')
                slider_material.observe(update, 'value')
                
                hbox = HBox([out.children[5],slider_refrac,slider_refrac2])
                rot_box = HBox([out.children[3],out.children[4]])
                vbox = VBox([out.children[0],out.children[1],out.children[2],rot_box,hbox,out.children[-2]])
                display(vbox)
                update_list(out.children[-2])
                out.children[-2].on_click(update_objects2)
                

                    
            elif i["Typ"] == "Kreis":
                #changable parameters for circle
                set_values_circle(i)
                

                out = interactive(Geo.circle, {'manual': True, 'manual_name':'Objekt ändern'},name=fixed(myobject),update=fixed(True),refrac=slider_refrac2,x=slider_xcoordinate,y=slider_ycoordinate,rad=circle["Radius"],mat=slider_material)
                out.children[-2].layout=layout_button


                #slider_refrac3.observe(update2, 'value')
                slider_material.observe(update, 'value')
                hbox = HBox([out.children[3],slider_refrac,slider_refrac2])
                vbox = VBox([out.children[0],out.children[1],out.children[2],hbox,out.children[-2]])
                display(vbox)
                update_list(out.children[-2])
                out.children[-2].on_click(update_objects2)
        

  
    return




def removeObject(oldob):
    """ Remove the existing object oldob

        Args: oldob (String): name of the object       
        Returns: None"""
    
    for i in Geo.allobjects:
        if i["Name"] == oldob:
            if i["Typ"] == "Sender":
                Geo.current_sender = None

            Geo.allnames.remove(oldob)
            Geo.allobjects.remove(i)                    
            Geo.update_refrac_list()
            
            return
            
    return



def removeAll():
    
    Geo.allobjects = []
    Geo.allnames = []
    Geo.refraction = {}
    Geo.allmaterial = {'Luft':[],'Acrylglas':[],'Sand': [], 'Wachs':[], 'Aluminium':[],'Perfekt elektrisch (Dirichlet)':[],'Senderantenne':[]}
    Geo.current_sender = None

    return



def load_geo(filename):
    if filename==None:
        display(Javascript(pm.error_missing))
        return
    removeAll() ## Lösche vorhandene Objekte

    with open(filename) as json_file:
        mygeo = json.load(json_file)
        
    s=mygeo["Spezialobjekte"]
    b=mygeo["Block"]
    k=mygeo["Kreis"]
    for i in s:
        Geo.sender(name=i["Name"],typ=i["Typ"],x=i["Bezugspunkt"][0],y=i["Bezugspunkt"][1],rotation=i["Rotationswinkel"])
        
    for i in b:
        Geo.block(name=i["Name"],x=(i["Koordinaten"][0][0],i["Koordinaten"][1][0]),y=(i["Koordinaten"][0][1],i["Koordinaten"][1][1]),rotation=i["Rotationswinkel"],rotx=i["Rotationsmittelpunkt"][0],roty=i["Rotationsmittelpunkt"][1],mat=i["Material"],refrac=i["Brechungsindex"])
        
    for i in k:
        Geo.circle(name=i["Name"],x=i["Mittelpunkt"][0],y=i["Mittelpunkt"][1],rad=i["Radius"],mat=i["Material"],refrac=i["Brechungsindex"])
    return



def save_geo(filename):
    if filename==None:
        display(Javascript(pm.error_missing))
        return
            
    filename = filename+'.json'
    if filename in allfiles:
        display(Javascript(pm.error_name))
        return 
    allfiles.append(filename)
    mygeo = {"Spezialobjekte":[],"Block":[],"Kreis":[]}
    for i in Geo.allobjects:
        if i["Typ"] == "Sender" or i["Typ"] == "Prisma" or i["Typ"] == "Wachslinse":
            mygeo["Spezialobjekte"].append({"Name":i["Name"], "Typ":i["Typ"],"Bezugspunkt":i["Bezugspunkt"],"Rotationswinkel":i["Rotationswinkel"]})
        elif i["Typ"] == "Block":
            if i["Material"]=="Aluminium":
                mygeo["Block"].append({"Name":i["Name"], "Typ":i["Typ"],"Koordinaten":i["Koordinaten"],"Rotationswinkel":i["Rotationswinkel"],"Rotationsmittelpunkt":i["Rotationsmittelpunkt"],"Material":i["Material"],"Brechungsindex":0})
            else:    
                mygeo["Block"].append({"Name":i["Name"], "Typ":i["Typ"],"Koordinaten":i["Koordinaten"],"Rotationswinkel":i["Rotationswinkel"],"Rotationsmittelpunkt":i["Rotationsmittelpunkt"],"Material":i["Material"],"Brechungsindex":i["Brechungsindex"]})
        elif i["Typ"] == "Kreis":
            if i["Material"]=="Aluminium":
                mygeo["Kreis"].append({"Name":i["Name"], "Typ":i["Typ"],"Mittelpunkt":i["Mittelpunkt"],"Radius":i["Radius"],"Material":i["Material"],"Brechungsindex":0})
            else:
                mygeo["Kreis"].append(i)
        else:
            return

    with open(filename, 'w') as json_file:
      json.dump(mygeo, json_file,indent=3)
                    
    return



 



# Visibility for sliders/widgets depending on which action is selected with the todo slider


new_ob = interactive(new_object, myobject=options_objects)
change_ob = interactive(changeObject, myobject=slider_change)
remove_ob = interactive(removeObject,{'manual': True, 'manual_name':'Objekte entfernen'}, oldob=slider_remove)
remove_all = interactive(removeAll,{'manual': True, 'manual_name':'Alles löschen?'})
load = interactive(load_geo,{'manual': True, 'manual_name':'Geometrie laden'}, filename=file_load)
save = interactive(save_geo, {'manual': True, 'manual_name':'Geometrie speichern'}, filename=file_save)

remove_ob.children[-2].layout=layout_button
remove_all.children[-2].layout=layout_button
load.children[-2].layout=layout_button
save.children[-2].layout=layout_button



def show_slider(value):
    new_ob.layout.visibility = "hidden"
    change_ob.layout.visibility = "hidden"
    remove_ob.layout.visibility = "hidden"
    remove_all.layout.visibility = "hidden"
    load.layout.visibility = "hidden"
    save.layout.visibility = "hidden"
    
    new_ob.layout.width = "0%"
    change_ob.layout.width = "0%"
    remove_ob.layout.width = "0%"
    remove_all.layout.width = "0%"
    load.layout.width = "0%"
    save.layout.width = "0%"
    
    if pm.isMobile:
    	new_ob.layout.height = "1px"
    	change_ob.layout.height = "1px"
    	remove_ob.layout.height = "1px"
    	remove_all.layout.height = "1px"
    	load.layout.height = "1px"
    	save.layout.height = "1px"
    else:
    	new_ob.layout.height = "100%"
    	change_ob.layout.height = "100%"
    	remove_ob.layout.height = "100%"
    	remove_all.layout.height = "100%"
    	load.layout.height = "100%"
    	save.layout.height = "100%"
    
    if value == "Objekt hinzufügen":
        slider_refrac3.layout.visibility = "hidden"
        slider_refrac3.layout.height = "0%"
        new_ob.layout.visibility = "visible"
        if pm.isMobile:
        	new_ob.layout.width = "60%"
        	new_ob.layout.height = "100%"
        	print("test")
        else:
        	new_ob.layout.width = "60%"
        reset_values()
    if value == "Objekt bearbeiten":
        slider_change.options = Geo.allnames
        change_ob.layout.visibility = "visible"
        if pm.isMobile:
        	change_ob.layout.width = "60%"
        	change_ob.layout.height = "100%"
        else:
        	change_ob.layout.width = "60%"
        slider_change.value = None
        
    if value == "Objekt entfernen":
        slider_remove.options = Geo.allnames
        remove_ob.layout.visibility = "visible"
        if pm.isMobile:
        	remove_ob.layout.width = "60%"
        	remove_ob.layout.height = "100%"
        else:
        	remove_ob.layout.width = "60%"
        update_list(remove_ob.children[-2])
        remove_ob.children[-2].on_click(update_objects1)
    if value == "Alle Objekte entfernen":
        remove_all.layout.visibility = "visible"
        if pm.isMobile:
        	remove_all.layout.width = "60%"
        	remove_all.layout.height = "100%"
        else:
        	remove_all.layout.width = "60%"
        update_list(remove_all.children[-2])
        
    if value == "Geometrie laden":
        file_load.options = allfiles
        file_load.value ='Doppelspalt.json'
        load.layout.visibility = "visible"
        if pm.isMobile:
        	load.layout.width = "60%"
        	load.layout.height = "100%"
        else:
        	load.layout.width = "60%"
        update_list(load.children[-2])
    if value == "Geometrie speichern":
        save.layout.visibility = "visible"
        if pm.isMobile:
        	save.layout.width = "60%"
        	save.layout.height = "100%"
        else:
        	save.layout.width = "60%"
        update_list(save.children[-2])







                    



    
