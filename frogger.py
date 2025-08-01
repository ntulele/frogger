import turtle as trtl
import time

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 400
TOP = SCREEN_HEIGHT / 2
BOTTOM = -SCREEN_HEIGHT / 2
LEFTSIDE = -SCREEN_WIDTH / 2
RIGHTSIDE = SCREEN_WIDTH / 2

#NOTE Difficulty is primarily controlled by these 4 variables: 
STARTINGROWS = 1
MAXROWS = 3
LIVES = 5
DEFAULT_SPACING = 100  

ROWHEIGHT = 40 
RIGHT = 0
LEFT = 180

#NOTE 20x20 pixels is recommended size for the frogger and traffic(turtle) shapes
FROGGER_UP = "frogger_up.gif"
FROGGER_DOWN = "frogger_down.gif"
FROGGER_RIGHT = "frogger_right.gif"
FROGGER_LEFT = "frogger_left.gif"
SPLATTED_FROGGER_SHAPE = "skull.gif"
FROGGER_STARTING_HEIGHT = BOTTOM + 35

screen = trtl.Screen()
screen.setup(width=SCREEN_WIDTH, height=400)
screen.bgcolor("black")
screen.title("FROGGER!  by Paul Poling")
screen.tracer(0) 
screen.addshape(FROGGER_UP)
screen.addshape(FROGGER_DOWN)
screen.addshape(FROGGER_RIGHT)
screen.addshape(FROGGER_LEFT)
screen.addshape(SPLATTED_FROGGER_SHAPE) 

writer = trtl.Turtle()
writer.hideturtle()

frogger = trtl.Turtle()
all_turtles = [] 
score = 0
lives = LIVES
highest_reached = BOTTOM
gameover = False

TURTLE_COLORS = ["red", "orange", "yellow", "green", "blue", "purple", "white", "brown" ]
TURTLE_SHAPES = ["turtle","turtle","turtle","turtle","turtle","turtle","turtle","turtle"]

CAR_SHAPES_LEFT = ["car/blue.gif","car/brown.gif","car/purple.gif","car/gray.gif","car/green.gif","car/red.gif","car/teal.gif","car/white.gif"]
CAR_SHAPES_RIGHT = ["car/blue_R.gif","car/brown_R.gif","car/purple_R.gif","car/gray_R.gif","car/green_R.gif","car/red_R.gif","car/teal_R.gif","car/white_R.gif"]
for car in CAR_SHAPES_LEFT + CAR_SHAPES_RIGHT:
    screen.addshape(car)


def reset_frogger():
    global highest_reached
    frogger.penup()
    frogger.shape(FROGGER_UP)
    frogger.goto(0, FROGGER_STARTING_HEIGHT)
    highest_reached = BOTTOM
    frogger.pendown()
    screen.update()

def handle_collision(turtle):
    global lives
    if (abs(turtle.xcor() - frogger.xcor()) < 20) and (abs(turtle.ycor() - frogger.ycor()) < 20):
        frogger.shape(SPLATTED_FROGGER_SHAPE)
        screen.update()
        time.sleep(1)
        lives -= 1
        scoring()
        endgame()
        reset_frogger()
        time.sleep(0.5)

def wrap_around(turtle, direction):
    global LEFT, RIGHT
    rightgutter= RIGHTSIDE + 20
    leftgutter = rightgutter * -1 
    if direction == RIGHT and turtle.xcor() > rightgutter:
        turtle.setx(leftgutter)
    elif direction == LEFT and turtle.xcor() < leftgutter:
        turtle.setx(rightgutter)

def move_turtles(turts, direction=RIGHT, speed=2): 
    if gameover: return   #This hack is the only way I could determine to properly "freeze" the game when done

    for t in turts:
        t.forward(speed)  
        wrap_around(t, direction)
        handle_collision(t)
    screen.update() 

    #Keep the turtle row running:
    screen.ontimer(lambda: move_turtles(turts, direction, speed), 20)        

def load_traffic_row(rownum, direction, shapes, colors, spacing=DEFAULT_SPACING):
    turts = []
    for i in range(len(shapes)):
        t = trtl.Turtle(shapes[i])
        t.fillcolor(colors[i])
        t.penup()
        t.setheading(direction)
        xcor = RIGHTSIDE - (i * spacing)
        bottom = BOTTOM + 75
        t.goto(xcor, bottom + rownum * ROWHEIGHT)  
        turts.append(t)
    all_turtles.append(turts)

def activaterows(numberofrows):
    currentrowcount = len(all_turtles)
    for row in range(currentrowcount, currentrowcount + numberofrows):
        traffic = TURTLE_SHAPES
        direction = RIGHT
        cars = CAR_SHAPES_RIGHT
        spacebetween = DEFAULT_SPACING
        if row % 2 == 0: 
            direction = LEFT
            cars = CAR_SHAPES_LEFT
        if row > 3:
            traffic = cars
            spacebetween += 5
        load_traffic_row(row, direction, traffic, TURTLE_COLORS, spacing = spacebetween)
        move_turtles(all_turtles[row], direction, row + 1)

def hop_leftright(hops):
    if gameover: return  #Hacky solution to prevent further Frogger movement (and scoring!) at game end
    SIDE_HOP = 20
    if (hops) < 0:
        frogger.shape(FROGGER_LEFT)
    else:
        frogger.shape(FROGGER_RIGHT)

    newX = frogger.xcor() + SIDE_HOP * hops
    if abs(newX) < abs(SCREEN_WIDTH/2 - 20):
        frogger.setx(newX)

def hop_updown(hops):
    if gameover: return  #Hacky solution to prevent further Frogger movement (and scoring!) at game end
    global highest_reached, score
    VERTICAL_HOP = ROWHEIGHT #fixed, to keep Frogger centered vertically on row
    height = frogger.ycor()
    if (hops) < 0:
        frogger.shape(FROGGER_DOWN)
    else:
        frogger.shape(FROGGER_UP)
        if height > highest_reached:
            score += 50
            scoring()
            highest_reached = height

    newheight = height + VERTICAL_HOP * hops
    maxvertical = ROWHEIGHT * (len(all_turtles) + 1) + FROGGER_STARTING_HEIGHT
    if newheight >= FROGGER_STARTING_HEIGHT and newheight <= maxvertical:  #Keep Frogger in-bounds
        frogger.sety(newheight)
        if newheight == maxvertical and lives > 0:  #Frogger made it through!
            celebrate()
            reset_frogger()

"""
Credit goes to Nick S-F for his score management code 
that I used as a foundation for the writer usage in scoring() and celbrate() below
"""
def scoring():
    global score, lives, gameover
    writer.clear()
    writer.color("white")
    writer.penup()
    writer.goto(LEFTSIDE + 10, TOP - 70)
    writer.pendown()
    writer.write(
        f"Score: {score}\nLives: {lives}", align="left", font=("Arial", 16, "normal")
    )
    screen.update()

    endgame()

def endgame():
    global gameover
    if lives == 0:
        gameover=True  #This is then used by looped turtles to stop them at game end
        writer.color("red")
        writer.penup()
        writer.goto(0, TOP - 50)
        writer.pendown()
        writer.write("Game Over", align="center", font=("Arial", 24, "bold"))
        screen.update()

def celebrate():
    global gameover, score
    writer.color("green")
    writer.penup()
    writer.goto(-50, TOP - 100)
    writer.pendown()
    bonus = 500 * len(all_turtles)
    writer.write(f"Congrats, you survived! \nBonus: {bonus}\n", align="left", font=("Arial", 18, "bold"))
    score += bonus


    if len(all_turtles) < MAXROWS:
        writer.write("\n\n\nLet's add a lane!", align="left", font=("Arial", 18, "bold"))
        screen.update()
        time.sleep(1)
        scoring()
        reset_frogger()
        activaterows(1)
        time.sleep(1)
    else:
        screen.update()
        time.sleep(1)
        scoring()
        writer.color("green")
        writer.penup()
        writer.goto(-50, TOP - 100)
        writer.pendown()
        writer.write("\n!!!!  You Won  !!!!!", align="center", font=("Arial", 24, "bold"))
        screen.update()
        time.sleep(3)
        gameover=True   #Used to stop further turtle movement/interaction


reset_frogger() #call before row buildout, or lose a life! 
activaterows(STARTINGROWS)
scoring()
screen.onkey(lambda: hop_leftright(-1), "Left")
screen.onkey(lambda: hop_leftright(1), "Right")
screen.onkey(lambda: hop_updown(1), "Up")
screen.onkey(lambda: hop_updown(-1), "5")
screen.onkey(lambda: hop_updown(-1), "Down")
screen.listen()

screen.mainloop()