import arcade
from arcade.application import Window
import arcade.gui
import math
import random
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Далекий космос"
CHARACTER_SCALING = 0.6
TILE_SCALING = 0.5
MOVEMENT_SPEED = 5
PLAYER_HEALTH=50
BULLET_DAMAGE=10
INDICATOR_BAR_OFFSET=32
SPRITE_SCALING_LASER=0.8
BULLET_SPEED=8

class TurningSprite(arcade.Sprite):
    def update(self):
        super().update()
        self.angle = math.degrees(math.atan2(self.change_y, self.change_x))
class Player(arcade.Sprite):
    def __init__(self, filename, scale,bar_list:arcade.SpriteList):
        super().__init__(filename,scale)
        self.thrust = 0
        self.speed = 0
        self.max_speed = 4
        self.drag = 0.05
        self.indicator_bar: IndicatorBar = IndicatorBar(
            self, bar_list,(self.center_x,self.center_y)
        )
        self.health:int=PLAYER_HEALTH
    def update(self):
        if self.speed > 0:
            self.speed -= self.drag
            if self.speed < 0:
                self.speed = 0

        if self.speed < 0:
            self.speed += self.drag
            if self.speed > 0:
                self.speed = 0

        self.speed += self.thrust
        if self.speed > self.max_speed:
            self.speed = self.max_speed
        if self.speed < -self.max_speed:
            self.speed = -self.max_speed

        self.change_x = -math.sin(math.radians(self.angle)) * self.speed
        self.change_y = math.cos(math.radians(self.angle)) * self.speed
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.right < 0:
            self.left = SCREEN_WIDTH

        if self.left > SCREEN_WIDTH:
            self.right = 0

        if self.bottom < 0:
            self.top = SCREEN_HEIGHT

        if self.top > SCREEN_HEIGHT:
            self.bottom = 0
        super().update()
class IndicatorBar:
    def __init__(self,
        owner: Player,
        sprite_list: arcade.SpriteList,
        position: tuple[float, float] = (0, 0),
        full_color: arcade.Color = arcade.color.GREEN,
        background_color: arcade.Color = arcade.color.BLACK,
        width: int = 100,
        height: int = 4,
        border_size: int = 4,
    ) -> None:
        # Store the reference to the owner and the sprite list
        self.owner: Player = owner
        self.sprite_list: arcade.SpriteList = sprite_list

        # Set the needed size variables
        self._box_width: int = width
        self._box_height: int = height
        self._half_box_width: int = self._box_width // 2
        self._center_x: float = 0.0
        self._center_y: float = 0.0
        self._fullness: float = 0.0

        # Create the boxes needed to represent the indicator bar
        self._background_box: arcade.SpriteSolidColor = arcade.SpriteSolidColor(
            self._box_width + border_size,
            self._box_height + border_size,
            background_color,
        )
        self._full_box: arcade.SpriteSolidColor = arcade.SpriteSolidColor(
            self._box_width,
            self._box_height,
            full_color,
        )
        self.sprite_list.append(self._background_box)
        self.sprite_list.append(self._full_box)

        # Set the fullness and position of the bar
        self.fullness: float = 1.0
        self.position: tuple[float, float] = position
        def __repr__(self) -> str:
            return f"<IndicatorBar (Owner={self.owner})>"

    @property
    def background_box(self) -> arcade.SpriteSolidColor:
        """Returns the background box of the indicator bar."""
        return self._background_box

    @property
    def full_box(self) -> arcade.SpriteSolidColor:
        """Returns the full box of the indicator bar."""
        return self._full_box

    @property
    def fullness(self) -> float:
        """Returns the fullness of the bar."""
        return self._fullness

    @fullness.setter
    def fullness(self, new_fullness: float) -> None:
        """Sets the fullness of the bar."""
        # Check if new_fullness if valid
        if not (0.0 <= new_fullness <= 10.0):
            raise ValueError(
                f"Got {new_fullness}, but fullness must be between 0.0 and 1.0."
            )

        # Set the size of the bar
        self._fullness = new_fullness
        if new_fullness == 0.0:
            # Set the full_box to not be visible since it is not full anymore
            self.full_box.visible = False
        else:
            # Set the full_box to be visible incase it wasn't then update the bar
            self.full_box.visible = True
            self.full_box.width = self._box_width * new_fullness
            self.full_box.left = self._center_x - (self._box_width // 2)

    @property
    def position(self) -> tuple[float, float]:
        """Returns the current position of the bar."""
        return self._center_x, self._center_y

    @position.setter
    def position(self, new_position: tuple[float, float]) -> None:
        """Sets the new position of the bar."""
        # Check if the position has changed. If so, change the bar's position
        if new_position != self.position:
            self._center_x, self._center_y = new_position
            self.background_box.position = new_position
            self.full_box.position = new_position

            # Make sure full_box is to the left of the bar instead of the middle
            self.full_box.left = self._center_x - (self._box_width // 2)

class GameOver(arcade.View):
    def __init__(self):
        super().__init__()
        self.texture =arcade.load_texture("fotka")
        arcade.set_viewport(0, SCREEN_WIDTH -1, 0, SCREEN_HEIGHT -1)
    def on_draw(self):
        self.clear()
        self.texture.draw_sized(SCREEN_WIDTH /2, SCREEN_HEIGHT /2,
                                SCREEN_WIDTH, SCREEN_HEIGHT)
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view=GameView()
        game_view.setup()
        self.window.show_view(game_view)   


class GameView(arcade.View):


    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.csscolor.NAVY)
        self.player_list= None
        self.player_sprite = None
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.bullet_list=None
        self.bar_list=None
        self.planet_list=None
        self.planet_sprite=None

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.bullet_list=arcade.SpriteList()
        self.bar_list=arcade.SpriteList()
        self.planet_list=arcade.SpriteList()
        
        
        image_source= ":resources:images/space_shooter/playerShip1_blue.png"
        self.player_sprite= Player(image_source, CHARACTER_SCALING,self.bar_list)
        self.player_sprite.center_x =400
        self.player_sprite.center_y =400
        self.player_list.append(self.player_sprite)
        image=":resources:images/space_shooter/meteorGrey_big2.png"
        planet=arcade.Sprite(image,CHARACTER_SCALING)
        planet.center_x=random.randrange(SCREEN_WIDTH)
        planet.center_y= random.randrange(130,SCREEN_WIDTH)
        self.planet_list.append(planet)
    def on_draw(self):
        self.clear()
        self.planet_list.draw()
        self.player_list.draw()
        self.bullet_list.draw()
        self.bar_list.draw()
    def update_player_speed(self):

        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = MOVEMENT_SPEED
        
    def on_key_press(self, key, modifiers):
        if key==arcade.key.SPACE:
            bullet_sprite = TurningSprite(":resources:images/space_shooter/"
                                          "laserBlue01.png",
                                          SPRITE_SCALING_LASER)
            bullet_sprite.guid = "Bullet"

            bullet_speed = 13
            bullet_sprite.change_y = \
                math.cos(math.radians(self.player_sprite.angle)) * bullet_speed
            bullet_sprite.change_x = \
                -math.sin(math.radians(self.player_sprite.angle)) \
                * bullet_speed

            bullet_sprite.center_x = self.player_sprite.center_x
            bullet_sprite.center_y = self.player_sprite.center_y
            bullet_sprite.update()
            self.bullet_list.append(bullet_sprite)
        
        if key == arcade.key.LEFT:
            self.player_sprite.change_angle = 3
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_angle = -3
        elif key == arcade.key.UP:
            self.player_sprite.thrust = 0.15
        elif key == arcade.key.DOWN:
            self.player_sprite.thrust = -.2
        if self.player_sprite.forward !=0:
                self.player_sprite.health -= 0.5
                self.player_sprite.indicator_bar.fullness = (
                self.player_sprite.health / PLAYER_HEALTH
        )
                print(self.player_sprite.health)
        
        
        

    def on_key_release(self, key, modifiers):

        if key == arcade.key.LEFT:
            self.player_sprite.change_angle = 0
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_angle = 0
        elif key == arcade.key.UP:
            self.player_sprite.thrust = 0
        elif key == arcade.key.DOWN:
            self.player_sprite.thrust = 0
        
    def on_update(self, delta_time):
   
        self.bullet_list.update()
        self.player_list.update()
        self.player_sprite.indicator_bar.position=(
            self.player_sprite.center_x,
            self.player_sprite.center_y +INDICATOR_BAR_OFFSET     
        )
        if self.player_sprite.health > 50:
                self.player_sprite.health = 50
        for bullet in self.bullet_list:
            size = max(bullet.width, bullet.height)
            if bullet.center_x < 0 - size:
                    bullet.remove_from_sprite_lists()
            if bullet.center_x > SCREEN_WIDTH + size:
                    bullet.remove_from_sprite_lists()
            if bullet.center_y < 0 - size:
                    bullet.remove_from_sprite_lists()
            if bullet.center_y > SCREEN_HEIGHT + size:
                    bullet.remove_from_sprite_lists()
        for planet in self.planet_list:
            size = max(planet.width, planet.height)
            hit_list=arcade.check_for_collision_with_list(self.player_sprite, self.planet_list)
            if len (hit_list) >0:
                self.player_sprite.health += 0.5
                self.player_sprite.indicator_bar.fullness = (
                self.player_sprite.health / PLAYER_HEALTH
                )
            
           
            
        

    
class QuitButton(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        arcade.exit()
class StartView(arcade.View):
    
    def __init__(self):
        
        super().__init__()

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
        game_view=GameView()
        game_view.setup()
        self.window.show_view(game_view)
        
        
    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_message_box_close(self, button_text):
        print(f"User pressed {button_text}.")    


def main():
    window = arcade.Window(SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE)
    start_view=StartView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()