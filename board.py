import copy
#######data####
#!migrate to JSON

############333
import arcade as ar
import random
import numpy as np
import struct


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
        super().__init__(capacity=self.cluster_size,use_spatial_hash=True)

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
                     sprite.family= "centre_node"
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
            if self.object_sprite.family!="centre_node":
                self.object_sprite.visible=False
            super().update()

#***************************************************
#! remove nodes based on trigger add header to packet
class Packet(BoardObject):
    def __init__(
        self,
        texture_paths: list,
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
        emit_type: str= None,
                
        ):
        super().__init__(
            scale=scale,
            image_x=image_x,
            image_y=image_y,
            image_width=image_width,
            image_height=image_height,
            center_x=center_x,
            center_y=center_y,
            health= health,
            texture_paths= texture_paths,
            family='packet'
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
        self.emit_type =emit_type or self.emit_types[0]

    def header(self):
        pass
    def post_office(
        texture_path:list,
        creator:BoardObject,
        destination:BoardObject,
        emit_type:str):
        
        outbox= Packet(texture_paths=texture_path,
                       center_x=creator.center_x,
                       center_y=creator.center_y,
                       emit_type=emit_type                       
                       )
        
        outbox._emit_packet(target=destination)
        return outbox

    def _rando_vector(speed=None,angle=None):
        if speed is not None:
            speed=random.uniform(-speed, speed)
        if angle is not None:
            angle=random.uniform(0,360)
        return {'magnitude':speed,'direction':angle}

    def _disco_packet():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def _get_key(self,value):
        for key, val in self.emit_types.items():
            if val == value:
                return key
        return 0#default

    def _emit_packet(self,target=None)->None:
            if self._get_key(self.emit_type)==0:
                pass
            elif self._get_key(self.emit_type
                              )<=3 and target==None:
                self.change_x = self.rando_vector(
                    self.speed)['magnitude']
                self.change_y = self.rando_vector(
                    self.speed)['magnitude']
                
                if self._get_key(self.emit_type)==2:
                    self._rando_vector(angle=1)['direction']
                    self.speed = self.rando_vector(
                        self.speed)['magnitude']
            elif self._get_key(self.emit_type)==3:
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
                    

    def _displacement(self, next_hop=BoardObject, final_hop=BoardObject,layer_nodes=BoardObjectCluster)->dict:
        '''this needs work reckon could make it cleaner with maths...but sleep'''
        nh_pos=[]
        fh_pos=[]
        #!need exception blah blah blagh
        for index in layer_nodes:
            if layer_nodes[index].center_x==next_hop.center_x and layer_nodes[index].center_y==next_hop.center_y:
                nh_pos= [index,index%layer_nodes.clustx,index//layer_nodes.clusty]
                nh_index=index
            if layer_nodes[index].center_x==final_hop.center_x and layer_nodes[index].center_y==final_hop.center_y:
                fh_pos=[index,index%layer_nodes.clustx,index//layer_nodes.clusty]
        return {"nhindex":nh_index,"i_dp":fh_pos[0]-nh_pos[0],"x_dp":fh_pos[1]-nh_pos[1],"y_dp":fh_pos[2]-nh_pos[2]}
    
    def next_node(self,final_hop=BoardObject,layer_nodes=BoardObjectCluster)->BoardObject:
        
        
                
        
        possible_hop=ar.SpriteList()
        #! this be the place to fix
        
        
        
        possible_hop.extend(get_nearby_sprites(self,layer_nodes)) 
        possible_hop_dp=[]
        for sprite in possible_hop.__iter__():
            if sprite.family=="centre_node":
                possible_hop.remove(sprite)
            else:
                possible_hop_dp.append(self.displacement(sprite,final_hop,layer_nodes))
        sorted(possible_hop_dp, key=lambda x: (x['x_dp'], x['y_dp']))
        print(possible_hop_dp)
        result= layer_nodes[possible_hop_dp[0]['nhindex']] or None
        return result

#!move this to fog o war when needed?           
    def change_sprite_visibility(self, sprite, distance_threshold):
        
        packet_position = np.array([self.center_x, self.center_y])
        sprite_position = np.array([sprite.center_x, sprite.center_y])
        # Calculate the Euclidean distance between the packet and sprite
        distance = np.linalg.norm(packet_position - sprite_position)
        # Check if the distance is less than the distance threshold
        sprite.visible=True if distance < distance_threshold else False
#***************************************************

