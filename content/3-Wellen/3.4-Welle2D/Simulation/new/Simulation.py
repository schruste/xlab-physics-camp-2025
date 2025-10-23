from IPython.core.display import display, HTML

display(HTML("<style>.container { width:100% !important; }</style>"))

import json
import Display as dp
import parameter as pm
from Geo import *
from math import sqrt, pi,sin,cos,radians


from ipywidgets import interactive, fixed, HBox, Box, VBox 
from IPython.display import display, clear_output, Javascript
import matplotlib.pyplot as plt


on_init ="""
  let webgui = require("ngsolve_jupyter_widgets");
  let THREE = webgui.THREE;
  
  scene.on("selectpoint", (scene, p) => {
      let message = "you clicked on point (";
      message += p.x + ", ";
      message += p.y + ", ";
      message += p.z + ")";
      alert(message);
  });
"""


### Standard options for the domain


radius_pml = pm.scale_domain*0.4
radius_outer = pm.scale_domain*0.56
geodomain = Geo(radius_pml,radius_outer)


### Generate standard geometry and save in pickle-file
standard_geo = {"Spezialobjekte":[{"Name":"MySender", "Typ":"Sender", "Mittelpunkt":(-0.28,0.0), "Rotationswinkel":0}],
                "Block":[{"Name":"Block1", "Typ":"Block", "Koordinaten":[(0.12,-0.32),(0.16,-0.12)], "Rotationswinkel":0, "Rotationsmittelpunkt":(0.14,-0.22), "Material":'Reflektion',"Brechungsindex":10},
                         {"Name":"Block2", "Typ":"Block", "Koordinaten":[(0.12,-0.04),(0.16,0.04)], "Rotationswinkel":0,"Rotationsmittelpunkt":(0.14,0.0), "Material":'Reflektion',"Brechungsindex":10},
                         {"Name":"Block3", "Typ":"Block", "Koordinaten":[(0.12,0.12),(0.16,0.32)],"Rotationswinkel":0,"Rotationsmittelpunkt":(0.14,0.22), "Material":'Reflektion',"Brechungsindex":10}]
                ,"Kreis":[]
                }


with open('Standard-Geometrie.json', 'w') as json_file:
  json.dump(standard_geo, json_file,indent=3)



def draw_geometry(maxh):
    

    cf, mesh = Geo.drawGeo(maxh,geodomain)
    if mesh == None:
        return
    Draw(cf, mesh,js_code=on_init)

    return

def solveWave(maxh,degree, wave=1000):
    """ Solve the wave equation
            Args: wave  (double)
                refraction_blocks (double): =10 for reflection
                                    =1.5 for glass
                                    =1 for air
            mesh (NGSmesh)"""
    
    if Geo.current_sender == None:
        display(Javascript(pm.error_sender2))
        return
    if Geo.ngmesh == None or maxh !=Geo.maxh:
        Geo.drawGeo(maxh,geodomain)



    alpha_d = {"mat1" : 1, "mat2" : 1}
    alpha_d.update(Geo.refraction)
    m_fac = CoefficientFunction([alpha_d[mat] for mat in Geo.ngmesh.GetMaterials()])


    k = wave * m_fac
    uin = exp (-1J*k*x)

    fes = H1(Geo.ngmesh, complex=True, order=degree, dirichlet="scatterer|electric")
    u = fes.TrialFunction()
    v = fes.TestFunction()

    
    c = 5
    if Geo.maxh/degree*wave > c:
        display(Javascript(pm.resolution))
    

    uscat = GridFunction (fes)
    uscat.Set (uin, definedon=Geo.ngmesh.Boundaries("scatterer"))

    a = BilinearForm (fes, symmetric=True)
    a += SymbolicBFI (grad(u)*grad(v) )
    a += SymbolicBFI (-k*k*u*v)

    f = LinearForm (fes)

    a.Assemble()
    f.Assemble()

    res = uscat.vec.CreateVector()
    res.data = f.vec - a.mat * uscat.vec
    uscat.vec.data += a.mat.Inverse(freedofs=fes.FreeDofs(), inverse="sparsecholesky") * res

    Draw(uscat,Geo.ngmesh,js_code=on_init)
    pm.gridfct = uscat
    
    return uscat



### function to start interactive options
def start():
    def clear_geo(*args):
        with draw2.children[0]:
            draw2.children[0].clear_output()
        
    draw2 = interactive(draw_geometry,maxh=fixed(0.05))
    
    todo = interactive(dp.show_slider,value=dp.slider_todo)
    draw = interactive(draw_geometry,{'manual': True, 'manual_name':'Geometrie zeichnen'},maxh=dp.slider_maxh)
    printall = interactive(dp.print2,{'manual': True, 'manual_name':'Objekte ausführlich anzeigen'})

    todo.layout.height='45px'
    draw.children[1].layout=dp.layout_button_left
    printall.children[-2].layout=dp.layout_button_left
    if Geo.maxh != None:
        dp.slider_maxh.value=Geo.maxh
    
    v1 = VBox([draw.children[0],draw.children[1],todo,dp.num_obj,printall,dp.output])
    
    menu = HBox(children=[v1, dp.new_ob, dp.change_ob,dp.remove_ob, dp.remove_all, dp.load,dp.save])
    draw.children[1].on_click(clear_geo)
    v =VBox([draw2,draw.children[-1],menu,dp.output2])
    return   v


def solve_pde():
    solve = interactive(solveWave,{'manual': True, 'manual_name':'Gleichung lösen'},maxh=dp.slider_maxh,degree=dp.slider_degree,wave=dp.slider_wave)
    if Geo.maxh != None:
        dp.slider_maxh.value=Geo.maxh
    dp.slider_maxh.layout = dp.layout_widget
    solve.children[-2].layout=dp.layout_button

    box=VBox([solve.children[0],solve.children[1],solve.children[2],solve.children[3],solve.children[-1]])
    
    return box



def evaluate():

    def show_boxes(*args):
        box_p.layout.visibility = "hidden"
        box_p.layout.width = "0%"
        box_l.layout.visibility = "hidden"
        box_l.layout.width = "0%"
        box_c.layout.visibility = "hidden"
        box_c.layout.width = "0%"

        if dp.slider_evaluate.value =='Punkt':
            box_p.layout.visibility = "visible"
            box_p.layout.width = "50%"
            dp.x2.value=0
            dp.y2.value=0
            dp.rad.value=0
            dp.angle.value=(0,90)
            
        elif dp.slider_evaluate.value =='Gerade':
            box_l.layout.visibility = "visible"
            box_l.layout.width = "50%"
            dp.rad.value=0
            dp.angle.value=(0,90)

        elif dp.slider_evaluate.value =='Kreissektor':
            box_c.layout.visibility = "visible"
            box_c.layout.width = "50%"
            dp.x2.value=0
            dp.y2.value=0
        else:
            return
        
    
    def evaluation(value,x1,y1,rad,x2,y2,angle):

        if value =='Punkt':

            print("Realteil:\t", pm.gridfct(x1,y1).real)
            print("Imaginärteil:\t",pm.gridfct(x1,y1).imag)
            print("Norm:\t\t",abs(pm.gridfct(x1,y1)))
  
        elif value =='Gerade':
            if x1==x2 and y1==y2:
                return

            length = sqrt((x1-x2)**2+(y1-y2)**2)
            steps = length/0.0001
            real_list = []
            imag_list = []
            abs_list = []
            for i in range(int(steps)+1):
                pntx = x1 + i/steps*length *(x2-x1)
                pnty = y1 + i/steps*length *(y2-y1)
                val = pm.gridfct(pntx,pnty)
                real_list.append(val.real)
                imag_list.append(val.imag)
                abs_list.append(abs(val))
            plt.plot(real_list, label='Realteil')
            plt.plot(imag_list, label='Imaginärteil')
            plt.plot(abs_list, label='Norm')
            plt.legend()
            plt.show()
            #plt.savefig('plot.png')

            
        elif value =='Kreissektor':

            #check if object is inside the domain
            if (sqrt(x1**2+y1**2)+rad >= Geo.current_rpml):
                display(Javascript(pm.warning_outside))
            
            start,end = angle
            angular_range=end-start
            length = pi*2*rad*angular_range/360
            steps = length/0.0001
            real_list = []
            imag_list = []
            abs_list = []
            for i in range(int(steps)+1):
                pntx = x1 + rad * cos(radians(start+i*360/steps))
                pnty = y1 + rad * sin(radians(start+i*360/steps))
                val = pm.gridfct(pntx,pnty)
                real_list.append(val.real)
                imag_list.append(val.imag)
                abs_list.append(abs(val))
            plt.plot(real_list, label='Realteil')
            plt.plot(imag_list, label='Imaginärteil')
            plt.plot(abs_list, label='Norm')
            plt.legend()
            plt.show()
        else:
            return
            
        return 

    box_p=VBox([dp.x1,dp.y1])
    box_l=VBox([dp.x1,dp.y1,dp.x2,dp.y2])
    box_angle =HBox([dp.angle,dp.show_angle1,dp.show_angle2])
    box_c=VBox([dp.x1,dp.y1,dp.rad,box_angle])
    
    box_p.layout.visibility = "hidden"
    box_p.layout.width = "0%"
    box_l.layout.visibility = "hidden"
    box_l.layout.width = "0%"
    box_c.layout.visibility = "hidden"
    box_c.layout.width = "0%"
   
    eva = interactive(evaluation, {'manual': True, 'manual_name':'Gleichung lösen'},value=dp.slider_evaluate,x1=dp.x1,y1=dp.y1,x2=dp.x2,y2=dp.y2,rad=dp.rad,angle=dp.angle)
    eva.children[-2].layout=dp.layout_button_left
    
    dp.slider_evaluate.observe(show_boxes, 'value')
    #print(eva)
    dp.angle.observe(dp.angle_area, 'value')
    vbox=VBox([eva.children[0],eva.children[-2]])
    #vbox2=VBox(box)
    hbox=HBox([vbox,box_p,box_l,box_c])
    display(hbox)
    display(eva.children[-1])
    #display(eva.result)

    return



    
