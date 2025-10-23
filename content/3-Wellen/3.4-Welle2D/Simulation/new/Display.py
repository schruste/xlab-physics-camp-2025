

from Geo import *
import json

from ipywidgets import interact, interactive_output, interact_manual, Button, Output
from ipywidgets import FloatSlider, IntSlider, IntText, FloatLogSlider, FloatRangeSlider, Text, Dropdown, BoundedFloatText,IntRangeSlider
from ipywidgets import interactive, fixed, dlink, link, HBox, Box, VBox, Layout,Button
from IPython.display import clear_output,display, Javascript



### layout options
#box_layoutl = Layout(display='flex',flex_flow='column',align_items='stretch',width='65%')
#box_layouts = Layout(display='flex',flex_flow='column',align_items='stretch',width='35%')
#box_layouts = Layout(display='flex',flex_flow='column',align_items='stretch',heigth='90%')

style = {'description_width': 'initial'}
layout_button_left = Layout(width='400px', height='32px')
layout_button = Layout(width='575px', height='32px')
style_widget = {'description_width': '120px'}
layout_widget = Layout(width='575px', height='32px')
layout_left = Layout(width='400px', height='32px')




### define widgets and dictionaries of widgets
allfiles = ["Standard-Geometrie.json"]

button1 = Button(description="Auswertung starten",layout=layout_button_left)
options_todo = ['Geometrie laden', 'Geometrie speichern', 'Objekt hinzufügen', 'Objekt bearbeiten', 'Objekt entfernen', 'Alle Objekte entfernen']
options_material = ['Luft','Wasser','Fensterglas','Reflektion','Wachslinse','Prisma','Senderantennen','Außerhalb','freier Parameter']
options_boundary = ['Perfekt elektrisch (Dirichlet)','Leitend (Neumann)']
options_specialobj = ["Sender","Wachslinse","Prisma"]
options_evaluation =["Punkt","Gerade","Kreissektor" ]
options_objects = Dropdown(description='Objekttyp', options=['Spezialelemente','Block','Kreis'],style={'description_width': '125px'},layout=Layout(width='580px', height='32px'))

slider_wave=IntSlider(description='Wellenzahl',value=1300,min=500,max=3000,step=10,disabled=False, style=style_widget,layout=layout_widget)
slider_degree = IntSlider(description='Polynomgrad',value=4,min=1,max=6,disabled=False, style=style_widget,layout=layout_widget)
slider_maxh=FloatLogSlider(description='Gitterbreite', base=2,min=-10,max=-1,step=0.1, value=0.05, readout_format='.3f',disabled=False, style=style_widget,layout=layout_left)
slider_todo=Dropdown(description=' ',options=options_todo,value=None,disabled=False, style=style,layout=layout_left)

slider_name=Text(placeholder= 'Name', description='Name eingeben', disabled=False, style=style_widget,layout=layout_widget)
slider_refrac = BoundedFloatText(value=1,min=0, max=200,step=0.01,disabled =True)
slider_refrac2 = BoundedFloatText(description=' ',value=1,min=-3, max=200,step=0.01,disabled =False,style = style)
slider_refrac3 = Dropdown(description='Randbedingungen',value=None, options=options_boundary,style=style_widget)
slider_material = Dropdown(description='Materialparameter', value =None, options=options_material, style=style_widget,layout=Layout(width='450px', height='32px'))
slider_rotation = IntSlider(description='Rotationswinkel',value=0, min=0,max=360,step=1,disabled=False, style=style_widget,layout=layout_widget)
slider_xcoordinate = FloatSlider(description='x-Koordinate', value=0.0,min=(-Geo.current_rpml+0.02),max=(Geo.current_rpml-0.02),step=0.001,readout_format='.3f', disabled=False, style=style_widget,layout=layout_widget)
slider_ycoordinate = FloatSlider(description='y-Koordinate', value=0.0,min=(-Geo.current_rpml+0.02),max=(Geo.current_rpml-0.02),step=0.001,readout_format='.3f', disabled=False, style=style_widget,layout=layout_widget)


slider_evaluate = Dropdown(description='Auswertung an',value=None,options=options_evaluation,style=style_widget,layout=layout_left)
x1 = FloatSlider(description='x-Koordinate', value=0.0,min=(-Geo.current_rpml+0.02),max=(Geo.current_rpml-0.02),step=0.001, readout_format='.3f',disabled=False, style=style_widget,layout=layout_widget)
x2 =FloatSlider(description='x-Koordinate', value=0.0,min=(-Geo.current_rpml+0.02),max=(Geo.current_rpml-0.02),step=0.001, readout_format='.3f',disabled=False, style=style_widget,layout=layout_widget)
y1 = FloatSlider(description='y-Koordinate', value=0.0,min=(-Geo.current_rpml+0.02),max=(Geo.current_rpml-0.02),step=0.001,readout_format='.3f', disabled=False, style=style_widget,layout=layout_widget)
y2 = FloatSlider(description='y-Koordinate', value=0.0,min=(-Geo.current_rpml+0.02),max=(Geo.current_rpml-0.02),step=0.001, readout_format='.3f',disabled=False, style=style_widget,layout=layout_widget)
rad = FloatSlider(description='Radius',value=0.005,min=0.005,max=0.100,step=0.001, disabled=False, readout_format='.3f',style=style_widget,layout=layout_widget)
angle = IntRangeSlider(description='Winkelspanne', value=[0,180],min=0,max=360, disabled=False,style=style_widget,readout=False,layout=Layout(width='400px', height='32px'))
show_angle1 = IntText(description='von', value=0, min=0,max=360,disabled=True, style=style,layout=Layout(width='75px', height='32px'))
show_angle2 = IntText(description='bis', value=180, min=0,max=360,disabled=True, style=style,layout=Layout(width='75px', height='32px'))
angle_box = HBox([angle,show_angle1,show_angle2]) 

def angle_area(*args):
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



slider_change = Dropdown(description='Vorhandene Objekte',value=None,options=Geo.allnames, style=style_widget,layout=layout_widget)
slider_remove = Dropdown(description='Vorhandene Objekte',value=None,options=Geo.allnames, style=style_widget,layout=layout_widget)
file_load = Dropdown(options=allfiles,value=None, description='Dateien',style=style_widget,layout=layout_widget)
file_save = Text(value='Geometrie',placeholder= 'Datei', description='Dateiname', disabled=False,style=style_widget,layout=layout_widget)


output = Output()
output2 = Output()
output3 = Output()
num_obj = IntText(description='Anzahl Elemente', value=len(Geo.allnames),disabled=True,style=style_widget,layout=layout_left)


def print1(*args):
    num_obj.disabled = False
    num_obj.value = len(Geo.allnames)
    num_obj.disabled = True
    with output:
        output.clear_output()
        Geo.printObjects(False)
    with output2:
        output2.clear_output()
def print2():
    with output2:
        output2.clear_output()
        Geo.printObjects(True)


def update_list(var):
    var.on_click(print1)
    return

def update_objects(*args):
    if len(Geo.allnames) >=1:
        slider_remove.value=Geo.allnames[0]
    else:
        slider_remove.value = None
    slider_remove.options=Geo.allnames
    return


def disable_rot(*args):
    if slider_rotation == 0:
        block["Rotationspunktx"].disabled = True
        block["Rotationspunkty"].disabled = True
    else:
        block["Rotationspunktx"].disabled = False
        block["Rotationspunkty"].disabled = False

def reset(*args):
    slider_refrac3.value=None
    slider_material.value=None

def rotation_pointx(*args):
    x1,x2=block["Positionx"].value
    block["Rotationspunktx"].max=x2
    block["Rotationspunktx"].min=x1
    block["Rotationspunktx"].value=(x1+x2)/2

def rotation_pointy(*args):
    y1,y2=block["Positiony"].value
    block["Rotationspunkty"].max=y2
    block["Rotationspunkty"].min=y1
    block["Rotationspunkty"].value=(y1+y2)/2






sender ={
    "Name" : Text(placeholder= 'Name eingeben', value='Objekt',description='Name', disabled=False, style=style_widget,layout=layout_widget),
    "Sonderobjekt" : Dropdown(description='Objekt',options=options_specialobj,disable=False, style=style_widget,layout=layout_widget),
}

block ={        
    "Name" : Text(value ='Block',placeholder= 'Name eingeben', description='Name', disabled=False, style=style_widget,layout=layout_widget),
    "Positionx" : FloatRangeSlider(description='x-Koordinaten', value=[-0.01,0.01],min=(-Geo.current_rpml+0.02),max=(Geo.current_rpml-0.02),step=0.001, readout_format='.3f',disabled=False, style=style_widget,layout=layout_widget),
    "Positiony" : FloatRangeSlider(description='y-Koordinaten', value=[-0.01,0.01],min=(-Geo.current_rpml+0.02),max=(Geo.current_rpml-0.02),step=0.001, readout_format='.3f',disabled=False, style=style_widget,layout=layout_widget),
    "Rotationspunktx" : BoundedFloatText(description="Rotationsmittelpunkt"+5*" "+"x",value = 0, step=0.001,readout_format='.3f',min=(-Geo.current_rpml+0.02),max=(Geo.current_rpml-0.02),disabled=False, style={'description_width': '137px'},layout=Layout(width='345px', height='32px')),
    "Rotationspunkty" : BoundedFloatText(description='y',value = 0, step=0.001,readout_format='.3f',min=(-Geo.current_rpml+0.02),max=(Geo.current_rpml-0.02),disabled=False, style=style,layout=Layout(width='225px', height='32px'))

}

circle ={        
    "Name" : Text(value ='Kreis',placeholder= 'Name eingeben', description='Name', disabled=False, style=style_widget,layout=layout_widget),
    "Radius" : FloatSlider(description='Radius',value=0.005,min=0.005,max=0.3*pm.scale_domain,step=0.001, disabled=False, readout_format='.3f',style=style_widget,layout=layout_widget),
}




#########################################
def new_object(myobject):
    
    slider_refrac.layout.visibility = "hidden"
    slider_refrac2.layout.visibility = "hidden"
    slider_refrac3.layout.visibility = "hidden"
    slider_refrac.layout.width = "0%"
    slider_refrac2.layout.width = "0%"
    slider_refrac3.layout.height = "0%"


    def update2(*args):
        if slider_refrac3.value == "Perfekt elektrisch (Dirichlet)":
            slider_refrac2.value = -2.0
        else:
            slider_refrac2.value = -3.0

    def update(*args):
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
        elif slider_material.value == "Wasser":
            slider_refrac.layout.visibility = "visible"
            slider_refrac.layout.width = "115px"
            slider_refrac.diabled = False
            slider_refrac.value = 1.33
            slider_refrac2.value = slider_refrac.value
        elif slider_material.value == "Fensterglas":
            slider_refrac.layout.visibility = "visible"
            slider_refrac.layout.width = "115px"
            slider_refrac.diabled = False
            slider_refrac.value = 1.57
            slider_refrac2.value = slider_refrac.value
        elif slider_material.value == "Reflektion":
            slider_refrac.layout.visibility = "visible"
            slider_refrac.layout.width = "115px"
            slider_refrac.diabled = False
            slider_refrac.value = 10
            slider_refrac2.value = slider_refrac.value
        elif slider_material.value == "Wachslinse":
            slider_refrac.layout.visibility = "visible"
            slider_refrac.layout.width = "115px"
            slider_refrac.diabled = False
            slider_refrac.value = 1.57
            slider_refrac2.value = slider_refrac.value
        elif slider_material.value == "Prisma":
            slider_refrac.layout.visibility = "visible"
            slider_refrac.layout.width = "115px"
            slider_refrac.diabled = False
            slider_refrac.value = 1.65
            slider_refrac2.value = slider_refrac.value
        elif slider_material.value == "Senderarm":
            slider_refrac.layout.visibility = "visible"
            slider_refrac.layout.width = "115px"
            slider_refrac.diabled = False
            slider_refrac.value = 50
            slider_refrac2.value = slider_refrac.value
        elif slider_material.value == "freier Parameter":
            slider_refrac2.layout.visibility = "visible"
            slider_refrac2.layout.width = "115px"
            #slider_refrac.diabled = False
        else :
            slider_refrac3.layout.visibility = "visible"
            slider_refrac3.layout.heigth = "32px"
            slider_refrac3.layout.width = "575px"
            slider_refrac2.min = -3.0
            



    
    
    if myobject == 'Spezialelemente' :
        out = interactive(Geo.sender,{'manual': True, 'manual_name':'Objekt hinzufügen'},update=fixed(False),typ=sender["Sonderobjekt"],name=sender["Name"],x=slider_xcoordinate,y=slider_ycoordinate,rotation=slider_rotation)
        out.children[-2].layout=layout_button
        display(out)
        update_list(out.children[-2])
    elif myobject == 'Kreis':
        
        out = interactive(Geo.circle,{'manual': True, 'manual_name':'Kreis hinzufügen'},update=fixed(False),name=circle["Name"],x=slider_xcoordinate,y=slider_ycoordinate,rad=circle["Radius"],mat=slider_material,refrac=slider_refrac2)
        out.children[-2].layout=layout_button

        
        slider_refrac3.observe(update2, 'value')
        slider_material.observe(update, 'value')
        hbox = HBox([out.children[4],slider_refrac2,slider_refrac])
        vbox = VBox([out.children[0],out.children[1],out.children[2],out.children[3],hbox,slider_refrac3,out.children[6]])
        display(vbox)
        #display(out.children[-1])
        update_list(out.children[-2])
        out.children[-2].on_click(reset)
    elif myobject == 'Block':
        
        out = interactive(Geo.block,{'manual': True, 'manual_name':'Block hinzufügen'},update=fixed(False),name=block["Name"],x=block["Positionx"],y=block["Positiony"],rotation=slider_rotation,rotx=block["Rotationspunktx"],roty=block["Rotationspunkty"],mat=slider_material,refrac=slider_refrac2)
        out.children[-2].layout=layout_button

        slider_material.observe(update, 'value')
        slider_refrac3.observe(update2, 'value')
        block["Positionx"].observe(rotation_pointx, 'value')
        block["Positiony"].observe(rotation_pointy, 'value')
        slider_rotation.observe(disable_rot, 'value')
        hbox = HBox([out.children[6],out.children[7],slider_refrac])
        rot_point = HBox([out.children[4],out.children[5]])
        vbox = VBox([out.children[0],out.children[1],out.children[2],out.children[3],rot_point,hbox,slider_refrac3,out.children[8]])
        display(vbox)
        #display(out.children[-1])
        update_list(out.children[-2])
        out.children[-2].on_click(reset)
    else:
        
        return
   
    return 



def changeObject(myobject):
    """ Change the existing object 

        Args:
            name (String): name of the object
                
        Returns: None"""

    


    slider_refrac.layout.visibility = "hidden"
    slider_refrac2.layout.visibility = "hidden"
    slider_refrac3.layout.visibility = "hidden"
    slider_refrac.layout.width = "0%"
    slider_refrac2.layout.width = "0%"
    slider_refrac3.layout.height = "0%"

    def update2(*args):
        if slider_refrac3.value == "Perfekt elektrisch (Dirichlet)":
            slider_refrac2.value = -2.0
        else:
            slider_refrac2.value = -3.0


    def update(*args):
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
        elif slider_material.value == "Wasser":
            slider_refrac.layout.visibility = "visible"
            slider_refrac.layout.width = "115px"
            slider_refrac.diabled = False
            slider_refrac.value = 1.33
            slider_refrac2.value = slider_refrac.value
        elif slider_material.value == "Fensterglas":
            slider_refrac.layout.visibility = "visible"
            slider_refrac.layout.width = "115px"
            slider_refrac.diabled = False
            slider_refrac.value = 1.57
            slider_refrac2.value = slider_refrac.value
        elif slider_material.value == "Reflektion":
            slider_refrac.layout.visibility = "visible"
            slider_refrac.layout.width = "115px"
            slider_refrac.diabled = False
            slider_refrac.value = 10
            slider_refrac2.value = slider_refrac.value
        elif slider_material.value == "Wachslinse":
            slider_refrac.layout.visibility = "visible"
            slider_refrac.layout.width = "115px"
            slider_refrac.diabled = False
            slider_refrac.value = 1.57
            slider_refrac2.value = slider_refrac.value
        elif slider_material.value == "Prisma":
            slider_refrac.layout.visibility = "visible"
            slider_refrac.layout.width = "115px"
            slider_refrac.diabled = False
            slider_refrac.value = 1.65
            slider_refrac2.value = slider_refrac.value
        elif slider_material.value == "Senderarm":
            slider_refrac.layout.visibility = "visible"
            slider_refrac.layout.width = "115px"
            slider_refrac.diabled = False
            slider_refrac.value = 50
            slider_refrac2.value = slider_refrac.value
        elif slider_material.value == "freier Parameter":
            slider_refrac2.layout.visibility = "visible"
            slider_refrac2.layout.width = "115px"
            #slider_refrac.diabled = False
        else :
            slider_refrac3.layout.visibility = "visible"
            slider_refrac3.layout.heigth = "32px"
            slider_refrac3.layout.width = "575px"
            slider_refrac2.min = -3.0
            
       
    for i in Geo.allobjects: 
        if i["Name"] == myobject:
            if i["Typ"] == "Sender":
                #changable parameters for sender
                slider_xcoordinate.value = i["Mittelpunkt"][0]+0.25*0.0025
                slider_ycoordinate.value = i["Mittelpunkt"][1]+0.25*0.04
                slider_rotation.value = i["Rotationswinkel"]

                out = interactive(Geo.sender,{'manual': True, 'manual_name':'Objekt ändern'}, name=fixed(myobject),typ=fixed("Sender"),update=fixed(True),x=slider_xcoordinate,y=slider_ycoordinate,rotation=slider_rotation)
                out.children[-2].layout=layout_button
                display(out)
                update_list(out.children[-2])

            if i["Typ"] == "Wachslinse":
                #changable parameters for lens
                slider_xcoordinate.value = i["Mittelpunkt"][0]
                slider_ycoordinate.value = i["Mittelpunkt"][1]
                slider_rotation.value = i["Rotationswinkel"]
                
                out = interactive(Geo.sender,{'manual': True, 'manual_name':'Objekt ändern'},name=fixed(myobject),typ=fixed("Wachslinse"),update=fixed(True),x=slider_xcoordinate,y=slider_ycoordinate,rotation=slider_rotation)
                out.children[-2].layout=layout_button
                display(out)
                update_list(out.children[-2])

            if i["Typ"] == "Prisma":
                #changable parameters for prism
                slider_xcoordinate.value = i["Mittelpunkt"][0]
                slider_ycoordinate.value = i["Mittelpunkt"][1]
                slider_rotation.value = i["Rotationswinkel"]
                
                out = interactive(Geo.sender,{'manual': True, 'manual_name':'Objekt ändern'},name=fixed(myobject),typ=fixed("Prisma"),update=fixed(True),x=slider_xcoordinate,y=slider_ycoordinate,rotation=slider_rotation)
                out.children[-2].layout=layout_button
                display(out)
                update_list(out.children[-2])

                            
            elif  i["Typ"]== "Block":
                #changable parameters for block
                matold = i["Material"]
                if matold == i["Name"]:
                    matold = "freier Parameter"
                if matold == "Perfekt elektrisch (Dirichlet)" or matold == "Leitend (Neumann)":
                    matold = "Außerhalb"
                    
                xnew = block["Positionx"]
                ynew = block["Positiony"]
                xnew.value = [i["Koordinaten"][0][0],i["Koordinaten"][1][0]]
                ynew.value = [i["Koordinaten"][0][1],i["Koordinaten"][1][1]]
                slider_rotation.value = i["Rotationswinkel"]
                rotx = block["Rotationspunktx"]
                roty = block["Rotationspunkty"]
                block["Positionx"].observe(rotation_pointx, 'value')
                block["Positiony"].observe(rotation_pointy, 'value')
                rotx.value = i["Rotationsmittelpunkt"][0]
                roty.value = i["Rotationsmittelpunkt"][1]
                if matold != "Außerhalb":
                    slider_material.value = matold
                    slider_refrac2.value=i["Brechungsindex"]

                

                out = interactive(Geo.block, {'manual': True, 'manual_name':'Objekt ändern'},name=fixed(myobject),update=fixed(True),refrac=slider_refrac2,x=xnew,y=ynew,rotation=slider_rotation,mat=slider_material,rotx=rotx,roty=roty)
                out.children[-2].layout=layout_button
                

                slider_refrac3.observe(update2, 'value')
                slider_material.observe(update, 'value')
                hbox = HBox([out.children[5],slider_refrac,slider_refrac2])
                rot_box = HBox([out.children[3],out.children[4]])
                vbox = VBox([out.children[0],out.children[1],out.children[2],rot_box,hbox,slider_refrac3,out.children[-2]])
                display(vbox)
                update_list(out.children[-2])
                out.children[-2].on_click(reset)

                    
            elif i["Typ"] == "Kreis":
                #changable parameters for circle
                matold = i["Material"]
                if matold == i["Name"]:
                    matold = "freier Parameter"
                if matold == "Perfekt elektrisch (Dirichlet)" or matold == "Leitend (Neumann)":
                    matold = "Außerhalb"

                slider_xcoordinate.value = i["Mittelpunkt"][0]
                slider_ycoordinate.value = i["Mittelpunkt"][1]
                
                rnew = circle["Radius"]
                rnew.value = i["Radius"]
                if matold != "Außerhalb":
                    slider_refrac2.value=i["Brechungsindex"]
                    slider_material.value = matold
                

                out = interactive(Geo.circle, {'manual': True, 'manual_name':'Objekt ändern'},name=fixed(myobject),update=fixed(True),refrac=slider_refrac2,x=slider_xcoordinate,y=slider_ycoordinate,rad=rnew,mat=slider_material)
                out.children[-2].layout=layout_button


                slider_refrac3.observe(update2, 'value')
                slider_material.observe(update, 'value')
                hbox = HBox([out.children[3],slider_refrac,slider_refrac2])
                vbox = VBox([out.children[0],out.children[1],out.children[2],hbox,slider_refrac3,out.children[-2]])
                display(vbox)
                update_list(out.children[-2])
                out.children[-2].on_click(reset)

  
    return




def removeObject(oldob):
    """ Remove the existing object oldob

        Args:
            oldob (String): name of the object
                
        Returns: None"""
    
    for i in Geo.allobjects:
        if i["Name"] == oldob:
            if i["Typ"] == "Sender":
                Geo.current_sender = None
            else:
                Geo.allmaterial[i["Material"]].remove(i)
                if (len(Geo.allmaterial[i["Material"]])<1) and (i["Material"] in Geo.refraction):
                        del Geo.refraction[i["Material"]]
            Geo.allnames.remove(oldob)
            Geo.allobjects.remove(i)                    
            
            
            return
            
    display(Javascript(pm.error_removed))
    return



def removeAll():
    
    Geo.allobjects = []
    Geo.allnames = []
    Geo.allmaterial = {'Luft':[],'Wasser':[],'Fensterglas':[],'Reflektion':[],'Prisma': [], 'Wachslinse':[], 'Senderantenne':[],'Perfekt elektrisch (Dirichlet)':[],'Leitend (Neumann)':[]}
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
        Geo.sender(name=i["Name"],typ=i["Typ"],x=i["Mittelpunkt"][0],y=i["Mittelpunkt"][1],rotation=i["Rotationswinkel"])
        
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
            mygeo["Spezialobjekte"].append({"Name":i["Name"], "Typ":i["Typ"],"Mittelpunkt":i["Mittelpunkt"],"Rotationswinkel":i["Rotationswinkel"]})
        elif i["Typ"] == "Block":
            mygeo["Block"].append({"Name":i["Name"], "Typ":i["Typ"],"Koordinaten":i["Koordinaten"],"Rotationswinkel":i["Rotationswinkel"],"Rotationsmittelpunkt":i["Rotationsmittelpunkt"],"Material":i["Material"],"Brechungsindex":i["Brechungsindex"]})
        elif i["Typ"] == "Kreis":
            mygeo["Kreis"].append(i)
        else:
            return

    with open(filename, 'w') as json_file:
      json.dump(mygeo, json_file,indent=3)
                    
    return



 



# Visibility for Sliders


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
    
    if value == "Objekt hinzufügen":
        new_ob.layout.visibility = "visible"
        new_ob.layout.width = "60%"
    if value == "Objekt bearbeiten":
        slider_change.options = Geo.allnames
        change_ob.layout.visibility = "visible"
        change_ob.layout.width = "60%"
    if value == "Objekt entfernen":
        slider_remove.options = Geo.allnames
        remove_ob.layout.visibility = "visible"
        remove_ob.layout.width = "60%"
        update_list(remove_ob.children[-2])
        remove_ob.children[-2].on_click(update_objects)
    if value == "Alle Objekte entfernen":
        remove_all.layout.visibility = "visible"
        remove_all.layout.width = "60%"
        update_list(remove_all.children[-2])
        
    if value == "Geometrie laden":
        file_load.options = allfiles
        file_load.value = None
        load.layout.visibility = "visible"
        load.layout.width = "60%"
        update_list(load.children[-2])
    if value == "Geometrie speichern":
        save.layout.visibility = "visible"
        save.layout.width = "60%"
        update_list(save.children[-2])







                    



    
