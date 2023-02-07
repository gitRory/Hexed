import arcade
import gameinstance
  
def main():
    window = gameinstance.MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()