from math import pi,sqrt
import parameter as pm

from ngsolve import *
from ngsolve.webgui import Draw

from netgen.geom2d import SplineGeometry
from netgen.geom2d import CSG2d, Circle, Rectangle
from netgen.geom2d import EdgeInfo as EI, PointInfo as PI, Solid2d

from IPython.display import display, Javascript



class Geo:

    def __init__(self, rpml, router):
        self.rpml = rpml
        self.router = router

    
    
    allobjects = []
    allnames = []
    allmaterial = {'Luft':[],'Wasser':[],'Fensterglas':[],'Reflektion':[],'Prisma': [], 'Wachslinse':[], 'Senderantenne':[],'Perfekt elektrisch (Dirichlet)':[],'Leitend (Neumann)':[]}
    refraction = {}
    current_sender = None

    
    current_rpml = pm.scale_domain*0.1
    ngmesh = None
    maxh = None
    

    def drawGeo(maxh,domain):
        """Generate the mesh that is displayed with Netgen

            Args:
                maxh (Float): changeable mesh size (slider)
                domain (Geo object): fixed parameter of the domain for radius and PML-radius
                

            adding all objects to CSGGeometry"""

        
        
        Geo.current_rpml = domain.rpml
        Geo.maxh = maxh
        geo = CSG2d()
        #geo = SplineGeometry()


        #boundaries of domain
        c_pml = Circle( center=(0, 0), radius=domain.rpml, mat="mat1")
        c_outer= Circle( center=(0, 0), radius=domain.router, mat="mat2")

        domain1 = c_pml
        geo.Add(c_outer-c_pml)

        if Geo.current_sender != None:
            
            x = Geo.current_sender["Mittelpunkt"][0]-pm.scale_sender*0.065
            y = Geo.current_sender["Mittelpunkt"][1]
            sender = Solid2d([(x-pm.scale_sender*pm.mat_thickness,y-pm.scale_sender*0.009),
                              EI(bc="electric"),
                              (x,y-pm.scale_sender*0.009),
                              EI(bc="scatterer"),
                             (x,y+pm.scale_sender*0.009),
                              EI(bc="electric"),
                             (x-pm.scale_sender*pm.mat_thickness,y+pm.scale_sender*0.009),
                              EI(bc="electric")],mat="Außerhalb")
            
            sender_arm1 = Solid2d([(x,y-pm.scale_sender*0.009),
                          (x+pm.scale_sender*0.13,y-pm.scale_sender*0.04),
                          (x+pm.scale_sender*0.13,y-pm.scale_sender*(0.04+pm.mat_thickness)),
                          (x,y-pm.scale_sender*(0.009+pm.mat_thickness))],mat="Senderantenne")
            sender_arm2 = Solid2d([(x,y+pm.scale_sender*0.009),
                         (x+pm.scale_sender*0.13,y+pm.scale_sender*0.04),
                         (x+pm.scale_sender*0.13,y+pm.scale_sender*(0.04+pm.mat_thickness)),
                         (x,y+pm.scale_sender*(0.009+pm.mat_thickness))],mat="Senderantenne")
            if Geo.current_sender["Rotationswinkel"] !=0:
                sender.Rotate(Geo.current_sender["Rotationswinkel"],center=(x+pm.scale_sender*0.065,y))
                sender_arm1.Rotate(Geo.current_sender["Rotationswinkel"],center=(x,y))
                sender_arm2.Rotate(Geo.current_sender["Rotationswinkel"],center=(x,y))

            
            domain1 = domain1-sender-sender_arm1-sender_arm2
            geo.Add(sender_arm1)
            geo.Add(sender_arm2)


        for material in Geo.refraction :
            cnt = 0
            for i in Geo.allmaterial[material]:
                if i["Typ"] == "Block":
                    if material == 'Leitend (Neumann)':
                        obj = Rectangle( pmin=i["Koordinaten"][0], pmax=i["Koordinaten"][1], mat=i["Material"],bc="conductive")
                    elif material == 'Perfekt elektrisch (Dirichlet)':
                        obj = Rectangle( pmin=i["Koordinaten"][0], pmax=i["Koordinaten"][1], mat=i["Material"],bc="electric")
                    else:
                        obj = Rectangle( pmin=i["Koordinaten"][0], pmax=i["Koordinaten"][1], mat=i["Material"])
                        
                    if i["Rotationswinkel"] != 0:
                        obj.Rotate(i["Rotationswinkel"],center=i["Mittelpunkt"])
                    if cnt == 0:
                        domain_mat = obj
                        cnt = 1
                    else:
                        domain_mat += obj
                        
                elif i["Typ"] == "Kreis":
                    if material == 'Leitend (Neumann)':
                        obj = Circle( center=i["Mittelpunkt"], radius=i["Radius"], mat=i["Material"],bc="conductive")
                    elif material == 'Perfekt elektrisch (Dirichlet)':
                        obj = Circle( center=i["Mittelpunkt"], radius=i["Radius"], mat=i["Material"],bc="electric")
                    else:
                        obj = Circle( center=i["Mittelpunkt"], radius=i["Radius"], mat=i["Material"])
                    
                    #if i["Rotationswinkel"] != 0:
                     #   obj.Rotate(i["Rotationswinkel"],center=i["Mittelpunkt"])
                    if cnt == 0:
                        domain_mat = obj
                        cnt = 1
                    else:
                        domain_mat += obj
                        
                elif i["Typ"] == "Wachslinse":
                    x = i["Mittelpunkt"][0]
                    y = i["Mittelpunkt"][1]
                    obj = Solid2d([(x-pm.scale_lens*0.135,y-pm.scale_lens*0.012),
                                  (x+pm.scale_lens*0.135,y-pm.scale_lens*0.012),
                                  (x+pm.scale_lens*0.135,y),
                                   EI((x+pm.scale_lens*0.0675,y+pm.scale_lens*0.031)),
                                   (x,y+pm.scale_lens*0.031),
                                  EI((x-pm.scale_lens*0.0675,y+pm.scale_lens*0.031)),
                                  (x-pm.scale_lens*0.135,y)],mat=i["Material"])
                    if i["Rotationswinkel"] != 0:
                        obj.Rotate(i["Rotationswinkel"],center=i["Rotationsmittelpunkt"])
                    if cnt == 0:
                        domain_mat = obj
                        cnt = 1
                    else:
                        domain_mat += obj
                        
                elif i["Typ"] == "Prisma":
                    x = i["Mittelpunkt"][0]
                    y = i["Mittelpunkt"][1]
                    obj = Solid2d([(x-pm.scale_prism*0.21/2,y-pm.scale_prism*sqrt(3)/4*0.21),
                                    (x+pm.scale_prism*0.21/2,y-pm.scale_prism*sqrt(3)/4*0.21),
                                    (x,y+pm.scale_prism*sqrt(3)/4*0.21)],mat=i["Material"])
                    if i["Rotationswinkel"] != 0:
                        obj.Rotate(i["Rotationswinkel"],center=i["Mittelpunkt"])
                    if cnt == 0:
                        domain_mat = obj
                        cnt = 1
                    else:
                        domain_mat += obj
                        
                else:
                    return
                    
           

            if cnt == 1:
                if material == 'Perfekt elektrisch (Dirichlet)' or material == 'Leitend (Neumann)':
                    domain1 = domain1-domain_mat
                else:
                    domain1 = domain1-domain_mat
                    geo.Add(domain_mat)
        Geo.refraction["Senderantenne"]=50
        geo.Add(domain1) 
        ngmesh = geo.GenerateMesh(maxh=maxh)
    
        ngmesh = Mesh(ngmesh)
        ngmesh.SetPML(pml.Radial(origin=(0,0), rad=domain.rpml, alpha=0.1j), "mat2")
        ngmesh.Curve(3)
        cf = ngmesh.RegionCF(VOL, dict(mat1=3, mat2=7))
        Geo.ngmesh = ngmesh
        
        return cf, ngmesh

        

    def sender(typ,name,x,y,rotation,update=False):
        """ Determine parameters for sender geometry
            check if position and overlapping of the object
            save valid object

            Args:
                typ (String) : what kind of a special object
                name (String): name of the sender
                x (Float): x-coordinate of senders midpoint
                y (Float): y-coordinate of senders midpoint
                rotation (Int) : angle between 0° and 360°
                update (Boolean): False, if new sender is created
                        True, if we update existing sender

            -dimensions of sender: width of 0.02 in x-direction and width of 0.06 in y-direction
            -only one sender is allowed
            -save sender in global class variable Geo.current_sender

            Returns: None
            """

        
        # measurements of the sender/prism/lens
        if typ == "Sender":
            point1 = (x-pm.scale_sender*0.0025, y-pm.scale_sender*0.04)
            point2 = (x+pm.scale_sender*0.13, y+pm.scale_sender*0.04)
            mat = "sender"
            refrac = -1
            x += pm.scale_sender*0.065
            rad = pm.scale_sender*sqrt(0.065**2+0.04**2)
        elif typ == "Prisma":
            point1 = (x-pm.scale_prism*0.21/sqrt(3),y-pm.scale_prism*0.21/sqrt(3))
            point2 = (x+pm.scale_prism*0.21/sqrt(3),y+pm.scale_prism*0.21/sqrt(3))
            mat = "Prisma"
            refrac = 1.65
            rad = pm.scale_prism*0.21/sqrt(3)
        else:
            point1 = (x-pm.scale_lens*0.0215,y-pm.scale_lens*0.135)
            point2 = (x+pm.scale_lens*0.0215,y+pm.scale_lens*0.135)
            mat = "Wachslinse"
            refrac = 1.57
            rad = pm.scale_lens * sqrt(0.135**2+0.031**2)

                
        # check if there exists a sender
        ### if no: check if position is possible without overlappings
        ##### if yes: save new sender
        

        if update == True:
            if Geo.overlapping(name,x,y,rad,refrac):
                for i in Geo.allobjects:
                    if i["Name"] == name:
                        i["Mittelpunkt"]=(x,y)
                        i["Rotationswinkel"]=rotation
                        if i["Typ"]=="Sender":
                            Geo.current_sender = i
                        display(Javascript(pm.changed))
                        return
            
            
        elif Geo.current_sender != None and typ == "Sender":
            display(Javascript(pm.error_sender))
            return
        else:
            if Geo.overlapping(name,x,y,rad,refrac) and Geo.same_name(name):
                Geo.allnames.append(name)
                obj = {"Name":name,"Typ":typ,"Mittelpunkt":(x,y),"Radius":rad,"Rotationswinkel":rotation,"Material":mat, "Brechungsindex":refrac}
                if typ == "Sender":
                    Geo.current_sender = obj
                    #Geo.refraction["Senderantenne"]=50
                else:
                    Geo.allmaterial[mat].append(obj)
                    Geo.refraction[mat]=refrac
                Geo.allobjects.append(obj)
                
        return

    

    def block(name,x,y,rotation,rotx,roty,mat,refrac,update=False):
        """ Determine parameters for block geometry
            check if position and overlapping of the object
            save valid object
            
            Args:
                name (String): name of the block
                x (Float,Float): tuple (x1,x2) of x-coordinates for vertices of block
                y (Float,Float): tuple (y1,y2) of y-coordinates for vertices of block
                rotation (Int) : angle between 0° and 360°
                material: String describing the material, in Geo.refraction corresponding refraction parameter of the material
                update (Boolean): False, if new block is created
                        True, if we update existing block

            save all block parameters
                in global list allobjects, and
                according to its material in global list of the material

            Returns: None
            """

        # measurements of the block 
        x1,x2 = x
        y1,y2 = y
        point1 = (x1, y1)
        point2 = (x2, y2)


        if mat == None:
            display(Javascript(pm.error_missing))
            return
        if mat == "freier Parameter":
            mat = name
            Geo.allmaterial[mat]=[]
        if mat == "Außerhalb":
            if refrac == None:
                display(Javascript(pm.error_missing))
                return
            elif refrac == -2:
                mat = 'Perfekt elektrisch (Dirichlet)'
            else:
                mat = 'Leitend (Neumann)'
            refrac =None
        

        
        # measurements for overlapping and rotation
        m1 = (x2+x1)/2
        m2 = (y1+y2)/2
        if m1==rotx and m2==roty:
            rad = sqrt((x2-x1)**2+(y2-y1)**2)/2
        else:
            max_x=max(abs(rotx-x1),abs(x2-rotx))
            max_y=max(abs(roty-y1),abs(y2-roty))
            rad = sqrt(max_x**2+max_y**2)

        # check if we want to update an existing block,
        ### if yes: check if position is possible without overlappings
        ##### if yes: update new parameters
        
        if update == True:
            if Geo.overlapping(name,m1,m2,rad,refrac):
                for i in Geo.allobjects:
                    if name == i["Name"]:
                        i["Koordinaten"] = [point1,point2]
                        i["Mittelpunkt"] = (m1,m2)
                        i["Radius"] = rad
                        i["Rotationswinkel"] = rotation
                        i["Rotationsmittelpunkt"] = (rotx,roty)
                        if refrac != i["Brechungsindex"]:
                            if i["Material"] != name:
                                Geo.allmaterial[i["Material"]].remove(i)    #delete from list of old material
                            i["Material"] = mat
                            i["Brechungsindex"] = refrac
                            Geo.allmaterial[mat].append(i)      #insert in list of the new material
                            Geo.refraction[mat] = refrac

                        display(Javascript(pm.changed))
                        
                        return
            

                
        # check if position is possible without overlappings
        ### if yes: add new block
        
        else:
            if Geo.overlapping(name,m1,m2,rad,refrac) and Geo.same_name(name):
                b = {"Name":name,"Typ":"Block","Koordinaten":[point1,point2],"Mittelpunkt":(m1,m2),"Radius":rad,"Rotationswinkel":rotation,"Rotationsmittelpunkt":(rotx,roty),"Material":mat,"Brechungsindex":refrac}
                Geo.allnames.append(name)
                Geo.allobjects.append(b)
                Geo.allmaterial[mat].append(b)
                Geo.refraction[mat]=refrac


        return


    def circle(name,x,y,rad,mat,refrac,update=False):
        """ Determine parameters for circle geometry
            check if position and overlapping of the object
            save valid object

            Args:
                name (String): name of the block
                x (Float): x-coordinates of circle midpoint
                y (Float): y-coordinates of circle midpoint
                rad (Float): radius of circle
                rotation (Int) : angle between 0° and 360°
                material: String describing the material, in Geo.refraction corresponding refraction parameter of the material
                update (Boolean): False, if new circle is created
                                  True, if we update existing cirle

            save all circle parameters
                in global list allobjects, and
                according to its material in global list of the material

            Returns: None
            """
        if mat == None:
            display(Javascript(pm.error_missing))
            return
        if mat == "freier Parameter":
            mat = name
            Geo.allmaterial[mat]=[]
        if mat == "Außerhalb":
            if refrac == None:
                display(Javascript(pm.error_missing))
                return
            elif refrac == -2:
                mat = 'Perfekt elektrisch (Dirichlet)'
            else:
                mat = 'Leitend (Neumann)'
            refrac =None

        
        
        # check if we want to update an existing block,
        ### if yes: check if position is possible without overlappings
        ##### if yes: update new parameters

        if update == True:
            if Geo.overlapping(name,m1,m2,rad,refrac):
                for i in Geo.allobjects:
                    if name == i["Name"]:
                        i["Mittelpunkt"] = (x,y)
                        i["Radius"] = rad
                        if refrac != i["Brechungsindex"]:
                            if i["Material"] != name:
                                Geo.allmaterial[i["Material"]].remove(i)    #delete from list of old material
                            i["Material"] = mat
                            i["Brechungsindex"] = refrac
                            Geo.allmaterial[mat].append(i)      #insert in list of the new material
                            Geo.refraction[mat] = refrac

                        display(Javascript(pm.error_changed))
                        
                        return


        # check if position is possible without overlappings
        ### if yes: add new circle

        else:
            if Geo.overlapping(name,x,y,rad,refrac) and Geo.same_name(name):
                c = {"Name":name,"Typ":"Kreis","Mittelpunkt":(x,y),"Radius":rad,"Material":mat,"Brechungsindex":refrac}
                Geo.allnames.append(name)
                Geo.allobjects.append(c)
                Geo.allmaterial[mat].append(c)
                Geo.refraction[mat]=refrac
            
        return



    def same_name(name):
        """Check if an object with the same name exists
            Args:
                name (String): name of the object
                
            Returns:
                Boolean: True, if object is allowed
                         False, if same name, outside of domain or overlapping"""
        
        if name in Geo.allnames:
            display(Javascript(pm.error_name))
            return False
        
        return True

    
    def overlapping(name,x,y,rad,refrac):
        """ Check if object is positioned inside the PML-Circle, and
            check if object overlaps with other objects
                if same material: overlapping is ok

            Args:
                name (String): name of the object
                x (Float): x coordinate of midpoint
                y (Float): y coordinate of midpoint
                rad (Float): minimal radius so that object is completely contained in circle
                material: same materials can overlap
                update (Boolean): if True, remove object before overlapping check
                
            Returns:
                Boolean: True, if object is allowed
                         False, if same name, outside of domain or overlapping
        """


        #check if object is inside the domain
        if (sqrt(x**2+y**2)+rad >= Geo.current_rpml):
            display(Javascript(pm.warning_outside))
            return True
        

        #overlapping allowed if same material 
        #check position of all existing objects
        
        for i in Geo.allobjects:
            if  i["Brechungsindex"] != refrac and i["Name"] != name:
                if sqrt((x-i["Mittelpunkt"][0])**2+(y-i["Mittelpunkt"][1])**2)<(rad+i["Radius"]):
                    display(Javascript(pm.warning_overlap))     
                    return True
                

        return True

    
    def printObjects(everything):
        """ Function to print all existing objects

            Args:
                everything (Boolean): If True, print all parameters of the object
                                        (useful, if we want to change existing object)
                                     If False, print the type and the name of the object

            Returns: None"""
        
        
        print("Vorhandene Objekte:")
        if len(Geo.allobjects) == 0:
            print("Keine Objekte enthalten")
            return
        
        if everything == True: 
            for i in Geo.allobjects:
                print("Name\t\t\t ",i["Name"],"\nObjekttyp\t\t",i["Typ"],"\nMittelpunkt\t\t",i["Mittelpunkt"])
                print("Radius\t\t\t",i["Radius"])
                if i["Typ"] == 'Sender' or i["Typ"] == 'Prisma' or i["Typ"] == 'Wachslinse':
                    print("Rotationswinkel\t\t",i["Rotationswinkel"])
                if i["Typ"] == 'Block':
                    print("Eckpunkte\t\t", i["Koordinaten"])
                    print("Rotationswinkel\t\t",i["Rotationswinkel"],"\nRotationsmittelpunkt\t",i["Rotationsmittelpunkt"])
                print("Material\t\t",i["Material"], "\nBrechungsindex\t\t",i["Brechungsindex"],"\n")


        else:
            for i in Geo.allobjects:
                print("Objekt:     ", i["Name"], "\t vom Typ:     " ,i["Typ"])
           
        return









   
