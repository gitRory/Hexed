

#######data####
#!migrate to JSON

YHEXOFFSET= 0.8660 #np.sqrt(3) / 2 apporxi

############333
import arcade as ar
import random
import numpy as np

#?import pymunk use this with arcade.PyMunk maybe
#***************************************************
class BoardObject(ar.AnimatedTimeBasedSprite):
    """if interacts on the board, it's one of these."""
    def __init__(
        self,
        texture_paths: dict,
        scale: float = 1,
        image_x: float = 0,
        image_y: float = 0,
        image_width: float = 0,
        image_height: float = 0,
        center_x: float = 0,
        center_y: float = 0,
        health: float= 50,
                
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
            
        )
        self.health= health
        self.texture_paths= texture_paths
#***************************************************

class BoardObjectCluster(ar.SpriteList):
    def __init__(
        self,
        cluster_type:str= "undefined",
        cluster_size_of_x: int =1,
        cluster_size_of_y: int =1,
        object_sprite: BoardObject= None,
        ):
        self.cluster_type = cluster_type
        self.clustx=cluster_size_of_x
        self.clusty=cluster_size_of_y
        self.cluster_size = cluster_size_of_x * cluster_size_of_y
        self.object_sprite = object_sprite
        super().__init__(capacity=self.cluster_size)


    def create_cluster(self,board_object=BoardObject,cluster_size=int):
        try:
            cluster_type=board_object.packet_type
        except ValueError:
            print("oops")
        else:
            cluster_type=board_object.__name__
        new_cluster=BoardObjectCluster(
            cluster_type=cluster_type,
            object_sprite=board_object,
            cluster_size=cluster_size
            )
        for _ in range(cluster_size):
            new_cluster.append(new_cluster.object_sprite)
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
            return super().update()
 

    def make_hex_pattern(self):
        x, y = 0, 0
        for i in range(self.clusty):
            if i % 2 == 0:
                x = self.object_sprite.health / 2
            else:
                x = 0
            for _ in range(self.clustx):
                self.object_sprite.center_x = x
                self.object_sprite.center_y = y
                for _ in range(len(self)):
                    self.append(self.object_sprite.__class__(**{k: v for k, v in vars(self.object_sprite).items() if k != "_width"}))

                x += self.object_sprite.health
            y += self.object_sprite.health * YHEXOFFSET

    # def make_hex_pattern(self):
    #     nodes=BoardObjectCluster()
    #     x,y,yobj,xobj=0,0,0,0
    #     for _ in range(self.clusty*self.clustx):
    #         nodes.append(copy.deepcopy(self.object_sprite))
    #     for index,sprite in enumerate(nodes):
    #         if xobj== self.clustx-1:
    #             yobj+=1
    #         xobj=index%self.clustx
    #         if xobj==0:
    #             if yobj % 2 == 0:
    #                 x= (self.object_sprite.health / 2)
    #             else:
    #                 x = 0
    #         if ((xobj % 2 == 0 and yobj % 3 == 1) or
    #         (xobj % 2 != 0 and yobj % 3 == 2)):
    #             sprite.texture = \
    #                 ar.load_texture(self.object_sprite.texture_paths[1])
    #         sprite.center_x=x
    #         sprite.center_y=y
    #         y+= self.object_sprite.health * YHEXOFFSET
    #         x+= self.object_sprite.health
    #     return nodes



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
        packet_type: str = None
                
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
        )
        self.speed=speed 
        self.history:list=[] #spritelist
        self.payload: list = []
        self.capacity: int= 0
        self.emission_rate = emission_rate        
        self.trail_interval = self.speed*2 
        self.trail_sprites = trail_sprites #spritelist
        self.has_trail=False
        self.packet_types={0: "undefined",1:"plain",2:"bloom",3:"hunter",4:"detour"}
        self.packet_type =packet_type or self.packet_types[0]

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