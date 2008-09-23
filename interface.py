import sys, pygame, main

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
   
   screen.fill(black)
   
   for node in main.circuit.nodes:
      position1 = (node.x-2, node.y-2)
      position2 = (4, 4)
      rectangle = pygame.Rect(position1, position2)
      pygame.draw.rect(screen, red, rectangle, 0)
   
   for road in main.circuit.roads:
      position1 = (road.begin.x, road.begin.y)
      position2 = (road.end.x, road.end.y)
      rectangle = pygame.Rect(position1, position2)
      pygame.draw.line(screen, white, position1, position2, 1)
   
   #screen.blit(ball, ballrect)
   
   
   pygame.display.flip()