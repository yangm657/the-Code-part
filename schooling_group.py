

from tkinter import *
from random import *
import math
import time
import numpy as np

RUNNING = False

wait_for_start = False
with_predator = False
with_predator = True
with_leader = True

# If true view will always follow predator
TRACK_PREDATOR = False
# If false will track the (weighted) centroid of all boids.

#Defining canvas variables
width = 1400
height = 900
#width = 800
#height = 500

background = "cyan"
canvas = None
window = None

frame_pause = 0

## Counter for the main loop
## Now done with local variable
##cycles = 0

#Defining boid variables
initialNumBoids = 40
numBoids = initialNumBoids
## Stop when num boids goes down to this value:
numBoidsStop = 20
## Stop when num cycles gets up to this value:
numCyclesStop = 50000

head_radius = 10
tail_radius = 5
boids = []
dead_boids = []
initial_velocity_range = 4

window = Tk()

max_speed = IntVar()
max_speed.set(4)
## the initial speed for biods


predator_max_speed = IntVar()
predator_max_speed.set(5)          
## the speed for predator

predator_accel = 5

## Prey fix flee when closer to predator than this:
flee_dist = IntVar()
flee_dist.set(300)

selfish_dist = IntVar()
selfish_dist.set(900)

#Defining rule strengths
#boid-boid attraction
boid_boid_attraction_threshold = IntVar()
boid_boid_attraction_threshold.set(2000)
#(10000000000)
#(2000)

#cohesion
boid_boid_attraction_strength = DoubleVar()
boid_boid_attraction_strength.set(0.6)


## Repulsion
boid_boid_repulsion_threshold = IntVar()
boid_boid_repulsion_threshold.set(150)

boid_boid_repulsion_strength = DoubleVar()
boid_boid_repulsion_strength.set(2)

## selfish
boid_selfish_strength=DoubleVar()
boid_selfish_strength.set(2)

##leadership
boid_leadership_strength=DoubleVar()
boid_leadership_strength.set(2)

## Align velocities
boid_boid_alignment_threshold = IntVar()
boid_boid_alignment_threshold.set(200)

boid_boid_alignment_strength = DoubleVar()
boid_boid_alignment_strength.set(0.3)
#boid_boid_alignment_strength = 0

rand_strength = DoubleVar()
rand_strength.set(0.2)

# attraction to food
boid_food_attraction_strength = DoubleVar()
boid_food_attraction_strength.set(1) ## attraction to food

# the second food2
boid_food2_attraction_strength = DoubleVar()
boid_food2_attraction_strength.set(0) ## attraction to food

## sepcial
special_individual_boid_attraction_strength = boid_boid_attraction_strength.get()
special_individual_boid_alignment_strength = 0.3
special_individual_boid_repulsion_strength = 2
special_individual_max_speed = max_speed.get()
speical_selfish_strength = boid_selfish_strength.get()




food = None
predator = None
x_offset = 0
y_offset = 0

boid_count = 0 ## counter to give each boid an id
gauge_panel = None


def main():
    global boids, food, gauge_panel, RUNNING, food2, boids, dead_boids, numBoids, cycles
    num_tests = 50
    create_window()
    for x in range(10):
      attraction_str = 0 + x*0.2
      global RR
      RR = 255
      global GG
      GG = 255
      global BB
      BB = 255

      RR = RR - x*15
      GG = GG - x*25
      BB = BB - x*25
      #change of color
      
      boid_boid_attraction_strength.set(attraction_str)
      print( "Testing average cycles for attraction strength", attraction_str)
      tot_cycles = 0
      standard_cycles = []
      for n in range(num_tests):
        initialise()

        if not wait_for_start:
            cycles = main_loop()
            print( "Number of cycles run:", cycles )
            print("\n")
            standard_cycles.append(cycles)
            tot_cycles += cycles 
      print( "Av cycles for attraction strength", attraction_str,
              "is", int(tot_cycles/num_tests) )
      standard = np.std(standard_cycles,  ddof=1)
      print("standard diviation is ",standard )


def initialise():
    global boids, numBoids, food, predator, gauge_panel, canvas, cycles, RUNNING, food2
    RUNNING = False
    cycles = 0
    canvas.delete(ALL)
    boids = []
    deadBoids = []
    numBoids = initialNumBoids
    buildBoids()
    initialise_boid_count_and_separations()
    food = Food()
    food2 = Food()
    

    if with_predator:
       predator = Predator()
    gauge_panel = GaugePanel()
    ##仪表板


def run_loop():
    global food, predator, gauge_panel, RUNNING, food2
    if not wait_for_start:
        cycles = main_loop()
        print( "Number of cycles run:", cycles )
    

def main_loop():
    global food, gauge_panel, RUNNING, food2, boids, dead_boids, numBoids, cycles
    cycles = 0
    abc=[]
    if RUNNING:
        return # don't run a second loop
    else:
         RUNNING = True
    #Loop to continuously draw boid and update its position.
    for n in range( numCyclesStop ):
        if not RUNNING:
            return cycles
        cycles += 1
        
        if with_predator:
           calculate_predator_boid_separations()
           #do_predation()
           survivors = []
           dead_boids=[]
           for i in range( len(boids) ):
               if predator_boid_separations[i] > 30:
                   survivors.append(boids[i] )
                   
               else:
                   numBoids -= 1
                   dead_boids.append( boids[i] )
                   if boids[0] in dead_boids:
                       abc.append(cycles)
                       print("the leader1 dead using ", abc[0])
                   #if boids[5] in dead_boids:
                       #abc.append(cycles)
                      # print("the leader1 dead using ", abc[0])
                       

           boids = survivors

           
           for b in dead_boids:
               b.delete_graphic()
               #if b.id == 0:
                   #gauge_panel.update(cycles)
                   #canvas.update()
                   #return cycles
                   
               
               
           if  (numBoids > numBoidsStop):
              predator.move()
        if (numBoids > numBoidsStop):
            
               
            food.draw()
            food2.draw()
            food.move()
            food2.move()
            calculate_boid_separations()
            moveBoids()
            moveBoidGraphics()
            gauge_panel.update(cycles)
            canvas.update()
            time.sleep(frame_pause)            
            
        else:
          canvas.create_text( 300, 30, text= "All but " +str(numBoidsStop) +
                              " little fish have been eaten :(", fill='red' )
          gauge_panel.update(cycles)
          canvas.update()
          return cycles
    canvas.create_text( 300, 30, text= "Maximum Cycles Limit Reached", fill='red' )
    gauge_panel.update(cycles)
    canvas.update()
   
    return cycles
        

def initialise_boid_count_and_separations():
    global boid_count, boid_separations, predator_boid_separations
    boid_count = 0
    boid_separations = [[ 0  for x in range(numBoids)] for x in range(numBoids)] 
    predator_boid_separations = [0 for x in range(numBoids)]


class GaugePanel:
    def __init__(self):
       self.x_offset_gauge = canvas.create_text(20,20, anchor="w", text='x_offset = 0')
       self.y_offset_gauge = canvas.create_text(20,40, anchor="w", text='y_offset = 0')
       self.cycles_gauge   = canvas.create_text(20,60, anchor="w", text='cycles = 0')
       self.numBoids_gauge = canvas.create_text(20,80, anchor="w", text='numBoids = ' + str(int(numBoids)))
      
    def update(self, cycles):
        canvas.itemconfig( self.x_offset_gauge, text='x_offset = ' + str(int(x_offset)))
        canvas.itemconfig( self.y_offset_gauge, text='y_offset = ' + str(int(y_offset)))
        canvas.itemconfig( self.cycles_gauge,   text='cycles = ' +   str(int(cycles)))    
        canvas.itemconfig( self.numBoids_gauge, text='numBoids = ' + str(int(numBoids)))


def create_window():
    global window, canvas
    global boid_boid_attraction_strength
    global boid_boid_attraction_threshold
    global boid_boid_repulsion_strength
    global boid_boid_repulsion_threshold
    global boid_selfish_strength
    global boid_leadership_strength
    canvas = Canvas(window, width = width, height = height, background = background)
    window.title('Boids - FYP - George Smithson')
    canvas.update()
    canvas.pack()
    slider_panel = Frame(window)
    make_gauge_widget( slider_panel,  "\nSpeed", max_speed, 0, 20, 1)
    make_gauge_widget( slider_panel,  "Attraction\nStrength", boid_boid_attraction_strength, 0, 3, 0.1)
    make_gauge_widget( slider_panel,  "Attract\nThreshold", boid_boid_attraction_threshold, 0, 5000, 5)
    make_gauge_widget( slider_panel,  "Repel\nStrength", boid_boid_repulsion_strength, 0, 8, 0.1)
    make_gauge_widget( slider_panel,  "Repel\nThreshold", boid_boid_repulsion_threshold, 0, 1000, 5)
    make_gauge_widget( slider_panel,  "Align\nStrength", boid_boid_alignment_strength, 0, 3, 0.1 )
    make_gauge_widget( slider_panel, "Align\nThreshold", boid_boid_alignment_threshold, 0, 2000, 5 )
    make_gauge_widget( slider_panel, "Food\nAttraction", boid_food_attraction_strength, 0, 5, 0.1 )
    make_gauge_widget( slider_panel, "Food2\nAttraction", boid_food2_attraction_strength, 0, 5, 0.1 )
    make_gauge_widget( slider_panel, "Random\nMovement", rand_strength, 0, 3, 0.1)
    make_gauge_widget( slider_panel,  "Selfish\nStrength", boid_selfish_strength, 0, 6, 0.5)
    make_gauge_widget( slider_panel,  "Leadership\nStrength", boid_leadership_strength, 0, 6, 0.5)

    make_gauge_widget( slider_panel, "Predator\nSpeed", predator_max_speed, 0, 20, 1 )
    make_gauge_widget( slider_panel, "Flee\nDistance", flee_dist, 0, 500, 1 )

    start_button = Button( slider_panel, text="START", height=4, command=main_loop )
    reset_button = Button( slider_panel, text="Reset", height=3, command=initialise )
   
    start_button.pack()
    reset_button.pack()
    slider_panel.pack()


def make_gauge_widget( panel, name, var, start, end, res ):
    frame = Frame(panel)
    label = Label( frame, text=name )
    slider = Scale( frame, from_=start, to=end, resolution=res, variable=var )
    label.pack()
    slider.pack()
    frame.pack(side=LEFT)
    

            

def do_predation():
    global boids, dead_boids, numBoids, cycles
    survivors = []
  
    for i in range( len(boids) ):
        if predator_boid_separations[i] > 30:
            ##the distance that predator could eat biods
            survivors.append(boids[i] )
        else:
            numBoids -= 1
            dead_boids.append( boids[i] )
            #print(dead_boids)
            #if boids[0] in dead_boids:
                #print("the dead is ")
                #abc.append(cycles)
                #print(abc)
                
    #boids = survivors
    #for b in dead_boids:
        #b.delete_graphic()
#        for i in b.graphic:
#            canvas.delete(i)

def leader():
    global boids, dead_boids, numBoids
    for i in range(len(boids)):
        if predator_boid_separations[i] < 30 and i == 0 :
            print("a") 

   
def sprite_list_centroid( sprite_list ):
    cx, cy = 0, 0
    for sprite in sprite_list:
        cx += sprite.x
        cy += sprite.y
    num = len(sprite_list)
    return( (cx/num, cy/num) )


def adjusted_boids_centroid():
    cx, cy = 0, 0
    for boid in boids:
        cx += boid.x
        cy += boid.y
    numDead = len(dead_boids)
    if with_predator:
       cx += predator.xpos * (numDead+1)
       cy += predator.ypos * (numDead+1)
    total = numBoids + numDead + 1
    return( (cx/total, cy/total) )
    #return( predator.xpos, predator.ypos )
    
def moveBoidGraphics():
    #print("*** running moveBoidGraphics")
    global x_offset, y_offset    
    if TRACK_PREDATOR:
        cx = predator.xpos
        cy = predator.ypos
    else:
        cx, cy = adjusted_boids_centroid()
    x_offset = width/2 - cx
    y_offset = height/2 - cy
    for boid in boids:
        boid.move_graphic(x_offset, y_offset)
        
def moveBoids():
    #print("*** running moveBoids")
    #Runs a method to get new velocity and moves it to new position.
    for boid in boids:
        boid.moveToNewPos()

def buildBoids():
    #Builds a list of length (numBoids) containing created instances of Boid class.
    global boids
    boids = [Boid() for boid in range(numBoids)]
 

def add_vectors( vectors ):
    if len( vectors ) == 1:
        return vectors[0]
    (v1, v2) = vectors[0]
    ##print("vectors =", vectors )
    (r1, r2) = add_vectors(vectors[1:])
    return( v1+r1, v2+r2 )

def vector_magnitude( vect ):
    x, y = vect
    return( math.sqrt( x**2 + y**2 ) )

def scale_vector_to_magnitude( vect, mag ):
    if vect == (0,0):
        return (0,0)
    vectm = vector_magnitude( vect )
    x, y = vect
    return( x * mag/vectm, y * mag/vectm )
    

def limit_vector_to_magnitude( vect, mag_limit ):
    mag = vector_magnitude( vect )
    if mag > mag_limit:
        return scale_vector_to_magnitude( vect, mag_limit )
    return vect

def rotate_point_by_angle_around_point( p, angle, cent ):
    x, y = p
    cx, cy = cent
    rx = cx + (x-cx) * math.cos(angle) - ((y-cy) * math.sin(angle))
    ry = cy + (x-cx) * math.sin(angle) + ((y-cy) * math.cos(angle))
    return( rx, ry )

def rotate_point_list_by_angle_around_point( points, ang, cent ):
    if points == []:
        return[]
    rest = rotate_point_list_by_angle_around_point( points[2:], ang, cent )
    x, y = rotate_point_by_angle_around_point( (points[0],points[1]), ang, cent )
    return( [x, y] + rest )

def offset_point_list( p, plist ):
    if plist == []:
        return []
    x, y = p
    lx, ly = plist[0], plist[1]
    return( [x + lx, y + ly] + offset_point_list( p, plist[2:] ) )

def calculate_boid_separations():
    global boid_separations
    for nb1 in range(numBoids):
        for nb2 in range( nb1 +1, numBoids ):
             sep = point_separation( boids[nb1].position(), boids[nb2].position() )
             boid_separations[nb1][nb2] = sep
             boid_separations[nb2][nb1] = sep
## 此函数计算任意两个boid之间距离（勾股定理）
             
def calculate_predator_boid_separations():
    global predator_boid_separations
    for nb in range(numBoids):
        sep = point_separation( (predator.xpos, predator.ypos), boids[nb].position() )
        predator_boid_separations[nb] = sep
        
             
def point_separation( p1, p2 ):
    x1, y1 = p1
    x2, y2 = p2
    return( math.sqrt( (x1 - x2)**2 + (y1-y2)**2 ) )
 
def point_separation_squared( p1, p2 ):
    x1, y1 = p1
    x2, y2 = p2
    return(  (x1 - x2)**2 + (y1-y2)**2 ) 
    
def nearest_boid_to_point( p ):
    x, y = p
    nearest_so_far = boids[0]
    #print( nearest_so_far )
    nearest_dist_so_far = point_separation_squared( p, nearest_so_far.position() )
    for b in boids[1:]:
        dist = point_separation_squared( p, b.position() )
        if dist < nearest_dist_so_far:
            nearest_dist_so_far = dist
            nearest_so_far = b
    return nearest_so_far

def nearest_boid_to_boid( p ):
    x, y = p
    nearest_boids = boids[0]
    if p != nearest_boids.position():
        nearst_dist_boids = point_separation_squared( p, nearest_boids.position() )
        for b in boids[1:]:
            dist = point_separation_squared( p, b.position() )
            if dist < nearst_dist_boids and dist!=0 and point_separation_squared != 0 :
                nearst_dist_boids = dist
                nearest_boids = b
    else:
        nearest_boids = boids[1]
        nearst_dist_boids = point_separation_squared( p, nearest_boids.position() )
        for b in boids[2:]:
            dist = point_separation_squared( p, b.position() )
            if dist < nearst_dist_boids and dist!=0 and point_separation_squared != 0 :
                nearst_dist_boids = dist
                nearest_boids = b
    return nearest_boids

def color_string_from_rbg_ranges( r, g, b ):
    r1, r2 = r
    g1, g2 = g
    b1, b2 = b
    return( "#" + ("00"+ hex(randint(r1,r2))[2:])[-2:] 
                + ("00"+ hex(randint(g1,g2))[2:])[-2:]     
                + ("00"+ hex(randint(b1,b2))[2:])[-2:] )
 
class StickyGraphic:
  
  def __init__(self, x,y,head_radius,bod_len_x,bod_len_y,tail_radius,hcol,bcol,tcol):
      self.hr = head_radius
      self.tr = tail_radius
      self.head = canvas.create_oval(int(x-self.hr),int(y-self.hr),
                                     int(x+self.hr),int(y+self.hr),
                                     outline='black',fill=hcol, 
                                     activefill='red',width=1)   
      self.body = canvas.create_line(int(x), int(y),
                           int(x-bod_len_x), int(y-bod_len_y),
                           width=5, fill=bcol)
      self.tail = canvas.create_oval( int(x-bod_len_x -self.tr), int(y-bod_len_y -self.tr),
                              int(x-bod_len_x +self.tr), int(y-bod_len_y +self.tr),
                              outline='black',fill=tcol,activefill='red',width=1 )

  def delete_graphic(self):
          print( "Running StickyGraphic.delete_graphic()" )
          canvas.coords( self.head, 100, 100, 150, 150 )
          canvas.delete(self.head)
          canvas.delete(self.body)
          canvas.delete(self.tail)
          canvas.update()
                              
  def move(self, x,y,bod_len_x, bod_len_y):
        x += x_offset
        y += y_offset
        canvas.coords( self.head, int(x-self.hr),int(y-self.hr),
                                     int(x+self.hr),int(y+self.hr) )   
        canvas.coords(self.body, int(x), int(y),
                                 int(x-bod_len_x), int(y-bod_len_y) )
        canvas.coords( self.tail, int(x-bod_len_x -self.tr), int(y-bod_len_y -self.tr),
                                  int(x-bod_len_x +self.tr), int(y-bod_len_y +self.tr) )
      



class Predator:
    def __init__(self):
        self.head_radius = 30
        self.tail_radius = 15
        ## Starts in Fixed Position
        self.xpos = -500
        #-500
        self.ypos =height/2
        #height/2
        self.vx = 2
        self.vy = 2
        self.graphic = StickyGraphic(self.xpos,self.ypos, self.head_radius, self.vx*7, self.vy*7,
                                     self.tail_radius, 'red', 'red', 'red' )

                                          
    
    def move(self):
        self.xpos += self.vx
        self.ypos += self.vy
        target = nearest_boid_to_point( (self.xpos, self.ypos) )
        #catch the most nearst fish
        target_vector = (target.x-self.xpos, 
                         target.y-self.ypos)
        velocity_change = scale_vector_to_magnitude(target_vector, predator_accel)
        self.vx += velocity_change[0]
        self.vy += velocity_change[1]
        self.vx, self.vy = limit_vector_to_magnitude((self.vx,self.vy), predator_max_speed.get())
        self.graphic.move(self.xpos, self.ypos, self.vx*7, self.vy*7)

        
        
        
class Food:
    def __init__(self):
        self.xpos = 1000
        self.ypos = 2000
        self.angle = 0
        self.rotation = 0
        #self.geom = [-20,-20, 0,-30, 20,-20, 20,20, 10, -15, -10, -15]
        self.geom = [ randint(-15,15) for x in range(14)]
        offcoords = offset_point_list( (self.xpos, self.ypos), self.geom )
        self.graphic = canvas.create_polygon( *offcoords,
                               outline = "black", fill = 'green' )
        self.centre_tag = canvas.create_text(self.xpos,self.ypos, text='X')

        

    def draw(self):
        rot_coords = rotate_point_list_by_angle_around_point( self.geom, self.angle,
                                                             (0,0) )
        #rot_coords = self.geom                                                  
        offset_coords = offset_point_list( (self.xpos + x_offset, self.ypos + y_offset), rot_coords )
        canvas.coords( self.graphic, *offset_coords )
        canvas.coords( self.centre_tag, self.xpos+x_offset, self.ypos+y_offset)
        canvas.update()
                               
    def move(self):
        move_mag = 5
        max_dev = 50
        self.rotation += uniform( -0.01, 0.01 )
        if self.rotation > 0.1:
            self.rotation = 0.1
        if self.rotation < -0.1:
            self.rotation = -0.1     
        self.angle += self.rotation
        self.xpos += uniform(-move_mag, move_mag)
        self.ypos += uniform(-move_mag, move_mag)
        for n in  range(len( self.geom )):
            self.geom[n] = self.geom[n] + uniform(-3,+3)
            if self.geom[n] > max_dev:
                self.geom[n] = max_dev
            if self.geom[n] < - max_dev:
                self.geom[n] = - max_dev
        
                               
#------------------------------------------------------------------------------------

class Boid:
    #The Boid class contains the rules regarding how the boids move
    #and react to each other.

    def __init__(self):
        global boid_count
        self.id = boid_count
        boid_count += 1
        #Sets up inital velocity vector, and position to a random x,y space on the canvas.
        self.vx = uniform(-initial_velocity_range,initial_velocity_range)
        self.vy = uniform(-initial_velocity_range,initial_velocity_range)
        self.x = randint(0,width)
        self.y = randint(0,height)
        self.velocity = (self.vx, self.vy)
        #self.position = (self.px, self.py)
        #print('Initial velocity = ', self.velocity )
        self.graphic = self.make_graphic()
        #print( "Created boid:", self )


    def __repr__(self):
        return "boid{}:coords({},{}),vel({},{})".format(self.id, self.x, self.y, self.vx, self.vy )
        
    def position(self):
        return(self.x, self.y)

    def make_graphic(self):
        
         XX = int(boid_boid_attraction_strength.get()*100)
         x=255-XX
         y=255-XX
         z=255-XX
         if self.id == 0:
             head_color = color_string_from_rbg_ranges( (255,255),(0,0), (0,0 ) )
         else:
              if x == -5 or x == -15:
                  head_color = color_string_from_rbg_ranges( (0,0),(0,0), (0,0) )
              else:     
                  head_color = color_string_from_rbg_ranges( (x,x),(y,y), (z,z) )
         tail_color = color_string_from_rbg_ranges( (200,255),(50,120), (50,120) )
         x, y = self.x, self.y
         vx, vy = self.velocity[0], self.velocity[1]
         head = canvas.create_oval(int(x-head_radius),int(y-head_radius),
                           int(x+head_radius),int(y+head_radius),
                           outline='black',fill=head_color, 
                           activefill='red',width=1)
         body = canvas.create_line(int(x), int(y),
                           int(x-vx*5), int(y-vy*5),
                           width=5)
         tail = canvas.create_oval( int(x-vx*5 -tail_radius), int(y-vy*5 -tail_radius),
                                    int(x-vx*5 +tail_radius), int(y-vy*5 +tail_radius),
                           outline='black',fill=tail_color,activefill='red',width=1)
         idtag = canvas.create_text(x,y, text=self.id)
         return( (head,body,tail,idtag) )

    def delete_graphic(self):
        for i in self.graphic:
            canvas.delete(i)

    def move_graphic(self, x_offset, y_offset):
        ## print( "move_graphic", self, x_offset, y_offset)
        x, y = self.x+x_offset, self.y+y_offset
        vx, vy = self.velocity[0], self.velocity[1]
        box, boy = scale_vector_to_magnitude( self.velocity, head_radius)
        canvas.coords( self.graphic[0], int(x-head_radius),int(y-head_radius),
                                        int(x+head_radius),int(y+head_radius) )
        canvas.coords( self.graphic[1], int(x-box),int(y-boy), int(x - vx*5), int(y - vy*5) )
        canvas.coords( self.graphic[2], int(x - vx*5 -tail_radius), int(y - vy*5 -tail_radius),
                                        int(x - vx*5 +tail_radius), int(y - vy*5 +tail_radius) )
        canvas.coords( self.graphic[3], int(x), int(y))

    def separation(self, boid):
        ## print( self.id, boid.id )
        ## print("***", self.id, boid.id )
        return( boid_separations[self.id][boid.id] )

        
    def moveToNewPos(self):
        
        #This function applies the three different rules to calculate
        #then update the velocity of the boids.
        #for boid in boids:
            self.x, self.y = add_vectors([self.position(), self.velocity] )
            #(vect1, vect2, vect3) = ((0,0), (0,0), (0,0))
            vect1 = self.boid_boid_attraction()
            vect2 = self.boid_boid_repulsion()
            vect3 = self.boid_boid_velocity_alignment()
            vect4 = self.boid_random_velocity_change()
            vect5 = self.boid_food_attraction()
            vect6 = self.boid_food2_attraction()## food2
            #newvel = add_vectors([self.velocity, vect1, vect2, vect3, vect4, vect5, vect6])
            if self.id == 0:
                newvel = add_vectors([self.velocity, vect1, vect2, vect4, vect5, vect6])
            else:
                newvel = add_vectors([self.velocity, vect1, vect2, vect3, vect4, vect5, vect6])
            if with_predator:                  
                    newvel = add_vectors( [newvel, self.boid_predator_repulsion(),self.boid_boid_selfish()])
            if with_leader:
                    newvel = add_vectors( [newvel,  self.boid_boid_leader(),self.boid_boid_selfish()])   
            #print("Unlimited velocity =", newvel)
            if self.id == 0:
      
                max_sp = max_speed.get()
            else:
                max_sp = max_speed.get()
            self.velocity = limit_vector_to_magnitude( newvel, max_sp )
            #print("New velocity =", self.velocity)
    
    def boid_boid_leader(self):
        cx = 0
        cy = 0
        for  boid in boids:
            if ((boid.id == 0) and (not boid is self) and (self.separation(boid) < 1500)):
                cx = boid.x 
                cy = boid.y 
        dx = cx - self.x
        dy = cy - self.y
        leader_strength = boid_leadership_strength.get()
        return scale_vector_to_magnitude( (dx,dy), 
                                           leader_strength)
    
    def boid_boid_attraction(self):
        #Cohesion - Move boid towards percieved center mass of neighbours
        cx = 0
        cy = 0
        num_neighbours = 0
        for boid in boids:
            if ( (not boid is self) and 
                 (self.separation(boid) < 1000)
               ):
                cx += boid.x
                cy += boid.y
                num_neighbours += 1
        if num_neighbours == 0:
            return (0,0)
        cx /= num_neighbours
        cy /= num_neighbours
        dx = cx - self.x
        dy = cy - self.y
        if self.id == 0:
            attraction = special_individual_boid_attraction_strength
            ##attraction = special_individual_boid_attraction_strength
        else:
            attraction = boid_boid_attraction_strength.get()
        return scale_vector_to_magnitude( (dx,dy), 
                                          attraction )
        

    def boid_boid_repulsion(self):
        #Seperation - don't go too close to other boids
        tot_vx, tot_vy = (0,0)
        if self.id == 0:
            #repulsion = boid_boid_repulsion_strength.get()
            repulsion = special_individual_boid_repulsion_strength
        else:
            repulsion = boid_boid_repulsion_strength.get()
        for boid in boids:
            if not (boid is self):
                ss = self.separation(boid)
                #sssqrt = math.sqrt(ss)
                ##sssq = ss*ss
                if ss < boid_boid_repulsion_threshold.get(): #norm to get magnitude of vector
                    vx = self.x -boid.x 
                    vy = self.y -boid.y
                    svx, svy = scale_vector_to_magnitude( (vx,vy),
                                              (1- ss/boid_boid_repulsion_threshold.get())
                                               * repulsion
                                             )
                    tot_vx += svx
                    tot_vy += svy
        #print("boid_boid_repulsion =", (tot_vx, tot_vy))
        return (tot_vx, tot_vy)  
        
    
    def boid_boid_velocity_alignment(self):
        #Alignment - align with average velogity of flock

        tot_vx, tot_vy = (0,0)
        svx, svy = (self.velocity[0], self.velocity[1])
        if self.id == 0:
            alignment = special_individual_boid_alignment_strength
        else:
            alignment = boid_boid_alignment_strength.get()
        for boid in boids:
            if not (boid is self):
                ss = self.separation(boid)
                if ss < boid_boid_alignment_threshold.get():
                   dvx = boid.velocity[0] - svx
                   dvy = boid.velocity[1] - svy
                   sdvx, sdvy = scale_vector_to_magnitude( (dvx,dvy),
                                                  (1 - ss/boid_boid_alignment_threshold.get())
                                                  * alignment )
                   tot_vx += sdvx
                   tot_vy += sdvy
        return( (tot_vx, tot_vy) )


    def boid_random_velocity_change(self): ## Random velocity change
        rs = rand_strength.get()
        return( ( uniform(-rs, rs ),
                  uniform(-rs, rs )
              ) )

    def boid_food_attraction(self): ## Attraction to food
        
        if self.id == 0:
            dx = food.xpos - self.x
            dy = food.ypos - self.y
            food_attraction = scale_vector_to_magnitude( (dx,dy),
                                                     boid_food_attraction_strength.get() )
        else:
            food_dis = point_separation((food.xpos, food.ypos),self.position())
            if food_dis<1500:
                
                dx = food.xpos - self.x
                dy = food.ypos - self.y
                food_attraction = scale_vector_to_magnitude( (dx,dy),
                                                     boid_food_attraction_strength.get() )
            else:
                return (0,0)
        ##print( "food_attraction =", food_attraction )
        return food_attraction
    
    ##the food2_attraction
    def boid_food2_attraction(self): ## Attraction to food2
        dx = food2.xpos - self.x
        dy = food2.ypos - self.y
        food2_attraction = scale_vector_to_magnitude( (dx,dy),
                                                     boid_food2_attraction_strength.get() )
        ##print( "food2_attraction =", food2_attraction )
        return food2_attraction

        
    def boid_predator_repulsion(self): ## Repulsion from predator
        pred_dist = point_separation((predator.xpos,predator.ypos),self.position())
        if self.id == 0:	
            if pred_dist < flee_dist.get()+100:
                sep_vect = ( self.x-predator.xpos, self.y-predator.ypos)
                return scale_vector_to_magnitude( sep_vect, max_speed.get())
        else:
            if pred_dist < flee_dist.get():	
                sep_vect = ( self.x-predator.xpos, self.y-predator.ypos)
                return scale_vector_to_magnitude( sep_vect, max_speed.get())
        return (0,0)
    
    def boid_boid_selfish(self):
        pred_dist = point_separation((predator.xpos,predator.ypos),self.position())
        if pred_dist < selfish_dist.get():
            target = nearest_boid_to_boid((self.x, self.y))
            similar_line_x = target.x-predator.xpos
            similar_line_y = target.y-predator.ypos
            similar_hypotenuse = point_separation( (predator.xpos,predator.ypos), target.position())
            fix_dis = 300
            x_po = (fix_dis*similar_line_x)/similar_hypotenuse + target.x 
            y_po = (fix_dis*similar_line_y)/similar_hypotenuse + target.y
            sep_vect = (  x_po - self.x, y_po - self.y)
            #sep_vect = (  self.x - x_po, self.y - y_po )
            if self.id == 5:
                selfish = speical_selfish_strength
            else:
                selfish = boid_selfish_strength.get()               
            
            return scale_vector_to_magnitude( sep_vect, selfish )
        return (0,0)

#------------------------------------------------------------------------------------
#If being used by self, run main.         
if __name__ == "__main__":
    main()
    pass 
