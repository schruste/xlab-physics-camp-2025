from IPython.core.display import display, HTML

display(HTML("<style>.container { width:100% !important; }</style>"))

import json
import Display as dp
import parameter as pm
from Geo import *
from math import sqrt, pi,sin,cos,radians


from ipywidgets import interactive, interact, fixed, HBox, Box, VBox,Button, Checkbox
from IPython.display import display, clear_output, Javascript
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import csv 
from ngsolve.webgui import Draw

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



### Generate standard geometry and save in pickle-file
standard_geo = {"Spezialobjekte":[{"Name":"MySender", "Typ":"Sender", "Bezugspunkt":(-0.28,0.0), "Rotationswinkel":0}],
                "Block":[{"Name":"Block1", "Typ":"Block", "Koordinaten":[(0.12,-0.32),(0.16,-0.12)], "Rotationswinkel":0, "Rotationsmittelpunkt":(0.14,-0.22), "Material":'Reflektion',"Brechungsindex":10},
                         {"Name":"Block2", "Typ":"Block", "Koordinaten":[(0.12,-0.04),(0.16,0.04)], "Rotationswinkel":0,"Rotationsmittelpunkt":(0.14,0.0), "Material":'Reflektion',"Brechungsindex":10},
                         {"Name":"Block3", "Typ":"Block", "Koordinaten":[(0.12,0.12),(0.16,0.32)],"Rotationswinkel":0,"Rotationsmittelpunkt":(0.14,0.22), "Material":'Reflektion',"Brechungsindex":10}]
                ,"Kreis":[]
                }

double_split = {"Spezialobjekte":[{"Name":"Sender", "Typ":"Sender", "Bezugspunkt":(-0.45,0.0), "Rotationswinkel":0},
								{"Name":"Wachslinse", "Typ":"Wachslinse","Bezugspunkt":(-0.05,0.0), "Rotationswinkel":180 }],
                "Block":[{"Name":"Alu-Blech1", "Typ":"Block", "Koordinaten":[(0.15,-0.0675),(0.1515,-0.2775)], "Rotationswinkel":0, "Rotationsmittelpunkt":(0.15,-0.1725), "Material":'Aluminium',"Brechungsindex":0},
                         {"Name":"Alu-BlechMitte", "Typ":"Block", "Koordinaten":[(0.15,-0.0425),(0.1515,0.0425)], "Rotationswinkel":0,"Rotationsmittelpunkt":(0.15,0.0), "Material":'Aluminium',"Brechungsindex":0},
                         {"Name":"Alu-Blech2", "Typ":"Block", "Koordinaten":[(0.15,0.0675),(0.1515,0.2775)],"Rotationswinkel":0,"Rotationsmittelpunkt":(0.15,0.1725), "Material":'Aluminium',"Brechungsindex":0}]
                ,"Kreis":[]
                }
                
acryl = {"Spezialobjekte":[{"Name":"Sender", "Typ":"Sender", "Bezugspunkt":(-0.15,0.0), "Rotationswinkel":0}],
                "Block":[{"Name":"Acrylblock1", "Typ":"Block", "Koordinaten":[(-0.1,-0.05),(-0.0757,0)], "Rotationswinkel":0, "Rotationsmittelpunkt":(-0.25,-0.08785), "Material":'Acrylglas',"Brechungsindex":1.57},
                         {"Name":"Acrylblock2", "Typ":"Block", "Koordinaten":[(-0.1,0.0),(-0.0757,0.05)], "Rotationswinkel":0,"Rotationsmittelpunkt":(0.25,-0.08785), "Material":'Acrylglas',"Brechungsindex":1.57},
                         {"Name":"Acrylblock3", "Typ":"Block", "Koordinaten":[(-0.0757,-0.05),(-0.0514,0)],"Rotationswinkel":0,"Rotationsmittelpunkt":(-0.025,0.06355), "Material":'Acrylglas',"Brechungsindex":1.57}]
                ,"Kreis":[]
                }
             
mich_inter = {"Spezialobjekte":[{"Name":"Sender", "Typ":"Sender", "Bezugspunkt":(-0.3,0.0), "Rotationswinkel":0}],
                "Block":[{"Name":"Alu-Blech_unten", "Typ":"Block", "Koordinaten":[(-0.105,-0.3015),(0.105,-0.30)], "Rotationswinkel":0, "Rotationsmittelpunkt":(0.0,-0.3), "Material":'Aluminium',"Brechungsindex":0},
                         {"Name":"Alu-Blech_rechts", "Typ":"Block", "Koordinaten":[(0.3,-0.105),(0.3015,0.105)], "Rotationswinkel":0,"Rotationsmittelpunkt":(0.3,0.0), "Material":'Aluminium',"Brechungsindex":0},
                         {"Name":"Hartfaserplatte", "Typ":"Block", "Koordinaten":[(0.0,-0.105),(0.0025,0.105)],"Rotationswinkel":45,"Rotationsmittelpunkt":(0.0,0.0), "Material":'Hartfaserplatte',"Brechungsindex":1.58}]
                ,"Kreis":[]
                }

#with open('Standard-Geometrie.json', 'w') as json_file:
#  json.dump(standard_geo, json_file,indent=3)
  
#with open('Doppelspalt.json', 'w') as json_file:
 # json.dump(double_split, json_file,indent=3)
  
#with open('Acrylglas.json', 'w') as json_file:
 # json.dump(acryl, json_file,indent=3)
  
#with open('Michelson-Interferometer.json', 'w') as json_file:
 # json.dump(mich_inter, json_file,indent=3)



def draw_geometry(maxh):
    
    cf, mesh = Geo.drawGeo(maxh,pm.geodomain)
    if mesh == None:
        return
    with dp.outputdraw:
        dp.outputdraw.clear_output()
        Draw(cf,mesh,js_code=on_init)
        #Draw(cf=cf, mesh=mesh)

    return



def solveWave(maxh,degree, wave=1000):
    """ Solve the wave equation
            Args: wave  (double)
                refraction_blocks (double): =10 for reflection
                                    =1.5 for glass
                                    =1 for air
            mesh (NGSmesh)"""
    def solvenow2(btn):
        with dp.output3:
            dp.output3.clear_output()
            print("test a")
    def solvenow(btn):
        with dp.output3:
            dp.output3.clear_output()
            print("Die Gleichung wird gelöst. Bitte warten...")
        print("Die Gleichung wird gelöst. Bitte warten...")
        display(dp.output3)
        btn.disabled = True
        a.Assemble()
        f.Assemble()

        res = uscat.vec.CreateVector()
        res.data = f.vec - a.mat * uscat.vec
        uscat.vec.data += a.mat.Inverse(freedofs=fes.FreeDofs(), inverse="sparsecholesky") * res
        with dp.output3:
            dp.output3.clear_output()
            print("Die Gleichung wurde gelöst:")
            #try:
            #    Draw(uscat,Geo.ngmesh,min=-0.2,max=0.2,js_code=on_init,animate=True,settings={ "Complex": { "phase": 0.0, "animate": True, "speed": 2 }, "deformation" : 0.02  })
            #except:
            Draw(uscat,Geo.ngmesh,min=-0.2,max=0.2,js_code=on_init,animate=True,
                 interpolate_multidim=True, autoscale=False,
                 settings={"Objects": {"Wireframe": False}, "Complex": {"animate": True, "speed": 1.0, "phase" : 0.25}, "deformation" : 0.1}
                )
        pm.gridfct = uscat
        btn.disabled = False
        return
        
    if Geo.current_sender == None:
        display(Javascript(pm.error_sender2))
        return

    Geo.drawGeo(maxh,pm.geodomain)



    alpha_d = {"mat1" : 1, "mat2" : 1}
    alpha_d.update(Geo.refraction)
    m_fac = CoefficientFunction([alpha_d[mat] for mat in Geo.ngmesh.GetMaterials()])
    wavelength=wave
    wave = 2*pi/wave
    k = wave * m_fac
    uin = exp (-1J*k*x)

    fes = H1(Geo.ngmesh, complex=True, order=degree, dirichlet="scatterer|electric")
    u = fes.TrialFunction()
    v = fes.TestFunction()

    
    c = 1.5
    #if Geo.maxh/degree*wave > c:
        #display(Javascript(pm.resolution))
    

    uscat = GridFunction (fes)
    uscat.Set (uin, definedon=Geo.ngmesh.Boundaries("scatterer"))

    a = BilinearForm (fes, symmetric=True)
    a += SymbolicBFI (grad(u)*grad(v) )
    a += SymbolicBFI (-k*k*u*v)

    f = LinearForm (fes)
    with dp.output3:
        dp.output3.clear_output()
        if fes.ndof>600000:
            print("Das zu lösende Problem hat mehr als 600.000 Freiheitsgrade. \nAbhängig von den vorhandenen Ressourcen könnte dies zu viel sein.")
        elif fes.ndof>300000:
            print("Das zu lösende Problem hat mehr als 300.000 Freiheitsgrade. \nDas Lösen mag einige Sekunden dauern.")

        if Geo.maxh/degree*wave > c:
            print("Die Auflösung ist schlecht. Vor der Auswertung bitte Polynomgrad erhöhen oder Gitterbreite oder Wellenzahl verringern.")
        else:
            print("Die Auflösung ist angemessen.")
        print("\nAnzahl der Freiheitsgrade:",fes.ndof,"\nAuflösung: ~",wavelength*degree/Geo.maxh, "Punkte in jede Richtung pro Welle")
        
    btn = Button(description='Gleichung lösen')
    btn.layout=dp.layout_button
    btn.disabled = False
    display(dp.output3,btn)
    btn.on_click(solvenow)

    
    return 

def layout_switch():
    #return interactive(dp.make_mobile,{'Mobile layout': True})
    box = Checkbox(pm.isMobile, description='Portrait layout (mobile mode)')
    #return interact(dp.make_mobile,mobile=False)

    def changed(b):
        if b["new"] == False or b["new"] == True:
            dp.make_mobile(b["new"])

    box.observe(changed)
    return box

### function to start interactive options
def start(radius_pml=0.4,materialstärke_sender=0.0025):

    ## create the domain geometry and set passed parameters
    pm.current_rpml = pm.scale_domain*radius_pml
    pm.radius_outer = pm.scale_domain*radius_pml*1.4
    pm.geodomain = Geo(radius_pml,pm.radius_outer)
    pm.mat_thickness=materialstärke_sender

    ##
    dp.init_slider()
    
            
    ## generate mesh for the first run    
    dp.load_geo('Doppelspalt.json')
    draw_geometry(maxh=0.05)

    ## run functions interactively and show all required sliders
    todo = interactive(dp.show_slider,value=dp.slider_todo)
    draw = interactive(draw_geometry,{'manual': True, 'manual_name':'Geometrie zeichnen'},maxh=dp.slider_maxh)
    printall = interactive(dp.print2,{'manual': True, 'manual_name':'Objekte ausführlich anzeigen'})

    ## slider display and values
    todo.layout.height='45px'
    draw.children[1].layout=dp.layout_button_left      
    printall.children[-2].layout=dp.layout_button_left

    #draw.children[1].on_click(clear_geo) ## delete first mesh
    
    leftSliders = VBox([todo,dp.num_obj,printall,dp.dummy_btn,draw.children[0],draw.children[1],dp.dummy_btn,dp.output])
    if pm.isMobile:
        menu = VBox(children=[leftSliders, dp.new_ob, dp.change_ob,dp.remove_ob, dp.remove_all, dp.load,dp.save])
    else:
        menu = HBox(children=[leftSliders, dp.new_ob, dp.change_ob,dp.remove_ob, dp.remove_all, dp.load,dp.save])
    allSliders = VBox([dp.outputdraw,menu,dp.output2])
    

    
    return allSliders  


def solve_pde():
    ## call interactive function to solve the wave equation
    solve = interactive(solveWave,{'manual': True, 'manual_name':'Parameter prüfen'},maxh=dp.slider_maxh2,degree=dp.slider_degree,wave=dp.slider_wave)
    if Geo.maxh != None:
        dp.slider_maxh.value=Geo.maxh
    solve.children[-2].layout=dp.layout_button

    box=VBox([solve.children[0],solve.children[1],solve.children[2],solve.children[3],solve.children[-1]])
    
    return box



def evaluate():
    ## call interactive function to evaluate the wave equation
    def show_boxes(*args):
        box_p.layout.visibility = "hidden"
        box_p.layout.width = "0%"
        box_l.layout.visibility = "hidden"
        box_l.layout.width = "0%"
        box_c.layout.visibility = "hidden"
        box_c.layout.width = "0%"
        
        if pm.isMobile:
        	box_p.layout.height = "1px"
        	box_l.layout.height = "1px"
        	box_c.layout.height = "1px"
        else:
        	box_p.layout.height = "100%"
        	box_l.layout.height = "100%"
        	box_c.layout.height = "100%"

        if dp.slider_evaluate.value =='Punkt':
            box_p.layout.visibility = "visible"
            if pm.isMobile:
            	box_p.layout.height = "100%"
            	box_p.layout.width = "50%"
            else:
            	box_p.layout.width = "50%"
            dp.x2.value=0
            dp.y2.value=0
            dp.rad.value=0.1
            dp.angle1.value=0
            dp.angle2.value=180
            
        elif dp.slider_evaluate.value =='Gerade':
            box_l.layout.visibility = "visible"
            if pm.isMobile:
            	box_l.layout.height = "100%"
            	box_l.layout.width = "50%"
            else:
            	box_l.layout.width = "50%"
            dp.rad.value=0.1
            dp.angle1.value=0
            dp.angle2.value=180

        elif dp.slider_evaluate.value =='Kreisbogen':
            box_c.layout.visibility = "visible"
            if pm.isMobile:
            	box_c.layout.height = "100%"
            	box_c.layout.width = "50%"
            else:
           		box_c.layout.width = "50%"
            dp.x2.value=0
            dp.y2.value=0
        else:
            return
        
    
    def evaluation(value,x1,y1,rad,x2,y2,angle1,angle2):
        theta = np.linspace(0, 2*np.pi, 100)
        radius = 0.3
        rpmlx = pm.current_rpml*np.cos(theta)
        rpmly = pm.current_rpml*np.sin(theta)
        outerx = pm.radius_outer*np.cos(theta)
        outery = pm.radius_outer*np.sin(theta)
        figure, axes = plt.subplots(1,figsize=(5,5))
        axes.plot(rpmlx, rpmly, label="pml-radius")
        axes.plot(outerx, outery,label="outer-radius")
        
        axes.set_aspect(1)
        
        if value =='Punkt':
            with dp.outputplot:
                dp.outputplot.clear_output()
                plt.plot(x1,y1,'ob', label="Auswertungspunkt")
                plt.legend(bbox_to_anchor=(1.05, 1))
                plt.show()
            with dp.outputplt:
                dp.outputplt.clear_output()
                print("Realteil:\t", pm.gridfct(x1,y1).real)
                print("Imaginärteil:\t",pm.gridfct(x1,y1).imag)
                print("Norm:\t\t",abs(pm.gridfct(x1,y1)))
  
        elif value =='Gerade':
            with dp.outputplot:
                dp.outputplot.clear_output()
                plt.plot([x1,x2],[y1,y2],'b-',label="Auswertungsgerade")
                plt.plot(x1,y1,'xb', label="Startpunkt")
                plt.plot(x2,y2,'og', label="Endpunkt")
                plt.annotate("Start", (x1,y1))
                plt.annotate("End", (x2,y2))
                plt.legend(bbox_to_anchor=(1.05, 1))
                plt.show()
            if x1==x2 and y1==y2:
                with dp.outputplt:
                    dp.outputplt.clear_output()
                    print("Realteil:\t", pm.gridfct(x1,y1).real)
                    print("Imaginärteil:\t",pm.gridfct(x1,y1).imag)
                    print("Norm:\t\t",abs(pm.gridfct(x1,y1)))

                return

            length = sqrt((x1-x2)**2+(y1-y2)**2)
            steps = length*1000
            x = []
            real_list = []
            imag_list = []
            abs_list = []
            listx = []
            listy =[]
            pntx=x1
            pnty=y1
            
            for i in range(int(steps)+1):
                pntx = x1 + i/steps *(x2-x1)
                pnty = y1 + i/steps *(y2-y1)
                listx.append(pntx)
                listy.append(pnty)
                x.append(100*i/(int(steps)))
                try:
                    val = pm.gridfct(pntx,pnty)
                    real_list.append(val.real)
                    imag_list.append(val.imag)
                    abs_list.append(abs(val)) 
                except :
                    val = np.nan 
                    real_list.append(val)
                    imag_list.append(val)
                    abs_list.append(val)
                    
            fig2 = plt.figure(figsize=(14,10))
            ax1 = fig2.add_subplot(111)
            ax1.plot(x,real_list, label='Real')
            #ax1.plot(x,imag_list, label='Imaginärteil')
            ax1.plot(x,abs_list, label='Norm')
            ax1.set_xlim(left=x[0],right=x[-1])
            #plt.setp(ax1.get_xticklabels(),visible=False)
            ax1.set_ylabel("Wellengleichung")
            
            ax3 = ax1.twiny()
            ax3.xaxis.set_ticks_position('bottom') # set the position of the second x-axis to bottom
            ax3.xaxis.set_label_position('bottom') # set the position of the second x-axis to bottom
            ax3.spines['bottom'].set_position(('outward', 0))
            ax3.set_xlim(left=listx[0],right=listx[-1])
            if listx[0]==listx[-1]:
                ax3.set_xticks(np.array([-0.05,1.0]))
                ax3.set_xticklabels([listx[0],listx[-1]])
            ax3.set_xlabel('x-Koordinate')

            ax2 = ax1.twiny()
            ax2.xaxis.set_ticks_position('bottom') # set the position of the second x-axis to bottom
            ax2.xaxis.set_label_position('bottom') # set the position of the second x-axis to bottom
            ax2.spines['bottom'].set_position(('outward', 36))
            ax2.set_xlim(left=listy[0],right=listy[-1])
            if listy[0]==listy[-1]:
                ax2.set_xticks(np.array([-0.05,1.0]))
                ax2.set_xticklabels([listy[0],listy[-1]])
            ax2.set_xlabel('y-Koordinate')
            
            ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.setp(ax1.get_xticklabels(),visible=False)       ##invisible values of percentage scaling
            ax1.tick_params(axis='x', which='both', length=0)   ##invisible ticks of percentage scaling
            data = np.array([listx,listy,real_list,imag_list,abs_list])
            with dp.outputplt:
                dp.outputplt.clear_output()
                print("Die betrachtete Gerade hat eine Länge von ca {:.1f} Millimetern.".format(length*1000,1))
                plt.show()
            c='   '
            np.savetxt('data.csv', data.T, delimiter="   ", fmt='%10.4f', header=c+"x"+4*c+"y"+4*c+"real"+3*c+"imag"+3*c+"abs")
            data =""
            with open("data.csv", 'r') as file:
                data = file.read().replace('.', ',')
            with open("data.csv", 'w') as outfile:
                outfile.write(data)

            
        elif value =='Kreisbogen':
            with dp.outputplot:
                dp.outputplot.clear_output()
                if angle1==angle2:
                    circlesec = mpatches.Arc(xy=(x1,y1),width=2*rad,height=2*rad,theta1=angle1,theta2=angle2+360)
                else:
                    circlesec = mpatches.Arc(xy=(x1,y1),width=2*rad,height=2*rad,theta1=angle1,theta2=angle2)
                circlesec.set_label("Kreisbogen")
                axes.add_patch(circlesec)
                plt.plot(x1+rad*cos(radians(angle1)),y1+rad*sin(radians(angle1)),'xb',label="Startpunkt")
                plt.plot(x1+rad*cos(radians(angle2)),y1+rad*sin(radians(angle2)),'og',label="Endpunkt")
                
                    
                plt.annotate("Start", (x1+rad*cos(radians(angle1)),y1+rad*sin(radians(angle1)) ))
                plt.annotate("End", (x1+rad*cos(radians(angle2)),y1+rad*sin(radians(angle2))) )
                plt.legend(bbox_to_anchor=(1.05, 1))
                plt.show()

            #check if object is inside the domain
            if (sqrt(x1**2+y1**2)+rad >= pm.radius_outer):
                display(Javascript(pm.warning_outside2))
            
            start = angle1
            end = angle2
            angular_range=end-start
            if start > end:
                angular_range=360-start+end
            if start == end:
                angular_range = 360
            
            length = pi*2*rad*angular_range/360
            steps = length*1000
            real_list = []
            imag_list = []
            abs_list = []
            angle_list=[]
            x = []
            listx = []
            listy =[]
            for i in range(int(steps)+1):
                pntx = x1 + rad * cos(radians(start+i/steps*length*360/(2*pi*rad)))
                pnty = y1 + rad * sin(radians(start+i/steps*length*360/(2*pi*rad)))
                x.append(100*i/(int(steps)))
                listx.append(pntx)
                listy.append(pnty)
                if ((start+i/steps*length*360/(2*pi*rad))>=360):
                    angle_list.append(int(start+i/steps*length*360/(2*pi*rad))-360)
                else:
                    angle_list.append(int(start+i/steps*length*360/(2*pi*rad)))
                try:
                    val = pm.gridfct(pntx,pnty)
                    real_list.append(val.real)
                    imag_list.append(val.imag)
                    abs_list.append(abs(val)) 
                except :
                    val = np.nan 
                    real_list.append(val)
                    imag_list.append(val)
                    abs_list.append(val)
            
            fig2 = plt.figure(figsize=(14,10))
            ax1 = fig2.add_subplot(111)
            ax1.set_ylabel("Wellengleichung")
            ax1.plot(x,real_list, label='Real')
            #ax1.plot(x,imag_list, label='Imaginärteil')
            ax1.plot(x,abs_list, label='Norm')
            ax1.set_xlim(left=x[0],right=x[-1])
            

            ax2 = ax1.twiny()
            ax2.xaxis.set_ticks_position('bottom') # set the position of the second x-axis to bottom
            ax2.xaxis.set_label_position('bottom') # set the position of the second x-axis to bottom
            ax2.spines['bottom'].set_position(('outward', 0))
            
            len1 = len(angle_list)
            if start < end:
                ax2.set_xlim(left=angle_list[0],right=end)
            else:
                ax2.set_xlim(left=start-360,right=end)
            ax2.set_xlabel('Winkel')
            
            
            ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.setp(ax1.get_xticklabels(),visible=False)  #invisble labels of percentage scalign
            ax1.tick_params(axis='x', which='both', length=0)  #invisible ticks of percentage scaling
            
            data = np.array([listx,listy,real_list,imag_list,abs_list])
            with dp.outputplt:
                dp.outputplt.clear_output()
                print("Der betrachtete Kreisbogen hat eine Länge von ca {:.1f} Millimetern.".format(length*1000,1))
                plt.show()
            c='   '
            np.savetxt('data.csv', data.T, delimiter="   ", fmt='%10.4f', header=c+"x"+4*c+"y"+4*c+"real"+3*c+"imag"+3*c+"abs")
            data =""
            with open("data.csv", 'r') as file:
                data = file.read().replace('.', ',')
            with open("data.csv", 'w') as outfile:
                outfile.write(data)
        else:
            return
            
        return 

    box_p=VBox([dp.x1,dp.y1])
    box_l=VBox([dp.x1,dp.y1,dp.x2,dp.y2])
    #box_angle =HBox([dp.angle,dp.show_angle1,dp.show_angle2])
    box_c=VBox([dp.x1,dp.y1,dp.rad,dp.angle1,dp.angle2])
    
    box_p.layout.visibility = "hidden"
    box_p.layout.width = "0%"
    box_l.layout.visibility = "hidden"
    box_l.layout.width = "0%"
    box_c.layout.visibility = "hidden"
    box_c.layout.width = "0%"
   
    eva = interactive(evaluation, {'manual': True, 'manual_name':'Auswertung starten'},value=dp.slider_evaluate,x1=dp.x1,y1=dp.y1,x2=dp.x2,y2=dp.y2,rad=dp.rad,angle1=dp.angle1,angle2=dp.angle2)
    eva.children[-2].layout=dp.layout_button_left
    
    dp.slider_evaluate.observe(show_boxes, 'value')
    #dp.angle.observe(dp.angle_area, 'value')
    vbox=VBox([eva.children[0],eva.children[-2],dp.outputplot])
    if pm.isMobile:
        hbox=VBox([vbox,box_p,box_l,box_c])
    else:
        hbox=HBox([vbox,box_p,box_l,box_c])
    display(hbox)
    display(dp.outputplt)
    #display(eva.children[-1])
    

    return


