import sys
import numpy as np
from stack import Stack
import tkinter as tk
from PIL import Image, ImageTk

myapp = tk.Tk()

myapp.title('Maze')

raw_mouse_image = Image.open('mouse.png')
mouse_resize_image = raw_mouse_image.resize((30, 32))
mouse_image = ImageTk.PhotoImage(mouse_resize_image)

raw_cheese_image = Image.open('cheese.png')
cheese_resize_image = raw_cheese_image.resize((40, 42))
cheese_image = ImageTk.PhotoImage(cheese_resize_image)

class Maze:
  def __init__(self, current, exit, entry, rows, columns, content):
    self.__current = current
    self.__exit = exit
    self.__rows = rows
    self.__columns = columns
    self.__entry = entry
    self.__EXITMARKET = 'e'
    self.__ENTRYMARKET = 'm'
    self.__VISITED = '.'
    self.__WALL = '|'
    self.__mazeStack = Stack(rows+2*columns+2)
    self.__maze = np.empty((rows+2, columns+2), dtype=str)
    self.__backStack = Stack(self.__rows*self.__columns)
    
    for i in range(self.__rows+2):
      for j in range(self.__columns+2):
        if i == 0 or j == 0 or i == self.__rows+1 or j == self.__columns+1:
          self.__maze[i][j] = self.__WALL
        else:
          self.__maze[i][j] = content[i-1][j-1]

    for i in range(1, self.__rows+1):
      for j in range(1, self.__columns+1):
        if content[i-1][j-1] == '1':
          self.__maze[i][j] = self.__WALL

    self.__maze[self.__entry] = self.__ENTRYMARKET 
    self.__maze[self.__exit] = self.__EXITMARKET

    self.__backStack.empilhar(self.__current)

    label1 = tk.Label(image=mouse_image, width=30, height=32)
    label1.image = mouse_image
    label1.grid(row=self.__current[0], column=self.__current[1])

    label2 = tk.Label(image=cheese_image, width=30, height=32)
    label2.image = cheese_image
    label2.grid(row=self.__exit[0], column=self.__exit[1])

    for i in range(self.__rows+2):
      for j in range(self.__columns+2):
        if self.__maze[i][j] == self.__WALL:
          label = tk.Label(myapp, bg='black', width=4, height=2)
          label.grid(row=i, column=j)
        elif self.__maze[i][j] == '0':
          label = tk.Label(myapp, bg='white', width=4, height=2)
          label.grid(row=i, column=j)

  def run(self):
    if self.__current == self.__exit:
      print('Solucionado')
      return 1
    
    self.__maze[self.__current] = self.__VISITED
    label3 = tk.Label(myapp, bg='gray', width=4, height=2)
    label3.grid(row=self.__current[0], column=self.__current[1])
    
    # vizinho não visitados na pilha
    # direita, esquerda, baixo e cima.
    # empilhar ao contrário

    up = (self.__current[0]-1, self.__current[1])
    down = (self.__current[0]+1, self.__current[1])
    left = (self.__current[0], self.__current[1]-1)
    right = (self.__current[0], self.__current[1]+1)

    count = 0
    if self.__maze[up] == '0' or self.__maze[up] == 'e':
      self.__mazeStack.empilhar(up)
      count = count + 1
    if self.__maze[down] == '0' or self.__maze[down] == 'e':
      self.__mazeStack.empilhar(down)
      count = count + 1
    if self.__maze[left] == '0' or self.__maze[left] == 'e':
      self.__mazeStack.empilhar(left)
      count = count + 1
    if self.__maze[right] == '0' or self.__maze[right] == 'e':
      self.__mazeStack.empilhar(right)
      count = count + 1

    if self.__mazeStack.pilhaVazia():
      print('caminho não encontrado')
      return 0
    else: 
      if count == 0 and not self.__backStack.pilhaVazia():
        self.__current = self.__backStack.desempilhar()

      elif not self.__mazeStack.pilhaVazia():
        self.__backStack.empilhar(self.__mazeStack.verTopo())
        self.__current = self.__mazeStack.desempilhar()

      self.__maze[self.__current] = self.__ENTRYMARKET

    label1 = tk.Label(image=mouse_image, width=30, height=32)
    label1.image = mouse_image
    label1.grid(row=self.__current[0], column=self.__current[1])

  def exitMaze(self):
    pass

def main():
  with open('maze9x9.txt') as file:
  # with open('maze3x4.txt') as file:
    content = file.readlines()

  content = [line.strip('\n') for line in content]

  rows = content.__len__()
  columns = content[0].__len__()
  # entry = (3,3)
  # cheese = (2,4)
  # entry = (8,3)
  # cheese = (3,0)
  entry = (5,7)
  cheese = (0,1)
  current = entry


  maze = Maze(entry, cheese, current, rows, columns, content)
  def key(event):
      match event.keysym: 
        case 'space':
          maze.run()

  navbar = tk.Menu(myapp)
  navbar_options = tk.Menu(navbar, tearoff=0)

  navbar_options.add_command(label="Quit", command=myapp.quit)
  navbar.add_cascade(label="Options", menu=navbar_options)
  myapp.config(menu=navbar)
  myapp.bind('<Key>', key)

  myapp.mainloop()
    
if __name__ == "__main__":
    sys.exit(main())
