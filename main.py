import arcade
import screeninfo
import board
import gameinstance
  
def main():
    window = arcade.MyGame(gameinstance.local_packet_sprite_lists)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()