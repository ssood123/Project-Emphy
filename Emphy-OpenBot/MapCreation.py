import pygame, sys
from pygame.locals import *
import math
import random

#This function draws the "canvas" where you can draw your map
def drawEverything(screen,scaleFactor,numberOfRows,numberOfColumns,backgroundColor,screenWidth,screenHeight,displayGridLines,maze):
  screen.fill(backgroundColor);
  for i in range(0,numberOfRows):
    for j in range(0,numberOfColumns):
      if maze[i][j] == 1:
        pygame.draw.rect(screen,(0,0,0),[j*scaleFactor,i*scaleFactor,scaleFactor,scaleFactor]);
      elif maze[i][j] == 0:
        pygame.draw.rect(screen,(255,255,255),[j*scaleFactor,i*scaleFactor,scaleFactor,scaleFactor]);
  pygame.display.update();
  if displayGridLines == True:
    x = 0;
    while x*scaleFactor < screenWidth:
      pygame.draw.line(screen,(0,0,0),(x*scaleFactor,0),(x*scaleFactor,screenHeight));
      x = x + 1;
    pygame.display.update();
    y = 0;
    while y*scaleFactor < screenHeight:
      pygame.draw.line(screen,(0,0,0),(0,screenHeight-y*scaleFactor),(screenWidth,screenHeight-y*scaleFactor));
      y = y + 1;
    pygame.display.update();

#Prints your drawn map in C format
def printMazeinCFormat(maze,numberOfRows,numberOfColumns):
  print("{",end="");
  for i in range(0,numberOfRows):
    print("{",end="");
    for j in range(0,numberOfColumns):
      if j == numberOfColumns-1:
        print(str(maze[i][j]),end="");
      else:
        print(str(maze[i][j]) + "," ,end="");
    if i == numberOfRows-1:
      print("}",end="");
    else:
      print("},");
  print("}");
  for i in range(2):
    print();

#This function draws your map in python format
def printMazeinPythonFormat(maze,numberOfRows,numberOfColumns):
  print("[",end="");
  for i in range(0,numberOfRows):
    print("[",end="");
    for j in range(0,numberOfColumns):
      if j == numberOfColumns-1:
        print(str(maze[i][j]),end="");
      else:
        print(str(maze[i][j]) + "," ,end="");
    if i == numberOfRows-1:
      print("]",end="");
    else:
      print("],");
  print("]");
  for i in range(2):
    print();

def main():
  #Set initial data
  count = 1;
  scaleFactor = 20;
  numberOfRows = int(input("How many rows do you want? (for example, 30) "));
  numberOfColumns = int(input("How many columns do you want? (for example, 30) "));
  printImages = input("Would you like the program to save pictures of the map on your computer (yes/no)? ");
  #The instructions
  print("Directions: Once the pygame GUI opens up, left click to create a barrier.");
  print("Right click to create free space/erase a barrier.");
  print("Once you are done, press space to print the map in C/C++ and Python format.");
  print("You can update the map and print as many times as you like. Make sure to look at the most recently printed map.");
  print("Once you print a map, an image of the map may be saved to your computer (depending on whether or not you answered yes or no to the previous question) for future reference. Check your local folder for this.");
  backgroundColor = (255,255,255);
  screenWidth=scaleFactor*numberOfColumns;
  screenHeight=scaleFactor*numberOfRows;
  displayGridLines = True;

  #Setup map properly
  w, h = numberOfColumns, numberOfRows;
  maze = [[0 for x in range(w)] for y in range(h)]; 
  pygame.init();
  screen = pygame.display.set_mode((screenWidth,screenHeight));
  pygame.display.set_caption("Draw the Map")
  drawEverything(screen,scaleFactor,numberOfRows,numberOfColumns,backgroundColor,screenWidth,screenHeight,displayGridLines,maze);

  #The main loop, has a bunch of event handlers
  while True:
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit();
        sys.exit();
      if pygame.mouse.get_pressed()[0]: #LEFT CLICK draws a barrier/deletes free space
        mousePos = pygame.mouse.get_pos();
        mousePosX = int(mousePos[0]/scaleFactor);
        mousePosY = int(mousePos[1]/scaleFactor);
        maze[mousePosY][mousePosX] = 1;
        drawEverything(screen,scaleFactor,numberOfRows,numberOfColumns,backgroundColor,screenWidth,screenHeight,displayGridLines,maze);
        pygame.draw.rect(screen,(0,0,0),[mousePosX*scaleFactor,mousePosY*scaleFactor,scaleFactor,scaleFactor]);
      if pygame.mouse.get_pressed()[2]: #RIGHT CLICK erases a barrier/creates free space
        mousePos = pygame.mouse.get_pos();
        mousePosX = int(mousePos[0]/scaleFactor);
        mousePosY = int(mousePos[1]/scaleFactor);
        maze[mousePosY][mousePosX] = 0;
        drawEverything(screen,scaleFactor,numberOfRows,numberOfColumns,backgroundColor,screenWidth,screenHeight,displayGridLines,maze);
        pygame.draw.rect(screen,(255,255,255),[mousePosX*scaleFactor,mousePosY*scaleFactor,scaleFactor,scaleFactor]);
      if event.type == pygame.KEYDOWN: #Once space is pressed, print the map and save an image of it if applicable
        if event.key == pygame.K_SPACE:
          print("Map " + str(count) + ":");
          printMazeinPythonFormat(maze,numberOfRows,numberOfColumns);
          printMazeinCFormat(maze,numberOfRows,numberOfColumns);
          if printImages == "yes": #Saves an image of the map (called mapImage.png) to local folder
            pygame.image.save(screen,"mapImage.png");
          count = count + 1;

if __name__ == "__main__":
  main();