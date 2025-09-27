
# https://github.com/Herator2/CG100-Micropython-Projects
# Made by Alex VDE :)

try: from utils import *
except:
    print("Failed to import core utility 'utils.py'\nPlease download from casio.alexvde.dev and place alongside this\n - Alex :)")
    quit()

# Config - Main
VERSION = "0.1.0r"

# Config - Points
BASIC_FRUIT_POINTS = 1
SPECIAL_FRUIT_POINTS = 5
N_FRUITS_AT_ONCE = 3

# Config - Appearance
BACKGROUND_COLOR = (255,255,255)  # SHOULD BE INVISIBLE - Used to limit performence
FRUIT_COLOR = (255,0,0)
SPECIAL_FRUIT_COLOR = (0,0,255)
SNAKE_HEAD_COLOR = (128, 255, 128)

# Config - Gameplay
AREA_LOCATION_X = 7
AREA_LOCATION_Y = 4
X2_WALL = 22
Y2_WALL = 11

class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def translate(self, x, y):
        self.x += x
        self.y += y

class Fruit:
    def __init__(self, position, score = BASIC_FRUIT_POINTS, color = FRUIT_COLOR):
        self.position = position
        self.score = score
        self.color = color

class Snake:
    def __init__(self):
        self.positions = [Vec2(10,10)]
        self.direction = ":)"
        self.to_spawn = 3
        
    def move(self):
        # Move head
        v = None
        if self.direction == "left": v = Vec2(-1,0)
        elif self.direction == "right": v = Vec2(1,0)
        elif self.direction == "up": v = Vec2(0,-1)
        elif self.direction == "down": v = Vec2(0,1)
        else:
            v = Vec2(0,0)
            return
        last_position = Vec2(self.positions[0].x, self.positions[0].y)
        self.positions[0].translate(v.x, v.y)
        # Follow Body
        for (i, p) in enumerate(self.positions[1:]):
            self.positions[i+1] = Vec2(last_position.x, last_position.y)
            last_position = p
        # Spawn new
        if self.to_spawn > 0:
            self.positions.append(last_position)
            self.to_spawn -= 1
            
    def is_colliding_with_wall(self, x1, x2, y1, y2):
        v = self.positions[0]
        return ((v.x < x1) or (v.x > x2) or (v.y <= y1) or (v.y > y2))
    
    def is_colliding_with_self(self):
        for p in self.positions[1:]:
            if p.x == self.positions[0].x:
                if p.y == self.positions[0].y:
                    return True
        return False
    
    def is_colliding_with_fruit(self, fruit):
        if self.positions[0].x == fruit.position.x:
            if self.positions[0].y == fruit.position.y:
                return True
        return False

splash_screen(VERSION)

# Game restarts from here
while True:
    # Main menu
    pos = 0
    current_key = 0
    while True:
        # Up and down
        if getkey() == 34 and getkey() != current_key: pos+=1
        elif getkey() == 14 and getkey() != current_key: pos-=1
        if pos < 0: pos = 2
        elif pos > 2: pos = 0
        current_key = getkey()
        
        # Select
        if getkey() == 24:
            if pos == 2: quit()
            elif pos == 1: pass
            else: break
        
        # Render
        clear_screen()
        draw_circle_circumference(20,48,5,3,(0,0,0))
        draw_circle_circumference(20,68,5,3,(0,0,0))
        draw_circle_circumference(20,88,5,3,(0,0,0))
        draw_string(20,15, "Snake or something")
        draw_string(40,40, "Play")
        draw_string(40,60, "Change Difficulty - TODO")
        draw_string(40,80, "Quit")
        if pos == 0: draw_circle_solid(20,48,3,(0,128,255))
        elif pos == 1: draw_circle_solid(20,68,3,(0,128,255))
        elif pos == 2: draw_circle_solid(20,88,3,(0,128,255))
        show_screen()
    
    # Startup
    s = Snake()
    fruits = []
    deathmethod = "none"
    score = 0

    # Ingame Loop
    while True:
        # Clear
        clear_screen()
        
        # Draw game board
        draw_rect(AREA_LOCATION_X, AREA_LOCATION_Y, AREA_LOCATION_X + (int((X2_WALL * 16) - (len(s.positions) * 16))), AREA_LOCATION_Y + (Y2_WALL * 1), BACKGROUND_COLOR)
        
        # Get input
        k = getkey()
        if s.direction in ":)":
            if k == 34: s.direction = "down"
            elif k == 14: s.direction = "up"
            elif k == 25: s.direction = "right"
            elif k == 23: s.direction = "left"
        elif s.direction in ["left", "right"]:
            if k == 34: s.direction = "down"
            elif k == 14: s.direction = "up"
        else:
            if k == 25: s.direction = "right"
            elif k == 23: s.direction = "left"
        
        # Eat fruit
        a = []
        for f in fruits:
            if s.is_colliding_with_fruit(f):
                s.to_spawn += 1
                score += f.score
            else: a.append(f)
        fruits = a
        
        # Place Fruits
        while len(fruits) < N_FRUITS_AT_ONCE:
            fruits.append(Fruit(Vec2(randint(1, X2_WALL-1), randint(1, Y2_WALL-1))))
            if randint(0,5) == 0:
                fruits.append(Fruit(Vec2(randint(1, X2_WALL-1), randint(1, Y2_WALL-1)), SPECIAL_FRUIT_POINTS, SPECIAL_FRUIT_COLOR))
        
        # Move snake
        s.move()
        
        # Check snake collisions
        if s.is_colliding_with_self():
            deathmethod = "self"
            break
            
        if s.is_colliding_with_wall(0,X2_WALL,0,Y2_WALL):
            deathmethod = "wall"
            break
        
        # Render Fruits
        for f in fruits:
            x = AREA_LOCATION_X + (f.position.x * 16)
            y = AREA_LOCATION_Y + (f.position.y * 16)
            draw_rect(x,y-16,x+16,y, f.color)
            print(x, y)
        
        # Render Snake
        for (i,p) in enumerate(s.positions):
            x = AREA_LOCATION_X + (p.x * 16)
            y = AREA_LOCATION_Y + (p.y * 16)
            if i == 0: draw_rect(x,y-16,x+16,y, SNAKE_HEAD_COLOR)
            else: draw_rect(x,y-16,x+16,y, tuple(int(a/(i*1.5)) for a in SNAKE_HEAD_COLOR))
        
        # Display
        show_screen()
        
    # You died lmao
    clear_screen()
    if deathmethod == "wall":
        draw_string(20, 50, choice(["Where's the spatial awareness?"]))
    elif deathmethod == "self":
        draw_string(20, 50, choice(["Self Sabotage?"]))
    elif deathmethod == "hunger":
        draw_string(20, 50, choice(["Are you on a diet?"]))
    else:
        draw_string(0, 50, choice(["..."]))
    draw_string(20, 70, "Score = " + str(score))
    draw_string(20, 170, "Press [OK] to play again...")
    show_screen()
    while True:
        if getkey() == 24:
            clear_screen()
            show_screen()
            break
    

