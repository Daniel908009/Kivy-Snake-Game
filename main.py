from kivy.uix.actionbar import Button
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.window import Window
import random

# class for settings popup
class SettingsPopup(Popup):
    def __init__(self, caller):
        super(SettingsPopup, self).__init__()
        self.caller = caller
    def setSettings(self):
        self.ids.sizeSetting.text = str(self.caller.sizeOfGrid)
        self.ids.sizeSlider.value = self.caller.sizeOfGrid
        self.ids.speedSetting.text = str(self.caller.speed)
        self.ids.speedSlider.value = self.caller.speed
        self.ids.foodSetting.text = str(self.caller.numberOfFood)
    def applySettings(self):
        self.caller.sizeOfGrid = int(self.ids.sizeSetting.text)
        self.caller.speed = float(self.ids.speedSetting.text)
        self.caller.numberOfFood = int(self.ids.foodSetting.text)
        self.caller.resetGame()
        self.caller.settingsOpen = False
        self.dismiss()
    def dismissPopup(self):
        self.caller.settingsOpen = False
        self.dismiss()

# class for results popup
class ResultsPopup(Popup):
    def __init__(self, caller):
        super(ResultsPopup, self).__init__()
        self.caller = caller
    def setResults(self):
        self.ids.timeLabel.text = self.caller.ids.timeLabel.text
        self.ids.scoreLabel.text = self.caller.ids.scoreLabel.text
        self.ids.speedLabel.text = 'Speed: {}'.format(self.caller.speed)

# class for tiles of the snake grid
class Tile(Button):
    def __init__(self, caller, id, pos):
        super(Tile, self).__init__()
        self.caller = caller
        self.id = id
        self.poss = pos
    def click(self):
        pass

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
        for pos in self.snake:
            for tile in self.ids.snakeGrid.children:
                if tile.poss == pos:
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
        self.settingsOpen = True
        popup.setSettings()
        popup.open()
    def updateTime(self, t):
        if self.settingsOpen:
            return
        self.time += 1
        minutes, seconds = divmod(self.time, 60)
        self.ids.timeLabel.text = 'Time: {:02}:{:02}'.format(minutes, seconds)
    def startGame(self):
        if self.ids.startQuitButton.text == "Start":
            self.ids.startQuitButton.text = "Quit"
            self.ids.startQuitButton.background_color = (1, 1, 0, 1)
            self.timeClockEvent = Clock.schedule_interval(self.updateTime, 1)
            self.gameClockEvent = Clock.schedule_interval(self.gameLoop, 1*(self.speed/5))
        else:
            self.ids.startQuitButton.text = "Start"
            self.ids.startQuitButton.background_color = (0, 1, 0, 1)
            self.timeClockEvent.cancel()
            self.gameClockEvent.cancel()
            popup = ResultsPopup(self)
            popup.setResults()
            popup.open()
            self.resetGame()
    def gameLoop(self, t):
        if self.settingsOpen:
            return
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
        if hasattr(self, 'timeClockEvent') and len(self.snakeGrid) > 0 and self.ids.startQuitButton.text == "Quit": # checking for the snakeGrid to prevent errors when starting the game for the first time
            self.timeClockEvent.cancel()
        if hasattr(self, 'gameClockEvent') and len(self.snakeGrid) > 0 and self.ids.startQuitButton.text == "Quit":
            self.gameClockEvent.cancel()
        self.ids.timeLabel.text = 'Time: 00:00'
        self.score = 1
        self.ids.scoreLabel.text = 'Score: 1'
        self.snakeDirection = "up"
        self.collectedFood = False
        self.ids.startQuitButton.text = "Start"
        self.ids.startQuitButton.background_color = (0, 1, 0, 1)
        self.food = []
        self.setupGrid()
        self.setupSnake()
        for i in range(self.numberOfFood):
            self.generateFood()

# main app class
class SnakeApp(App):
    def build(self):
        return MainGrid()

# running the app
if __name__ == "__main__":
    SnakeApp().run()