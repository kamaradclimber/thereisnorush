import sys, pygame

class Circuit
   def __init__(self, newCrossroads, newRoads)
      self.roads  = newRoads
      self.nodes  = newNodes
   
   def addNode(newX, newY):
      nodes += [newX, newY]
   
   def addRoad(newX, newY):
      nodes += [newX, newY]

pygame.init()

#speed = [2, 2]

#  Colors   ####################################################################

black = (0, 0, 0)
white = (255, 255, 255)
red   = (255, 0, 0)

#  Settings ####################################################################

size     = width, height = (320, 240)
screen   = pygame.display.set_mode(size)
#ball = pygame.image.load("ball.bmp")
#ballrect = ball.get_rect()

while True:
   event = pygame.event.poll()
   
   if event.type == pygame.QUIT:
      sys.exit()
   
   #ballrect = ballrect.move(speed)
   
   #if ballrect.left < 0 or ballrect.right > width:
      #speed[0] = -speed[0]
   
   #if ballrect.top < 0 or ballrect.bottom > height:
      #speed[1] = -speed[1]
   
#  Drawing screen ##############################################################
   
   #for node in nodes:
   position1 = (10-2, 10-2)
   position2 = (4, 4)
   rectangle = pygame.Rect(position1, position2)
      
      
   
   
   screen.fill(black)
   #screen.blit(ball, ballrect)
   #pygame.draw.line(screen, white, position1, position2, 1)
   pygame.draw.rect(screen, red, rectangle, 0)
   pygame.display.flip()