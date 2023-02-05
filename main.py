import arcade
import gameinstance
  
def main():
    window = gameinstance.MyGame(gameinstance.local_packet_sprite_lists)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()