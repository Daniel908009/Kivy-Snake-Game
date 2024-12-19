from kivy.uix.actionbar import Button
from kivy.app import App
from kivy.uix.gridlayout import GridLayout


class Tile(Button):
    def click(self):
        print("tile clicked")


class MainGrid(GridLayout):
    def setupGrid(self):
        self.ids.snakeGrid.cols = self.sizeOfGrid
        for i in range(self.sizeOfGrid):
            for j in range(self.sizeOfGrid):
                self.ids.snakeGrid.add_widget(Tile())







class SnakeApp(App):
    def build(self):
        return MainGrid()
    
if __name__ == "__main__":
    SnakeApp().run()