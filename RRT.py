import pylab
import sympy.vector as sv
import sympy as sym
import matplotlib.backends.backend_agg as agg
import sys
import numpy as np
import pygame
from pygame.locals import *
import random
import matplotlib
matplotlib.use("Agg")

sym.init_printing()

offX = 600
offY = 300
# constants
SFX = 121
SFY = 60
# pygame window dimensions
XDIM = 1200
YDIM = 600
WINSIZE = [XDIM, YDIM]


# max length of tree branches
DistThreshold = 120


class ExploredLine(pygame.sprite.Sprite):

    def __init__(self, screen, startpoint, endpoint, width, height):
        BLUE = (0, 0, 255)
        pygame.sprite.Sprite.__init__(self)

        self.startpoint = startpoint
        self.endpoint = endpoint
        self.width = width
        self.height = height
        self.x = startpoint[0]
        self.y = startpoint[1]
        self.rectangle_Surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.rectangle_Surface.get_rect(
            center=(int(self.x + 0.5*(self.width)), int(self.y + 0.5*(self.height))))
        self.line = pygame.draw.line(screen, BLUE, self.startpoint, self.endpoint, 80)
        # Draw a rectangle onto the `rectangle` surface.

        # draw rectangle in the centre of the obstacle surface

        # self.mask = pygame.mask.from_surface(self.circle_Surface)
        # self.mask = pygame.mask.from_threshold(self.rectangle_Surface, BLUE)
        # screen.blit(self.rectangle_Surface, (self.startpoint, self.endpoint))

    def draw(self, screen):
        BLUE = (0, 0, 255)
        self.line = pygame.draw.rect(screen, BLUE, self.rect)


class RectangleObstacle(pygame.sprite.Sprite):

    def __init__(self, screen, x, y, width, height, StartCoords, GoalCoords):
        GREY = (50, 50, 50)
        pygame.sprite.Sprite.__init__(self)

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rectangle_Surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.rectangle_Surface.get_rect(
            center=(int(self.x + 0.5*(self.width)), int(self.y + 0.5*(self.height))))
        # Draw a rectangle onto the `rectangle` surface.

        # draw rectangle in the centre of the obstacle surface
        self.rectangle = pygame.draw.rect(screen, GREY, self.rect)
        # self.mask = pygame.mask.from_surface(self.circle_Surface)
        self.mask = pygame.mask.from_threshold(self.rectangle_Surface, GREY)
        screen.blit(self.rectangle_Surface, (self.x, self.y))

    def draw(self, screen):
        GREY = (50, 50, 50)
        self.rectangle = pygame.draw.rect(screen, GREY, self.rect)


class CircleObstacle(pygame.sprite.Sprite):

    def __init__(self, screen, x, y, radius, StartCoords, GoalCoords):
        GREY = (50, 50, 50)
        pygame.sprite.Sprite.__init__(self)

        self.x = x
        self.y = y
        self.radius = radius
        self.circle_Surface = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        self.rect = self.circle_Surface.get_rect(center=(self.x + radius, self.y + radius))
        # Draw a circle onto the `circle` surface.

        # draw circle in the centre of the obstacle surface
        self.circle = pygame.draw.circle(
            self.circle_Surface, GREY, (radius, radius), self.radius)
        # self.mask = pygame.mask.from_surface(self.circle_Surface)
        self.mask = pygame.mask.from_threshold(self.circle_Surface, GREY)
        screen.blit(self.circle_Surface, [int(self.x), int(self.y)])

    def draw(self, screen):
        GREY = (50, 50, 50)
        self.circle = pygame.draw.circle(
            self.circle_Surface, GREY, (self.radius, self.radius), self.radius)


class Node(pygame.sprite.Sprite):

    x = 0
    y = 0
    cost = 0
    parent = None

    def __init__(self, screen, xcoord, ycoord, radius):
        RED = (255, 0, 0)
        pygame.sprite.Sprite.__init__(self)
        self.x = xcoord
        self.y = ycoord
        self.radius = radius
        self.pathx = []
        self.pathy = []

        self.circle_Surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        self.rect = self.circle_Surface.get_rect(
            center=(int(self.x + radius), int(self.y + radius)))
        # self.mask = pygame.mask.from_surface(self.circle_Surface)
        self.mask = pygame.mask.from_threshold(self.circle_Surface, RED)
        screen.blit(self.circle_Surface, (int(self.x), int(self.y)))

    def getX():
        return self.x

    def getParentnodex(self):
        return self.parent.x

    def getParentnodey(self):
        return self.parent.y

    def draw(self, screen, colour):
        pygame.draw.circle(screen, colour, [self.x, self.y], self.radius)


class Explorationarea(pygame.sprite.Sprite):

    def __init__(self, screen, xcoord, ycoord, radius):
        BLUE = (0, 0, 255)
        pygame.sprite.Sprite.__init__(self)
        self.x = int(xcoord)
        self.y = int(ycoord)
        self.exploredradius = int(radius)
        self.circle_Surface = pygame.Surface(
            (self.exploredradius*2, self.exploredradius*2), pygame.SRCALPHA)
        self.rect = self.circle_Surface.get_rect(
            center=(int(self.x + self.exploredradius), int(self.y + self.exploredradius)))
        # self.mask = pygame.mask.from_surface(self.circle_Surface)
        self.mask = pygame.mask.from_threshold(self.circle_Surface, BLUE)
        # self.exploredarea = pygame.draw.circle(
        #     screen, BLUE, (self.x, self.y), self.exploredradius)
        screen.blit(self.circle_Surface, (self.x, self.y))
        # print(self.rect)

    def draw(self, screen, colour):
        pygame.draw.circle(screen, colour, [self.x, self.y], self.exploredradius)

# good ol pythagora's theorem


def dist(p1, p2):
    return np.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)

# is new node in GoalNode radius


def intersects(NewNode, GoalNode):
    # if the distance between the goal node and the new node is less than the radius, tree has reached target
    if dist([NewNode.x, NewNode.y], [GoalNode.x, GoalNode.y]) < (NewNode.exploredradius + GoalNode.radius):
        return True
    else:
        return False


def ChooseParent(NearestNeigbour, NewNode, NodeList):
    # assign the parent node to the new node and its cost/distance from start node
    NewNode.cost = NearestNeigbour.cost + \
        dist([NearestNeigbour.x, NearestNeigbour.y], [NewNode.x, NewNode.y])
    NewNode.parent = NearestNeigbour

# draw the successful route by calling the parent attribute iteratively


def DrawSolutionPath(StartNode, GoalNode, NodeList, pygame, screen):
    GREEN = (0, 255, 0)
    NearestNeigbour = NodeList[0]
    PathList = []
    for node in NodeList:
        if dist([node.x, node.y], [GoalNode.x, GoalNode.y]) < dist([NearestNeigbour.x, NearestNeigbour.y], [GoalNode.x, GoalNode.y]):
            NearestNeigbour = node
            #PathList.append((node.x, node.y))
    print("Total path distance ="+str(NearestNeigbour.cost))
    # iterating through the parent attribute and drawing the path
    while NearestNeigbour != StartNode:
        pygame.draw.line(screen, GREEN, [int(NearestNeigbour.x), int(NearestNeigbour.y)], [
                         int(NearestNeigbour.getParentnodex()), int(NearestNeigbour.getParentnodey())], 10)
        NearestNeigbour = NearestNeigbour.parent
        PathList.append((NearestNeigbour.x, NearestNeigbour.y))
    pygame.display.update()
    print(PathList)

    runrik = True
    integral = 0
    while runrik:
        cords0 = (PathList[0])
        cords1 = (PathList[1])

        l1 = (2.5 / SFX) * ((cords0[0] - offX) + (cords1[0] - cords0[0]) * t) * R.i + \
            (2.5 / SFY) * ((-cords0[1] + offY) + (-cords1[1] + cords0[1]) * t) * R.j
        firstInt = (li(l1, v))
        integral += firstInt
        print(-integral)
        if len(PathList) == 2:
            print('work is')
            print(-integral)
            runrik = False

        else:
            PathList.remove(PathList[0])

    return PathList


def StepToFrom(NearestNeigbour, RandomPoint):
    # if point is less than the distance threshold from the nearest node add it
    # to the tree otherwise calculate the position
    # of the point at the threshold distance in that direction
    if dist(NearestNeigbour, RandomPoint) <= DistThreshold:
        return RandomPoint
    else:
        theta = np.arctan2((RandomPoint[1] - NearestNeigbour[1]),
                           (RandomPoint[0]-NearestNeigbour[0]))
        return (round(NearestNeigbour[0] + np.cos(theta)*DistThreshold, 0), round(NearestNeigbour[1] + np.sin(theta)*DistThreshold, 0))


def find_path(MaxNodeNum, pygame, screen, NodeList, NearestNeigbour, StartNode, GoalNode,  RED, BLACK, WHITE, BLUE, GREEN, GREY, path_found, obstacles):
    ExploredAreaGroup = pygame.sprite.Group()

    GoalNodeGroup = pygame.sprite.GroupSingle()
    GoalNodeGroup.add(GoalNode)
    for i in range(MaxNodeNum):
        # generate a random point in the screen
        RandomPoint = Node(screen, random.random()*XDIM, random.random()*YDIM, 1)
        # find the nearest neighbour and connect the new point to it
        for node in NodeList:
            if dist([node.x, node.y], [RandomPoint.x, RandomPoint.y]) < dist([NearestNeigbour.x, NearestNeigbour.y], [RandomPoint.x, RandomPoint.y]):
                NearestNeigbour = node
##################################
# NearestNeigbour Co-coordinates ^^^^^^^
##################################
##################################
# NewNode Co-coordinates
##################################
        NewNodeCoords = StepToFrom([NearestNeigbour.x, NearestNeigbour.y], [
            RandomPoint.x, RandomPoint.y])
        if (125 < NewNodeCoords[0] < 1075) and (75 < NewNodeCoords[1] < 530):
            # creating node object at target destination and add it to a group to check for collisions
            NewNode = Node(screen, NewNodeCoords[0], NewNodeCoords[1], 1)
            NodeGroup = pygame.sprite.Group()
            NodeGroup.add(NewNode)
###################################
# Energy function attempt
###################################
            # linex = ((((2.5 / SFX) * (NewNode.x - NearestNeigbour.x) + SFX*t) + R.i) +
            #          (2.5 / SFY) * ((NewNode.x - NearestNeigbour.x) + R.j))
            # xint = (li(linex, v))
            #
            # liney = ((2.5 / SFX) * ((NewNode.x - NearestNeigbour.x) * R.i) +
            #          ((2.5 / SFY) * ((NewNode.x - NearestNeigbour.x) + SFY*t) + R.j)
            # yint = (li(linex, v))

            collision = pygame.sprite.groupcollide(NodeGroup, obstacles, True, False)

            # if it didn't collide draw it and add it to the group
            if not collision:
                # check for line collision with obstacles
                line_collision = False
                for obj in obstacles:
                    if isinstance(obj, RectangleObstacle):

                        clipped_line = obj.rect.clipline((int(NearestNeigbour.x), int(
                            NearestNeigbour.y)), (int(NewNode.x), int(NewNode.y)))
                        if clipped_line:
                            line_collision = True
                            # print("clipped line")
                if not line_collision:

                    # Draw node from  and line from Nearest Neightbour TO New Node

                    Exploredarea = Explorationarea(
                        screen, NewNodeCoords[0], NewNodeCoords[1], 40)

                    VisibleGroup = pygame.sprite.Group()
                    # VisibleGroup.add(Exploredarea)
                    # VisibleGroup.add(ExploredLineObj)
                    # assume no collision
                    exploration_collision = 0
                    # check for collision
                    for obj in ExploredAreaGroup:
                        ExploredCollision = pygame.sprite.collide_rect(Exploredarea, obj)
                        print(Exploredarea.rect)
                        print(obj.rect)
                        print(ExploredCollision)
                        if ExploredCollision == 1:
                            # if collision modify variable
                            exploration_collision = True
                    if not exploration_collision:
                        vision_radius = Exploredarea.draw(screen, BLUE)
                        ExploredLineObj = ExploredLine(screen, [NearestNeigbour.x, NearestNeigbour.y], [
                            NewNode.x, NewNode.y], 80, 80)
                        # ExploredLineObj = ExploredLine.draw(screen, BLUE)
                        ExploredAreaGroup.add(Exploredarea)

                        ExploredAreaGroup.add(ExploredLineObj)
                        NodeList.append(NewNode)
                        GoalNode.draw(screen, GREEN)
                        NewNode.draw(screen, RED)
                        pygame.draw.line(screen, BLACK, [NearestNeigbour.x, NearestNeigbour.y], [
                            NewNode.x, NewNode.y])
                        for obj in obstacles:
                            obj.draw(screen)
                        ChooseParent(NearestNeigbour, NewNode, NodeList)
                        if intersects(Exploredarea, GoalNode) is True or pygame.sprite.collide_rect(ExploredLineObj, GoalNode):
                            # ('Done!'
                            PathList = DrawSolutionPath(
                                StartNode, GoalNode, NodeList, pygame, screen)
                            path_found = True
                            break
                        else:
                            continue
        pygame.display.update()
        # print("find_path func:" + str(path_found))
    return path_found


def plotStream():
    # VECTOR FIELD
    w = 10
    Y, X = np.mgrid[-w:w:100j, -w:w:100j]

    # U =  (X/2) + (3*Y/4)
    # V = 3*(Y**2)/100

    U = -Y**2

    V = 0*Y/Y

    speed = np.sqrt(U ** 2 + V ** 2)

    fig = matplotlib.figure.Figure(figsize=(12.5, 6.25))

    # Varying color along a streamline
    ax = fig.add_subplot(111)
    strm = ax.streamplot(X, Y, U, V, color=U, linewidth=2, cmap='autumn')

    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = canvas.get_width_height()
    surf = pygame.image.fromstring(raw_data, size, "RGB")
    # screen.blit(surf, (0, 0))
    return surf


# line integral
x, y, z, t = sym.symbols('x,y,z,t')
R = sv.CoordSys3D('R')


def v(x, y, z):

    # return ((x/2) + (3*y/4)) * R.i + (3*(y**2)/100) * R.j
    return (-y**2) * R.i + 0*R.j


def voft(l):  # vector field along path l as a function of t
    x, y, z = (l.dot(R.i), l.dot(R.j), l.dot(R.k))  # x,y,z as functions of t
    return v(x, y, z)


def li(l, v):  # dl/dt
    dl = sym.diff(l, t)
    return sym.integrate(voft(l).dot(dl), (t, 0, 1))


def main():
    running = True
    done = False

# initialise screen and screen settings
    pygame.init()
    screen = pygame.display.set_mode(WINSIZE)
    surf = plotStream()
    clock = pygame.time.Clock()
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    GREY = (50, 50, 50)
    screen.fill(WHITE)

    path_found = False
    # max number of nodes in a tree
    MaxNodeNum = 1500


# run pygame untill done
    while not done:

        # quitting conditions
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYUP and event.key == KEY_ESCAPE):
                sys.exit('User has terminated the app')

        NodeList = []

        if path_found is False:

            screen.fill(WHITE)
            screen.blit(surf, (-41, -16))
            # starting coordinates add to list and make it random tree starting point
            StartCoords = [280, 280]
            StartNode = Node(screen, StartCoords[0], StartCoords[1], 10)
            pygame.draw.circle(screen, BLUE, (StartCoords[0], StartCoords[1]), 10)
            NodeList.append(StartNode)
            NearestNeigbour = NodeList[0]

        # goal coordinates
            GoalCoords = [963, 360]
            GoalNode = Node(screen, GoalCoords[0], GoalCoords[1], 20)
            pygame.draw.circle(screen, GREEN, (GoalCoords[0], GoalCoords[1]), 20)

        # instantiating obsticles
            obstacles = pygame.sprite.Group()
            # obstacle1 = CircleObstacle(screen, 500, 250, 60, StartCoords, GoalCoords)
            # # obstacle2 = CircleObstacle(screen, 400, 400, 20, StartCoords, GoalCoords)
            # obstacle3 = RectangleObstacle(screen, 400, 200, 40, 300, StartCoords, GoalCoords)

            # Creation of blocks/obsticles
            obstacle4 = RectangleObstacle(screen, 115, 100, 400, 20, StartCoords, GoalCoords)
            obstacle5 = RectangleObstacle(screen, 200, 300, 300, 20, StartCoords, GoalCoords)
            obstacle6 = RectangleObstacle(screen, 300, 100, 20, 220, StartCoords, GoalCoords)

            obstacle7 = RectangleObstacle(screen, 400, 200, 200, 20, StartCoords, GoalCoords)
            obstacle8 = RectangleObstacle(screen, 500, 500, 583, 20, StartCoords, GoalCoords)
            obstacle9 = RectangleObstacle(screen, 600, 400, 20, 120, StartCoords, GoalCoords)
            obstacle10 = RectangleObstacle(screen, 700, 100, 20, 300, StartCoords, GoalCoords)
            obstacle11 = RectangleObstacle(screen, 1000, 59, 20, 83, StartCoords, GoalCoords)
            obstacles.add(obstacle4, obstacle5,
                          obstacle6, obstacle7, obstacle8, obstacle9, obstacle10, obstacle11)

            path_found = find_path(MaxNodeNum, pygame, screen, NodeList,
                                   NearestNeigbour, StartNode, GoalNode, RED, BLACK, WHITE, BLUE, GREEN, GREY, path_found, obstacles)
            # print("in if statement:" + str(path_found))

            MaxNodeNum = MaxNodeNum+250
            print("Max node num is now:" + str(MaxNodeNum))
        else:

            pygame.display.update()
            continue


if __name__ == '__main__':
    main()
