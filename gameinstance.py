from dataclasses import dataclass, field, asdict
import arcade
import screeninfo


local_packet_sprite_lists= {'trail_particles_sprite_list':None,'packet_sprite_list':None, 'node_sprite_list': None}

#layers={'Physical':None,'Data_Link':None,'Network':None,'Transport':None,'Application':[{'Session layer':None},{'Presentation layer':None}]
#playable area of each layer defined by ["max_x","max_y","hop_size"]
layers={'Physical':"None",'Data_Link':None,'Network':None,'Transport':None,'Application':[{'Session layer':None},{'Presentation layer':None}]
        }


node_png={0:"C:/Users/User/OneDrive/Documents/coding/python/playground/hexed/spriteimg/node_1.png",
          1:"C:/Users/User/OneDrive/Documents/coding/python/playground/hexed/spriteimg/node_2.png"}

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
        self.sprite_data=sprite_data
        for each in sprite_data.keys():
            setattr(self, each, sprite_data[each])
        self.set_mouse_visible(False)
        self.background_color=arcade.color.BLACK
        
        self.node_sprite_list=BoardObjectCluster(
                object_sprite=BoardObject(node_png),
                cluster_size_of_x=10,cluster_size_of_y=10)
        self.node_sprite_list.make_hex_pattern()

    def setup(self):

        #todomake a def layer builder/logic
        
        # packet lists
        self.populate_class_packet_lists()
        self.node_sprite_list=board.BoardObjectCluster(
        object_sprite=board.BoardObject(node_png),
        cluster_size_of_x=10,cluster_size_of_y=10)
        self.node_sprite_list.make_hex_pattern()
        # Set the background color
        arcade.set_background_color(self.background_color)

    def on_draw(self):
        arcade.start_render()
        
        self.draw_class_packet_lists()

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called whenever the mouse button is clicked.
        """

    def update(self, delta_time):
        """ Movement and game logic """
        # Call update on all sprites
        
      
        #self.update_class_packet_lists()
        
    
    @classmethod
    def populate_class_packet_lists(cls):
        attributes = [
            attribute for attribute in cls.__dict__.keys(
                ) if "sprite_list" in attribute
            ]
        for each in attributes:
            setattr(cls, each, 
                    board.BoardObjectCluster(texture_paths=packet_png,
                                            object_sprite=board.Packet(
                                                trail_sprites=getattr(cls, "trail_particles_sprite_list"),
                                                texture_paths=packet_png),
                                            cluster_size_of_x=1,cluster_size_of_y=1
                                            )
                    )

    @classmethod
    def update_class_packet_lists(cls):
        attributes = [
            attribute for attribute in cls.__dict__.keys(
                ) if "sprite_list" in attribute
            ]
        for each in attributes:
                getattr(cls,each).update()
    @classmethod
    def draw_class_packet_lists(cls):
        attributes = [
            attribute for attribute in cls.__dict__.keys(
                ) if "sprite_list" in attribute
            ]
        for each in attributes:
                getattr(cls,each).draw()