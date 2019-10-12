"""EDIT THIS FILE

InvaderBot is a simple helper class which has methods to control the robot.
It offers an interface over Webots' default motor controller.
You can use it, modify it or you can also use Webots' own commands.
Using the helper class is recommended because it will later help you to
transfer your code into a physical robot, which is running on Raspberry Pi."""

from invader_bot import InvaderBot
from cv_connector import OpenCVConnector
import time
import math

bot = InvaderBot()
bot.setup()

kb = bot.robot.getKeyboard()
kb.enable(bot.timestep)

print("Starting OpenCVConnector...")
connector = OpenCVConnector()
connector.initConnection()
print("Started.")


patrolTargets = [
    [800, 800],
    [800, 200],
    [200, 200]
]

target_id = 0
speed = 100 # robot speed
lastX = 0
lastY = 0
lastPosCount = 0 # shit

# main loop
print("Starting main loop...")
while bot.step() != -1:

    target = patrolTargets[target_id]

    balls = connector.getBallCoordinates()
    pos = bot.get_position()

    while True:
        if balls:
            target = balls
            break
        else:
            balls = connector.getBallCoordinates()
    
    #ball0 = balls[0] if len(balls) > 0 else (0, 0)

    #print("Heading to balls[0] at " + str(ball0))

    #bot.set_motors(1,-1)

        dx = target[0] - pos[0] # difference in x
        dz = target[1] - pos[1] # difference in z

        da = math.atan2(dz, dx) # difference in angle
        da += math.pi/2

        ra = pos[2] - da # relative angle between robot orientation and the goal
        if ra > math.pi:
            ra -= 2 * math.pi
        if ra < -math.pi:
            ra += 2 * math.pi

        ra *= 57
            
        #print("targeting", target, "rel angle", ra)
        #if(lastPosCount == 10):
            #Reverse
        #if(abs(lastX-pos[0]) < 2. and abs(lastY-pos[1]) < 2.):
        #    lastPosCount += 1
        #lastX = pos[0]
        #lastY = pos[1]

        #turn the face towards the goal; about 10 degrees of precision is sufficient. Then march!
        limit = 40.
        limitn = -40.

        if ra < limitn or ra > limit:
            bot.set_motors(speed, 0) # turn right
            bot.set_motors(0, 0) # turn right
       ## elif ra > limit:
          ##  bot.set_motors(0, speed) # turn left
        else:
            bot.set_motors(speed, speed) # go straight
        #print(abs(dx) + abs(dz))
        if (abs(dx) + abs(dz) <= 40): # switch to the next target if close enough
            target_id += 1
            target_id %= len(patrolTargets)
print("my_robot is kill")
