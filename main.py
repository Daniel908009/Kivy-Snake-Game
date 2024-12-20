from kivy.uix.actionbar import Button
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.window import Window
import random

# class for settings popup
class SettingsPopup(Popup):
    def __init__(self, caller): # more things will be added later
        super(SettingsPopup, self).__init__()
        self.caller = caller
    def applySettings(self):
        # code for applying settings will be added later
        self.dismiss()

# class for results popup
class ResultsPopup(Popup):
    pass

# class for tiles of the snake grid
class Tile(Button):
    def __init__(self, caller, id, pos):
        super(Tile, self).__init__()
        self.caller = caller
        self.id = id
        self.poss = pos
    def click(self):
        pass # maybe I will add something here later

# class for the main grid
class MainGrid(GridLayout):
    def __init__(self):
        super(MainGrid, self).__init__()
        Window.bind(on_key_down=self.keyAction)
    def setupGrid(self):
        self.ids.snakeGrid.clear_widgets()
        self.ids.snakeGrid.cols = self.sizeOfGrid
        self.snakeGrid = []
        for i in range(self.sizeOfGrid):
            self.snakeGrid.append([])
            for j in range(self.sizeOfGrid):
                tile = Tile(self, i*self.sizeOfGrid+j, [i, j])
                self.ids.snakeGrid.add_widget(tile)
                self.snakeGrid[i].append(tile)
        
    def setupSnake(self):
        self.snake = [[int(self.sizeOfGrid/2), int(self.sizeOfGrid/2)]]
        #print(self.snake)
        for pos in self.snake:
            for tile in self.ids.snakeGrid.children:
                #print(tile.poss)
                #print(pos)
                if tile.poss == pos:
                    #print("found")
                    tile.background_color = (0, 1, 0, 1)
    def keyAction(self, instance, keyboard, keycode, text, modifiers):
        if self.ids.startQuitButton.text == "Quit": # the direction can only be changed when the game is running
            if text == 'w' and self.snakeDirection != "down":
                self.snakeDirection = "up"
            elif text == 'a' and self.snakeDirection != "right":
                self.snakeDirection = "left"
            elif text == 's' and self.snakeDirection != "up":
                self.snakeDirection = "down"
            elif text == 'd' and self.snakeDirection != "left":
                self.snakeDirection = "right"
    def openSettings(self):
        popup = SettingsPopup(self)
        popup.open()
    def updateTime(self, t):
        self.time += 1
        minutes, seconds = divmod(self.time, 60)
        self.ids.timeLabel.text = 'Time: {:02}:{:02}'.format(minutes, seconds)
    def startGame(self):
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
            popup = ResultsPopup() # will be enhanced later
            popup.open()
            self.resetGame()
    def gameLoop(self, t):
        # the movement logic
        if self.snakeDirection != '':
            if self.snakeDirection == "up":
                self.moveSnake("up")
            elif self.snakeDirection == "left":
                self.moveSnake("left")
            elif self.snakeDirection == "down":
                self.moveSnake("down")
            elif self.snakeDirection == "right":
                self.moveSnake("right")
        # all the food logic
        if self.numberOfFood > len(self.food):
            self.generateFood()
    def moveSnake(self, direction):
        for part in self.snake:
            for tile in self.ids.snakeGrid.children:
                if tile.poss == part:
                    tile.background_color = (1, 1, 1, 1)
        copySnake = []
        for i in self.snake:
            copySnake.append(i)
        if direction == "up":
            self.snake[0] = [self.snake[0][0]-1, self.snake[0][1]]
            for i in range(1, len(self.snake)):
                self.snake[i] = copySnake[i-1]
        elif direction == "down":
            self.snake[0] = [self.snake[0][0]+1, self.snake[0][1]]
            for i in range(1, len(self.snake)):
                self.snake[i] = copySnake[i-1]
        elif direction == "left":
            self.snake[0] = [self.snake[0][0], self.snake[0][1]-1]
            for i in range(1, len(self.snake)):
                self.snake[i] = copySnake[i-1]
        elif direction == "right":
            self.snake[0] = [self.snake[0][0], self.snake[0][1]+1]
            for i in range(1, len(self.snake)):
                self.snake[i] = copySnake[i-1]
        else:
            self.snakeDirection = "up"
        for part in self.snake:
            for tile in self.ids.snakeGrid.children:
                if tile.poss == part:
                    tile.background_color = (0, 1, 0, 1)
        for apple in self.food:
            if self.snake[0] == apple:
                self.snake.append(apple)
                self.food.remove(apple)
                self.score += 1
                self.ids.scoreLabel.text = 'Score: {}'.format(self.score)
                self.collectedFood = True
        self.checkCollision()
        self.collectedFood = False
    def checkCollision(self):
        # checking if the snake has hit the wall or itself, I had to rework the grid system to make this work
        if self.snake[0][0] < 0 or self.snake[0][0] >= self.sizeOfGrid or self.snake[0][1] < 0 or self.snake[0][1] >= self.sizeOfGrid:
            self.startGame()
        for i in range(len(self.snake)):
            if i != 0:
                if self.snake[0] == self.snake[i] and self.collectedFood == False:
                    self.startGame()
    def generateFood(self):
        coords =[random.randint(0, self.sizeOfGrid-1), random.randint(0, self.sizeOfGrid-1)]
        while coords in self.snake:
            coords =[random.randint(0, self.sizeOfGrid-1), random.randint(0, self.sizeOfGrid-1)]
        self.food.append(coords)
        for tile in self.ids.snakeGrid.children:
            if tile.poss == coords:
                tile.background_color = (1, 0, 0, 1)
    def resetGame(self):
        self.time = 0
        self.ids.timeLabel.text = 'Time: 00:00'
        self.score = 1
        self.ids.scoreLabel.text = 'Score: 1'
        self.snakeDirection = "up"
        self.food = []
        self.setupGrid()
        self.setupSnake()
        self.generateFood()

# main app class
class SnakeApp(App):
    def build(self):
        return MainGrid()

# running the app
if __name__ == "__main__":
    SnakeApp().run()