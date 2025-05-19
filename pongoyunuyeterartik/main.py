import json
import subprocess

from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen


Builder.load_file("interface.kv")

class MainMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sound = SoundLoader.load("oyununarayüzsesi.mp3")
        if self.sound:
            self.sound.loop = True
            self.sound.volume = 0.5
            self.sound.play()
    def start_server(self):
        subprocess.Popen(["python", "server.py"])
    def join_online_game(self):
        if self.sound:
            self.sound.stop()
        choosemodescreen = self.manager.get_screen("modescreen")
        self.manager.current="modescreen"
    def playoffline(self):
        subprocess.Popen(["python","offline.py"])
        if self.sound:
            self.sound.stop()
        self._play_game_music()
        subprocess.Popen(["python", "client.py"])
    def show_all_match(self):
        file = "keep_score.json"
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            data = {"player1": 0, "player2": 0}
        history_screen = self.manager.get_screen("history")
        history_screen.ids.player1.text = f"Player 1 wins = {data['player1']}"
        history_screen.ids.player2.text = f"Player 2 wins = {data['player2']}"
        self.manager.current = "history"

class HistoryScreen(Screen):
    def go_back(self):
        self.manager.current = "menu"


class ChooseModeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sound = None

    def _play_game_music(self, file):
        if self.sound:
            self.sound.stop()
        self.sound = SoundLoader.load(file)
        if self.sound:
            self.sound.loop = True
            self.sound.volume = 0.5
            self.sound.play()
    def startnormalmode(self):
        self._play_game_music("oyununoyunsesi.mp3")
        subprocess.Popen(["python", "client.py"])
    def startgsmode(self):
        self._play_game_music("Galatasaray Senfonisi (1).mp3")
        subprocess.Popen(["python", "clientgs.py"])
    def startfbmode(self):
        self._play_game_music("Mohikan Marşı _ FENERBAHÇE (1).mp3")
        subprocess.Popen(["python", "clientfb.py"])

class PongApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        sm = ScreenManager()
        sm.add_widget(MainMenu(name="menu"))
        sm.add_widget(HistoryScreen(name="history"))
        sm.add_widget(ChooseModeScreen(name="modescreen"))
        return sm

if __name__ == '__main__':
    PongApp().run()
