import copy
#######data####
#!migrate to JSON

############333
import arcade as ar
import random
import numpy as np
import PIL

#?import pymunk use this with arcade.PyMunk maybe
#***************************************************
class BoardObject(ar.AnimatedTimeBasedSprite):
    """if interacts on the board, it's one of these."""
    def __init__(
        self,
        texture_paths: list,
        scale: float = 1,
        image_x: float = 0,
        image_y: float = 0,
        image_width: float = 0,
        image_height: float = 0,
        center_x: float = 0,
        center_y: float = 0,
        family: str = None,
        health: float = 60,
    ):
        super().__init__(
            filename=texture_paths[0]['path'],
            scale=scale,
            image_x=image_x,
            image_y=image_y,
            image_width=image_width,
            image_height=image_height,
            center_x=center_x,
            center_y=center_y,
        )
        self.family = family
        self.health = health
        self.frames= self.rigged(texture_paths)

    @classmethod       
    def rigged(cls, texture_paths):
        frames = []
        for texture in texture_paths:
            frames.append(ar.AnimationKeyframe(
                tile_id=texture['name'],
                duration=30,
                texture=ar.texture.load_texture(
                    texture['path']
                    )
                )
            )
        return frames  


#***************************************************

class BoardObjectCluster(ar.SpriteList):
    def __init__(
        self,
        object_sprite: BoardObject,
        cluster_size_of_x: int,
        cluster_size_of_y: int,
        cluster_type:str= "undefined",
        ):
        self.cluster_type = cluster_type
        self.clustx=cluster_size_of_x 
        self.clusty=cluster_size_of_y  
        self.cluster_size = cluster_size_of_x * cluster_size_of_y
        self.object_sprite = object_sprite
        super().__init__(capacity=self.cluster_size)

    def create_cluster(board_object,cluster_size_of_x,cluster_size_of_y)-> object:
        
        cluster_type=board_object.family
        new_cluster=BoardObjectCluster(
        object_sprite=board_object,
        cluster_type=cluster_type,
        cluster_size_of_x=cluster_size_of_x,
        cluster_size_of_y=cluster_size_of_y
        )
        
        for index in range(new_cluster.cluster_size):
            sprite=copy.deepcopy(board_object)
            if cluster_type== 'node':
                xpos=index%new_cluster.clustx
                ypos=index//new_cluster.clusty
                if ypos%2==0:
                    sprite.center_x=xpos*board_object.health
                else:                  
                    sprite.center_x=(xpos*board_object.health)+board_object.health/2
                sprite.center_y=ypos*board_object.health* 0.8660 #YHEXOFFSET=np.sqrt(3) / 2 apporxi
                
                if (ypos%2==0 and xpos%3==1) or (ypos%2!=0 and xpos%3==2):
                     sprite.texture =  new_cluster.object_sprite.frames[1].texture
            new_cluster.append(sprite)
        return new_cluster
        
    def update_packets(self,sprite_list=ar.SpriteList):
        for sprite in sprite_list[:]:
                    sprite_list.health -= 1
                    if sprite.health <= 0 or sprite.alpha <= 0:
                        sprite_list.remove(sprite)
                    else:
                        sprite.alpha *= 0.999
                        sprite.scale = sprite.health / self.health
                        sprite.center_x += sprite.change_x
                        sprite.center_y += sprite.change_y

    def update(self) -> None:
        if self.object_sprite==Packet:
            self.update_packets(self)
            if self.object_sprite.health % self.object_sprite.trail_interval == 0:
                self.object_sprite.emit_packet(target=self.object_sprite.history[-1])
            if self.object_sprite.has_trail:
                self.update_packets(self.object_sprite.trail_sprites)
        else:
            super().update()

#***************************************************
#! remove nodes based on trigger
class Packet(BoardObject):
    def __init__(
        self,
        texture_paths: dict,
        scale: float = 0.5,
        image_x: float = 0,
        image_y: float = 0,
        image_width: float = 0,
        image_height: float = 0,
        center_x: float = 0,
        center_y: float = 0,
        speed: int= 2,
        health: float= 60,
        emission_rate: int= 1,
        trail_sprites: BoardObjectCluster=None,
        packet_type: str = None,
        emit_type: str= None,
                
        ):
        super().__init__(
            filename=texture_paths[0],
            scale=scale,
            image_x=image_x,
            image_y=image_y,
            image_width=image_width,
            image_height=image_height,
            center_x=center_x,
            center_y=center_y,
            health= health,
            texture_paths= texture_paths,
            packet_type=packet_type,
        )
        self.speed=speed 
        self.history:list=[] #spritelist
        self.payload: list = []
        self.capacity: int= 0
        self.emission_rate = emission_rate        
        self.trail_interval = self.speed*2 
        self.trail_sprites = trail_sprites #spritelist
        self.has_trail=False
        self.emit_types={0: "undefined",1:"plain",2:"bloom",3:"hunter",4:"detour"}
        self.emit_type =emit_type or self.packet_types[0]

    def rando_vector(speed=None,angle=None):
        if speed is not None:
            speed=random.uniform(-speed, speed)
        if angle is not None:
            angle=random.uniform(0,360)
        return {'magnitude':speed,'direction':angle}

    def disco_packet():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    def get_key(dict,vaule):
        return list(filter(lambda x: dict[x] == vaule, dict))[0]
    def emit_packet(self,target=None)->None:
            if self.get_key(self.packet_type)==0:
                pass
            elif self.get_key(self.packet_type
                              )<=3 and target==None:
                self.change_x = self.rando_vector(
                    self.speed)['magnitude']
                self.change_y = self.rando_vector(
                    self.speed)['magnitude']
                
                if self.get_key(self.packet_type)==2:
                    self.rando_vector(angle=1)['direction']
                    self.speed = self.rando_vector(
                        self.speed)['magnitude']
            elif self.get_key(self.packet_type)==3:
                if not(ar.check_for_collision(self, target)):
                    angle = np.arctan2(
                        target.center_y - self.center_y,
                        target.center_x - self.center_x
                        )
                    self.change_x = self.speed * np.cos(angle)
                    self.change_y = self.speed * np.sin(angle)
                else:
                    self.change_x = 0
                    self.change_y = 0
                    self.history.append(target)

#!move this to fog o war when needed?           
    def change_sprite_visibility(self, sprite, distance_threshold):
        
        packet_position = np.array([self.center_x, self.center_y])
        sprite_position = np.array([sprite.center_x, sprite.center_y])
        # Calculate the Euclidean distance between the packet and sprite
        distance = np.linalg.norm(packet_position - sprite_position)
        # Check if the distance is less than the distance threshold
        sprite.visible=True if distance < distance_threshold else False
#***************************************************