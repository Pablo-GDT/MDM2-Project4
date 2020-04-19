import sys
import numpy as np
import pygame
from pygame.locals import *
import random

# constants
XDIM = 600
YDIM = 600
WINSIZE = [XDIM, YDIM]
DistThreshold = 8
MaxNodeNum = 200
RADIUS = 10


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

    def getX():
        return self.x

    def getY():
        return self.y


def dist(p1, p2):
    return np.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)


def intersects(NewNode, GoalNode):
    if dist(NewNode, GoalNode) < GoalNode.radius:
        return True
    else:
        return False


def ChooseParent(NearestNeigbour, NewNode, NodeList):
    for node in NodeList:
        print(dist([node.x, node.y], [NearestNeigbour.x, NearestNeigbour.y]))
        print(dist([node.x, node.y], [NewNode.x, NewNode.y]))
        if dist([node.x, node.y], [NewNode.x, NewNode.y]) < RADIUS and node.cost + dist([node.x, node.y], [NewNode.x, NewNode.y]) < NearestNeigbour.cost + dist([NearestNeigbour.x, NearestNeigbour.y], [NewNode.x, NewNode.y]):
            NearestNeigbour = node
            NewNode.cost = NearestNeigbour.cost + \
                dist([NearestNeigbour.x, NearestNeigbour.y], [NewNode.x, NewNode.y])
            NewNode.parent = NearestNeigbour
            return NewNode, NearestNeigbour


def DrawSolutionPath(StartNode, GoalNode, NodeList, pygame, screen):
    ORANGE = (255, 164, 0)
    NearestNeigbour = NodeList[0]
    for node in NodeList:
        if dist([node.x, node.y], [GoalNode.x, GoalNode.y]) < dist([NearestNeigbour.x, NearestNeigbour.y], [GoalNode.x, GoalNode.y]):
            NearestNeigbour = node
        while NearestNeigbour != StartNode:
            pygame.draw.line(
                screen, ORANGE, (int(NearestNeigbour.x), int(NearestNeigbour.y)), (int(NearestNeigbour.parent), int(NearestNeigbour.parent.y), 5))
            NearestNeigbour = NearestNeigbour.parent


def StepToFrom(NearestNeigbour, RandomPoint):
    # if point is less than the distance threshold from the nearest node add it
    # to the tree otherwise calculate the position
    # of the point at the threshold distance in that direction
    if dist(NearestNeigbour, RandomPoint) < DistThreshold:
        return RandomPoint
    else:
        theta = np.arctan2((RandomPoint[1] - NearestNeigbour[1]),
                           (RandomPoint[0]-NearestNeigbour[0]))
        return NearestNeigbour[0] + np.cos(theta)*DistThreshold, NearestNeigbour[1] + np.sin(theta)*DistThreshold


def main():
    running = True
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

    while running is True:

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

        for i in range(MaxNodeNum):
            # generate a random point in the screen
            RandomPoint = Node(random.random()*XDIM, random.random()*YDIM, 1)
            # find the nearest neighbour and connects the new point to it
            for node in NodeList:
                if dist([node.x, node.y], [RandomPoint.x, RandomPoint.y]) < dist([NearestNeigbour.x, NearestNeigbour.y], [RandomPoint.x, RandomPoint.y]):
                    NearestNeigbour = node

            NewNodeCoords = StepToFrom([NearestNeigbour.x, NearestNeigbour.y], [
                                       RandomPoint.x, RandomPoint.y])
            NewNode = Node(NewNodeCoords[0], NewNodeCoords[1], 0.5)
            NodeList.append(NewNode)
            print(NodeList)
            pygame.draw.circle(screen, RED, (int(NewNode.x), int(NewNode.y)), 1)
            print(NearestNeigbour)
            print(NewNode)
            print(NodeList)
            # CHANGESs
            #NewNode, NearestNeigbour = ChooseParent(NearestNeigbour, NewNode, NodeList)
            # commenting
            pygame.draw.line(screen, BLACK, [int(NearestNeigbour.x),
                                             int(NearestNeigbour.y)], [int(NewNode.x), int(NewNode.y)])
            # if intersects(NewNode, GoalNode):
            #     print('Done!')
            #     DrawSolutionPath(StartNode, GoalNode, NodeList, pygame, screen)

        pygame.display.update()


if __name__ == '__main__':
    main()
