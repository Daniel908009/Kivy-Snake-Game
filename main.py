from kivy.uix.actionbar import Button
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.window import Window

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
            if text == 'w':
                print("w pressed")
                self.snakeDirection = "up"
            elif text == 'a':
                print("a pressed")
                self.snakeDirection = "left"
            elif text == 's':
                print("s pressed")
                self.snakeDirection = "down"
            elif text == 'd':
                print("d pressed")
                self.snakeDirection = "right"
    def openSettings(self):
        popup = SettingsPopup(self)
        popup.open()
    def updateTime(self, t):
        self.time += 1
        minutes, seconds = divmod(self.time, 60)
        self.ids.timeLabel.text = 'Time: {:02}:{:02}'.format(minutes, seconds)
    def startGame(self):
        print("Game button pressed")
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
        # movement code will be here
        if self.numberOfFood > len(self.food):
            self.generateFood()
    def generateFood(self):
        pass
    def resetGame(self):
        print("Game reset")
        self.time = 0
        self.ids.timeLabel.text = 'Time: 00:00'
        self.snakeDirection = "up"
        self.setupGrid()
        self.setupSnake()

class SnakeApp(App):
    def build(self):
        return MainGrid()
    
if __name__ == "__main__":
    SnakeApp().run()