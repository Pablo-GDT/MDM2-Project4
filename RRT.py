import sys
import numpy as np
import pygame
from pygame.locals import *
import random

# constants

# pygame window dimensions
XDIM = 600
YDIM = 600
WINSIZE = [XDIM, YDIM]


# max length of tree branches
DistThreshold = 8

# max number of nodes in a tree
MaxNodeNum = 200
RADIUS = 5


class CircleObstacle(pygame.sprite.Sprite):

    def __init__(self, screen, WINSIZE, StartCoords, GoalCoords):
        super(CircleObstacle, self).__init__(self)
        self.radius = 20
        GREY = (50, 50, 50)
        pygame.draw.circle(screen, GREY, (random.random()*XDIM, random.random()*YDIM), self.radius)


class Node:

    x = 0
    y = 0
    cost = 0
    parent = None

    def __init__(self, xcoord, ycoord, radius):
        self.x = xcoord
        self.y = ycoord
        self.radius = radius
        self.pathx = []
        self.pathy = []

    def getX():
        return self.x

    def getParentnodex(self):
        return self.parent.x

    def getParentnodey(self):
        return self.parent.y

# good ol pythagora's theorem


def dist(p1, p2):
    return np.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)

# is new node in GoalNode radius


def intersects(NewNode, GoalNode):
    # if the distance between the goal node and the new node is less than the radius, tree has reached target
    if dist([NewNode.x, NewNode.y], [GoalNode.x, GoalNode.y]) < GoalNode.radius:
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
    # ORANGE = (255, 164, 0)
    Red = (0, 255, 0)
    NearestNeigbour = NodeList[0]
    for node in NodeList:
        if dist([node.x, node.y], [GoalNode.x, GoalNode.y]) < dist([NearestNeigbour.x, NearestNeigbour.y], [GoalNode.x, GoalNode.y]):
            NearestNeigbour = node
    print("Total path distance ="+str(NearestNeigbour.cost))
    # iterating through the parent attribute and drawing the path
    while NearestNeigbour != StartNode:
        pygame.draw.line(screen, Red, [int(NearestNeigbour.x), int(NearestNeigbour.y)], [
                         int(NearestNeigbour.getParentnodex()), int(NearestNeigbour.getParentnodey())], 10)
        NearestNeigbour = NearestNeigbour.parent
    pygame.display.update()


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


def find_path(MaxNodeNum, pygame, screen, NodeList, NearestNeigbour, StartNode, GoalNode,  RED, BLACK, path_found):

    for i in range(MaxNodeNum):
        # generate a random point in the screen
        RandomPoint = Node(random.random()*XDIM, random.random()*YDIM, 1)
        # find the nearest neighbour and connect the new point to it
        for node in NodeList:
            if dist([node.x, node.y], [RandomPoint.x, RandomPoint.y]) < dist([NearestNeigbour.x, NearestNeigbour.y], [RandomPoint.x, RandomPoint.y]):
                NearestNeigbour = node

        NewNodeCoords = StepToFrom([NearestNeigbour.x, NearestNeigbour.y], [
            RandomPoint.x, RandomPoint.y])
        # creating node object at target destination
        NewNode = Node(NewNodeCoords[0], NewNodeCoords[1], 0.5)

        NodeList.append(NewNode)
        pygame.draw.circle(screen, RED, (int(NewNode.x), int(NewNode.y)), 1)

        ChooseParent(NearestNeigbour, NewNode, NodeList)

        # Draw line from Nearest Neightbour TO New Node
        pygame.draw.line(screen, BLACK, [int(NearestNeigbour.x),
                                         int(NearestNeigbour.y)], [int(NewNode.x), int(NewNode.y)])

        if intersects(NewNode, GoalNode) is True:
            print('Done!')
            # test(StartNode, NewNode, NearestNeigbour, NodeList, screen)
            DrawSolutionPath(StartNode, GoalNode, NodeList, pygame, screen)
            path_found = True
        else:
            path_found = False

        pygame.display.update()
    print("find_path func:" + str(path_found))
    return path_found


def main():
    running = True
    done = False

# initialise screen and screen settings
    pygame.init()
    screen = pygame.display.set_mode(WINSIZE)
    clock = pygame.time.Clock()
    WHTIE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    screen.fill(WHTIE)

    path_found = False

# run pygame untill done
    while not done:
        # quitting conditions
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYUP and event.key == KEY_ESCAPE):
                sys.exit('User has terminated the app')

        NodeList = []

    # starting coordinates add to list and make it random tree starting point
        StartCoords = [300, 300]
        StartNode = Node(StartCoords[0], StartCoords[1], 10)
        pygame.draw.circle(screen, BLUE, (StartCoords[0], StartCoords[1]), 10)
        NodeList.append(StartNode)
        NearestNeigbour = NodeList[0]

    # goal coordinates
        GoalCoords = [400, 400]
        GoalNode = Node(GoalCoords[0], GoalCoords[1], 10)
        pygame.draw.circle(screen, GREEN, (GoalCoords[0], GoalCoords[1]), 10)

        print("outside if statement:" + str(path_found))
        if path_found is False:
            path_found = find_path(MaxNodeNum, pygame, screen, NodeList,
                                   NearestNeigbour, StartNode, GoalNode, RED, BLACK, path_found)
            print("in if statement:" + str(path_found))
            done = True
        else:

            continue


if __name__ == '__main__':
    main()
