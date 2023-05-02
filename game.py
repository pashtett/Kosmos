import arcade
import arcade.gui
import math
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Далекий космос"
CHARACTER_SCALING = 0.6
TILE_SCALING = 0.5
MOVEMENT_SPEED = 5
class TurningSprite(arcade.Sprite):
    def update(self):
        super().update()
        self.angle = math.degrees(math.atan2(self.change_y, self.change_x))
class Player(arcade.Sprite):
    def __init__(self, filename, scale):
        super().__init__(filename,scale)
        self.thrust = 0
        self.speed = 0
        self.max_speed = 4
        self.drag = 0.05
        self.respawning = 0 
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
                 
    

class MyGame(arcade.Window):


    def __init__(self):

        
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.csscolor.NAVY)
        self.player_list= None
        self.player_sprite = None
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

    def setup(self):
        self.player_list = arcade.SpriteList()
        image_source= ":resources:images/space_shooter/playerShip1_blue.png"
        self.player_sprite= Player(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 100
        self.player_list.append(self.player_sprite)
    def on_draw(self):
        self.clear()
        self.player_list.draw()
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

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update to move the sprite
        # If using a physics engine, call update player to rely on physics engine
        # for movement, and call physics engine here.
        self.player_list.update()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.LEFT:
            self.player_sprite.change_angle = 3
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_angle = -3
        elif key == arcade.key.UP:
            self.player_sprite.thrust = 0.15
        elif key == arcade.key.DOWN:
            self.player_sprite.thrust = -.2

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.LEFT:
            self.player_sprite.change_angle = 0
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_angle = 0
        elif key == arcade.key.UP:
            self.player_sprite.thrust = 0
        elif key == arcade.key.DOWN:
            self.player_sprite.thrust = 0
     


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()