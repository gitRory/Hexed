from dataclasses import dataclass, field, asdict
import arcade
import screeninfo
import board
import random

local_packet_sprite_lists= {'trail_particles_sprite_list':None,
                            'packet_sprite_list':None,
                            'node_sprite_list': None
                            }

#layers={'Physical':None,'Data_Link':None,'Network':None,'Transport':None,'Application':[{'Session layer':None},{'Presentation layer':None}]
#playable area of each layer defined by ["max_x","max_y","hop_size"]
layers={'Physical':"None",
        'Data_Link':None,
        'Network':None,
        'Transport':None,
        'Application':[{'Session layer':None},
                       {'Presentation layer':None
                        }
                       ]
        }


node_png=[
    {'name':'edge',
     'path':"C:/Users/User/OneDrive/Documents/coding/python/playground/hexed/spriteimg/node_1.png"},
    {'name':'centre',
     'path':"C:/Users/User/OneDrive/Documents/coding/python/playground/hexed/spriteimg/node_2.png"}
    ]

packet_png=[
    {'name':'default',
     'path':"C:/Users/User/OneDrive/Documents/coding/python/playground/hexed/spriteimg/sprite_1.png"},
    {'name':'hunter',
     'path':"C:/Users/User/OneDrive/Documents/coding/python/playground/hexed/spriteimg/sprite_2.png"},
    {'name':'bloom',
     'path':"C:/Users/User/OneDrive/Documents/coding/python/playground/hexed/spriteimg/sprite_3.png"}
          ]





class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        super().__init__(
            screeninfo.get_monitors()[0].width,
            screeninfo.get_monitors()[0].height,
            "Hexed")    #todo make this work with multiscreen
        
        self.set_mouse_visible(False)
        self.background_color=arcade.color.BLACK
        self.node_sprite_list:board.BoardObjectCluster
        self.packet_sprite_list= arcade.SpriteList()

    def setup(self):  
        arcade.set_background_color(self.background_color)
        #todomake a def layer builder/logic
        node= board.BoardObject(texture_paths=node_png,family='node')
        self.node_sprite_list=board.BoardObjectCluster.create_cluster(
            node,
            cluster_size_of_x=10,
            cluster_size_of_y=10
            )
        

    def on_draw(self):
        arcade.start_render()
        self.node_sprite_list.draw()
        self.packet_sprite_list.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called whenever the mouse button is clicked.
        """
        
        pod=board.Packet.post_office(
            texture_path=packet_png,
            creator= self.node_sprite_list[random.randint(0,self.node_sprite_list.__sizeof__())],
            destination=self.node_sprite_list[random.randint(0,self.node_sprite_list.__sizeof__())],
            emit_type=packet_png[1]['name']
            )
        self.packet_sprite_list.append(pod)


    def update(self, delta_time):
        """ Movement and game logic """

        self.node_sprite_list.update()
        self.packet_sprite_list.update()