from dataclasses import dataclass, field, asdict
import arcade
import screeninfo
import board


local_packet_sprite_lists= {'trail_particles_sprite_list':None,'packet_sprite_list':None, 'node_sprite_list': None}

#layers={'Physical':None,'Data_Link':None,'Network':None,'Transport':None,'Application':[{'Session layer':None},{'Presentation layer':None}]
#playable area of each layer defined by ["max_x","max_y","hop_size"]
layers={'Physical':"None",'Data_Link':None,'Network':None,'Transport':None,'Application':[{'Session layer':None},{'Presentation layer':None}]
        }


node_png=[{'name':'edge','path':"C:/Users/User/OneDrive/Documents/coding/python/playground/hexed/spriteimg/node_1.png"},
          {'name':'centre','path':"C:/Users/User/OneDrive/Documents/coding/python/playground/hexed/spriteimg/node_2.png"}]

packet_png={0:"C:/Users/User/OneDrive/Documents/coding/python/playground/hexed/spriteimg/sprite_1.png",
          1:"C:/Users/User/OneDrive/Documents/coding/python/playground/hexed/spriteimg/sprite_2.png",
          2:"C:/Users/User/OneDrive/Documents/coding/python/playground/hexed/spriteimg/sprite_3.png"}





class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self,sprite_data):
        super().__init__(
            screeninfo.get_monitors()[0].width,
            screeninfo.get_monitors()[0].height,
            "Hexed")    #todo make this work with multiscreen
        
        self.set_mouse_visible(False)
        self.background_color=arcade.color.BLACK
        #self.node_sprite_list=None
        

    def setup(self):

        #todomake a def layer builder/logic
        node= board.BoardObject(node_png,family='node')
        self.node_sprite_list=board.BoardObjectCluster.create_cluster(node,cluster_size_of_x=10,cluster_size_of_y=10)

        arcade.set_background_color(self.background_color)

    def on_draw(self):
        arcade.start_render()
        self.node_sprite_list.draw()
        

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called whenever the mouse button is clicked.
        """

    def update(self, delta_time):
        """ Movement and game logic """
        
        self.node_sprite_list.update