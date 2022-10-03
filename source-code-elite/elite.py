# Elite
import pgzrun, math, pygame, numpy

angle1 = 90
angle2 = 90
xview = 0
yview = 6
zview = 250

def draw():
    screen.blit("background", (90, 5))
    drawShip(700, angle1, angle2, 1000)
    
def update():
    global angle1,angle2
    angle1 += 0.6
    angle2 += 1
        
def initViewTransform(rho, theta, phi):
    global va,vb,ve,vf,vg,vi,vj,vk,vl
    sintheta = math.sin(math.radians(theta))
    costheta = math.cos(math.radians(theta))
    sinphi = math.sin(math.radians(phi))
    cosphi = math.cos(math.radians(phi))
    va = -sintheta
    vb = costheta
    ve = -costheta*cosphi
    vf = -sintheta*cosphi
    vg = sinphi
    vi = -costheta*sinphi
    vj = -sintheta*sinphi
    vk = -cosphi
    vl = rho
    
def viewTransform(x,y,z):
    xe = va*x + vb*y
    ye = ve*x + vf*y + vg*z
    ze = vi*x + vj*y + vk*z + vl
    return (xe,ye,ze)

def perspectiveTransform(xyz,d):
    return ((d*xyz[0]/xyz[2])+400, (d*xyz[1]/xyz[2])+230)
    
def drawShip(rho, theta, phi, d):
    verts = [(32,0,76),(-32,0,76), (0,26,24), (-120,-3,-8),
             (120,-3,-8), (-88,16,-40), (88,16,-40), (128,-8,-40),
             (-128,-8,-40), (0,26,-40), (-32,-24,-40), (32,-24,-40),
             (-36,8,-40), (-8,12,-40), (8,12,-40), (36,8,-40),
             (36,-12,-40), (8,-16,-40), (-8,-16,-40), (-36,-12,-40),
             (0,0,76), (0,0,90), (-80,-6,-40), (-80,6,-40),
             (-88,0,-40), (80,6,-40), (88,0,-40), (80,-6,-40)]
    faces = [[1,2,0,20,21,20],[1,5,2],[6,0,2],[1,3,5],[4,0,6],[5,9,2],[9,6,2],
             [3,8,5],[7,4,6],[7,6,9,5,8,10,11],[8,3,1,10],[0,11,10,1,20,21,20],
             [7,11,0,4],[18,13,12,19],[17,16,15,14],[22,23,24],[27,26,25]]
    initViewTransform(rho, theta, phi)
    spoints = []
    vpoints = []
    for v in range(0, len(verts)):
        tpoints = viewTransform(verts[v][0],verts[v][1],verts[v][2])
        vpoints.append(tpoints) 
        spoints.append(perspectiveTransform(tpoints,d))
    fOrder = getFacesDrawOrder(faces,vpoints)
    for fo in reversed(range(0,len(faces))):
        f = fOrder[fo]
        vp0 = vpoints[faces[f][0]]
        vp1 = vpoints[faces[f][1]]
        vp2 = vpoints[faces[f][2]]
        vect1 = []
        vect2 = []
        for i in range(0,3):
            vect1.append(vp1[i] - vp0[i])
            vect2.append(vp2[i] - vp0[i])
        n = getNormalVector(vect1,vect2)
        los = [xview-vpoints[faces[f][0]][0],yview-vpoints[faces[f][0]][1],zview-vpoints[faces[f][0]][2]]
        vis = n[0]*los[0]+n[1]*los[1]+n[2]*los[2]
        fpoints = []
        for v in range(0,len(faces[f])):
            v1 = v-1
            if v1 < 0 : v1 = len(faces[f])-1
            cv1 = faces[f][v-1]
            sx1 = spoints[cv1][0]
            sy1 = spoints[cv1][1]
            cv2 = faces[f][v]
            sx2 = spoints[cv2][0]
            sy2 = spoints[cv2][1]
            fpoints.append(spoints[cv1])
        if vis > 0:
            pygame.draw.polygon(screen.surface,(0,0,0),fpoints)
            pygame.draw.polygon(screen.surface,(255,255,255),fpoints,3)    

def getFacesDrawOrder(fl, vp):
    favz = []
    for f in range(0,len(fl)):
        favz.append(getMostZ(fl[f],vp))
    forder = numpy.argsort(favz)
    return forder

def getNormalVector(a,b):
    x = a[1]*b[2] - b[1]*a[2]
    y = a[2]*b[0] - b[2]*a[0]
    z = a[0]*b[1] - b[0]*a[1]
    nv = [x,y,z]
    return nv

def getMostZ(flist,vlist):
    a = 0 
    for i in flist:
        vz = vlist[i][2]
        if a < vz: a=vz
    return a

pgzrun.go()
