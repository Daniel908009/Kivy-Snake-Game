from kivy.uix.actionbar import Button
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.window import Window
import random

class SettingsPopup(Popup):
    def __init__(self, caller): # more things will be added later
        super(SettingsPopup, self).__init__()
        self.caller = caller
    def applySettings(self):
        # code for applying settings will be added later
        self.dismiss()

class Tile(Button):
    def __init__(self, caller, id):
        super(Tile, self).__init__()
        self.caller = caller
        self.id = id
    def click(self):
        #print("tile clicked at id: ", self.id)
        pass

class MainGrid(GridLayout):
    def __init__(self):
        super(MainGrid, self).__init__()
        Window.bind(on_key_down=self.keyAction)
    def setupGrid(self):
        self.ids.snakeGrid.clear_widgets()
        self.ids.snakeGrid.cols = self.sizeOfGrid
        for i in range(self.sizeOfGrid):
            for j in range(self.sizeOfGrid):
                self.ids.snakeGrid.add_widget(Tile(self, i*self.sizeOfGrid+j))
    def setupSnake(self):
        self.snake = [int(self.sizeOfGrid//2)+int(self.sizeOfGrid)*int(self.sizeOfGrid//2)]
        for i in self.snake:
            for tile in self.ids.snakeGrid.children:
                if tile.id == i:
                    tile.background_color = (0, 1, 0, 1)
    def keyAction(self, instance, keyboard, keycode, text, modifiers):
        if self.ids.startQuitButton.text == "Quit": # the direction can only be changed when the game is running
            if text == 'w' and self.snakeDirection != "down":
                #print("w pressed")
                self.snakeDirection = "up"
            elif text == 'a' and self.snakeDirection != "right":
                #print("a pressed")
                self.snakeDirection = "left"
            elif text == 's' and self.snakeDirection != "up":
                #print("s pressed")
                self.snakeDirection = "down"
            elif text == 'd' and self.snakeDirection != "left":
                #print("d pressed")
                self.snakeDirection = "right"
    def openSettings(self):
        popup = SettingsPopup(self)
        popup.open()
    def updateTime(self, t):
        self.time += 1
        minutes, seconds = divmod(self.time, 60)
        self.ids.timeLabel.text = 'Time: {:02}:{:02}'.format(minutes, seconds)
    def startGame(self):
        #print("Game button pressed")
        if self.ids.startQuitButton.text == "Start":
            self.ids.startQuitButton.text = "Quit"
            self.ids.startQuitButton.background_color = (1, 1, 0, 1)
            self.timeClockEvent = Clock.schedule_interval(self.updateTime, 1)
            self.gameClockEvent = Clock.schedule_interval(self.gameLoop, 1)
        else:
            self.ids.startQuitButton.text = "Start"
            self.ids.startQuitButton.background_color = (0, 1, 0, 1)
            self.timeClockEvent.cancel()
            self.gameClockEvent.cancel()
            # results popup will be added later
            self.resetGame()
    def gameLoop(self, t):
        # the movement logic
        if self.snakeDirection != '':
            if self.snakeDirection == "up":
                #print("up")
                self.moveSnake("up")
            elif self.snakeDirection == "left":
                #print("left")
                self.moveSnake("left")
            elif self.snakeDirection == "down":
                #print("down")
                self.moveSnake("down")
            elif self.snakeDirection == "right":
                #print("right")
                self.moveSnake("right")
        
        #print(self.food)
        #print(len(self.food))
        #print(self.numberOfFood)
        
        # all the food logic
        if self.numberOfFood > len(self.food):
            self.generateFood()
            #print("food generated")
    def moveSnake(self, direction):
        for part in self.snake:
            for tile in self.ids.snakeGrid.children:
                if tile.id == part:
                    tile.background_color = (1, 1, 1, 1)
        copySnake = []
        #print(len(self.snake))
        for i in self.snake:
            copySnake.append(i)
        if direction == "up":
            self.snake[0] -= self.sizeOfGrid
            for i in range(len(self.snake)):
                if i != 0:
                    self.snake[i] = copySnake[i-1]
        elif direction == "down":
            self.snake[0] += self.sizeOfGrid
            for i in range(len(self.snake)):
                if i != 0:
                    self.snake[i] = copySnake[i-1]
        elif direction == "left":
            self.snake[0] -= 1
            for i in range(len(self.snake)):
                if i != 0:
                    self.snake[i] = copySnake[i-1]
        elif direction == "right":
            self.snake[0] += 1
            for i in range(len(self.snake)):
                if i != 0:
                    self.snake[i] = copySnake[i-1]
        else:
            self.snakeDirection = "up"

        for part in self.snake:
            for tile in self.ids.snakeGrid.children:
                if tile.id == part:
                    tile.background_color = (0, 1, 0, 1)
        for apple in self.food:
            if self.snake[0] == apple[0]*self.sizeOfGrid+apple[1]:
                self.snake.append(apple[0]*self.sizeOfGrid+apple[1])
                self.food.remove(apple)
                self.score += 1
                #print(self.score)
                self.ids.scoreLabel.text = 'Score: {}'.format(self.score)
                #rint("Apple eaten")
    def generateFood(self):
        coords =[random.randint(0, self.sizeOfGrid-1), random.randint(0, self.sizeOfGrid-1)]
        while coords in self.snake:
            coords =[random.randint(0, self.sizeOfGrid-1), random.randint(0, self.sizeOfGrid-1)]
        self.food.append(coords)
        for tile in self.ids.snakeGrid.children:
            if tile.id == coords[0]*self.sizeOfGrid+coords[1]:
                tile.background_color = (1, 0, 0, 1)
    def resetGame(self):
        #print("Game reset")
        self.time = 0
        self.ids.timeLabel.text = 'Time: 00:00'
        self.score = 1
        self.ids.scoreLabel.text = 'Score: 1'
        self.snakeDirection = "up"
        self.food = []
        self.setupGrid()
        self.setupSnake()
        self.generateFood()


class SnakeApp(App):
    def build(self):
        return MainGrid()
    
if __name__ == "__main__":
    SnakeApp().run()