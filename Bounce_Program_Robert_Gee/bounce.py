#!/usr/bin/python
from  particles import *
from pylab import *
from particleInitialize import *
import pygame
import sys, time
from PIL import Image as Image
import numpy


"""
    Hypothesis: The Brazil Nut effect is harder to visualize with larger containers. This could be
    because it takes longer to fill the empty spaces in the bottom of the container.

    Controls: Rotate with the w,a,s,d keys.
              Restart with larger container: q key.
              Restart with smaller container: e key.
"""

def read_texture(filename):
    img = Image.open(filename)
    img_data = numpy.array(list(img.getdata()), numpy.int8)
    textID  = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textID) # This is what's missing
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    return textID

# setting the size of the frame or specifying a region of an area
size = [800, 600]
width = 800
height = 600
screen = pygame.display.set_mode(size, DOUBLEBUF | OPENGL)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = [0, 0, 255]

glEnable(GL_DEPTH_TEST)

viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
glLoadIdentity()


sphere = gluNewQuadric() #Create new sphere

tex = read_texture('ball.jpg')
gluQuadricTexture(sphere, GL_TRUE)
glEnable(GL_TEXTURE_2D)


# This program is a 'driver' for a simple simulation of partilces in a box with
# periodic boundary conditions. Your objective will be to complete the code here
# so that you can 'see' the particles with OpenGL, or another library.

tStart = t0 = time.time()

dt = 0.1   # Time step taken by the time integration routine.
L = 10.    # Size of the box.
t = 0      # Initial time

# Particle update data:
COUNT = 1                    # Number of time steps computed
UPDATE_FRAMES = 2            # How often to redraw screen
ADD_PARTICLE_INTERVAL = 10   # How often to add a new particle

# How resolved are the spheres?
STACKS = 25
SLICES = 25

# Instantiate the forces function between particles
f = GranularMaterialForce()
# Create some particles and a box
p = Particles(L,f,periodicY=0)
particleInitialize(p,'one',L)
# Instantiate Integrator
integrate = VerletIntegrator(dt)

def init():
    pygame.init()

def draw():
    for i in range(p.N):
        glPushMatrix()
        global sphere
        #color = [255.0, 1.0, 2.0, 4.0]
        #glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
        glTranslatef(p.x[i], p.y[i], p.z[i]) #Move to the place
        glColor4f(255,255,0,255) #Put color
        gluSphere(sphere, p.r[i], 16, 8) #Draw sphere
        glPopMatrix()


def idle():
    global COUNT
    for i in range(UPDATE_FRAMES):
       integrate(f,p) # Move the system forward in time
       COUNT = COUNT + 1
       if mod(COUNT,ADD_PARTICLE_INTERVAL) == 0:
           # Syntax is addParticle(x,y,z,vx,vy,vz,radius)
           # Note y is into page.
           p.addParticle(.25*randn(),L,.25*randn(),0,0,0,.3*randn()+1.)
           f(p)  # Update forces

"""def key(k, x, y): #rotate frame around z.

def special(k, x, y): #roates

"""

def reshape(width, height):
    h = float(height)/float(width)
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-L/2*1.4, L/2*1.4, -L/2*1.4, L/2*1.4, -L, 3.0*L)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -L*2.0)
    screen = pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)

if __name__ == '__main__':

    # Open a window

    # Initialize

 done = False
 clock = pygame.time.Clock()
 init()

 q_pressed = False
 e_pressed = False

 while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.VIDEORESIZE:
            width, height = event.size

    keypress = pygame.key.get_pressed()

    # init model view matrix
    glLoadIdentity()

    # init the view matrix
    glPushMatrix()
    glLoadIdentity()

    # apply the movment
    if keypress[pygame.K_w]:
        glRotatef(20,1,0,0)
    if keypress[pygame.K_s]:
        glRotatef(-20,1,0,0)
    if keypress[pygame.K_d]:
        glRotatef(20,0,1,0)
    if keypress[pygame.K_a]:
        glRotatef(-20,0,1,0)

    if keypress[pygame.K_q]  and not q_pressed:
        L = L + 1
        p = Particles(L,f,periodicY=0)
        particleInitialize(p,'one',L)
        q_pressed = True
    if not keypress[pygame.K_q]:
        q_pressed = False


    if keypress[pygame.K_e] and not e_pressed:
        if L > 5:
            L = L - 1
            p = Particles(L,f,periodicY=0)
            particleInitialize(p,'one',L)
            e_pressed = True
    if not keypress[pygame.K_e]:
        e_pressed = False

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT) #Clear the screen
    glShadeModel(GL_SMOOTH)
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    lightZeroPosition = [10., 4., 50., 1.]
    lightZeroColor = [0.8, 1.0, 0.8, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
    glEnable(GL_LIGHT0)

    # multiply the current matrix by the get the new view matrix and store the final vie matrix
    glMultMatrixf(viewMatrix)
    viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

    # apply view matrix
    glPopMatrix()
    glMultMatrixf(viewMatrix)

    draw()

    L_string = "L: " + str(L)
    print(L_string)


    PN_string = "p.N: " + str(p.N)
    print(PN_string)
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[F")


    reshape(width,height)

    pygame.display.flip() #Update the screen
    pygame.time.wait(10)

    idle();
