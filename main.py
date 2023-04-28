import arcade
import arcade.gui
from arcade.gui.events import UIOnClickEvent
import game


class QuitButton(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        arcade.exit()
launch_check=game.launch
class MyWindow(arcade.Window):
    
    def __init__(self):
        
        super().__init__(800, 600, "Далекий Космос", resizable=True)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

       
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        
       
        self.v_box = arcade.gui.UIBoxLayout()
        
        settings_button = arcade.gui.UIFlatButton(text="Начать игру", width=200)
        self.v_box.add(settings_button.with_space_around(bottom=20))
        settings_button.on_click = self.on_click_launch
        
        
        
        
        
        quit_button = QuitButton(text="Выход", width=200)
        self.v_box.add(quit_button)
        open_message_box_button = arcade.gui.UITextureButton(widht=200,hight=200,texture=arcade.load_texture(":resources:images/items/flagRed2.png"))
        open_message_box_button.on_click = self.on_click_open
        self.v_box.add(open_message_box_button)
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )
    def on_click_open(self, event: arcade.gui.UIOnClickEvent):
                message_box = arcade.gui.UIMessageBox(
                width=300,
                height=200,
                message_text=(
                "Добро пожаловать в игру 'Далекий Космос'. Чтобы двигаться используйте стрелочки, а чтобы стрелять используйте пробел"
             ),
                callback=self.on_message_box_close,
                buttons=["Ok"]
            )
                self.manager.add(message_box)
    def on_click_launch(self, event: arcade.gui.UIOnClickEvent):
        launch_check=True
        arcade.close_window() 
        
        
    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_message_box_close(self, button_text):
        print(f"User pressed {button_text}.")

    
window = MyWindow()
arcade.run()

Screen_widht=1000
Screen_hight=800
Screen_title="Далекий Космос"
