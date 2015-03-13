import sys,pygame,random,pygame.time
import copy
black=0,0,0
white=255,255,255
red=255,0,0
green=0,255,0
blue=0,0,255
pygame.mixer.pre_init()

pygame.init()
screen=pygame.display.set_mode((640,480))
#bottom=[]
#screen_width=640
#screen_height=480
true=True
false=False
#move_left=false
#move_right=false
#move_down=false
#block_size=20
#height=480/block_size
#offset=480/2-50
block_screen=[]
#width=10
#move_left=false
#move_right=false
#move_down=false
#rot_block=false
#game_over=false
#enter_high_score=false
def copy_array(ar):
    return copy.deepcopy(ar)
class core_state:
	def __init__(self):
		self.screen_width=640
		self.screen_height=480
		#self.move_left=false
		#self.move_right=false
		#self.move_down=false
		self.block_size=20
		self.height=480/self.block_size
		self.offset=480/2-50
		self.width=10
		self.move_left=false
		self.move_right=false
		self.move_down=false
		self.rot_block=false
		self.game_over=false
		self.enter_high_score=false
		self.level=0
Core_State=core_state()
State=Core_State
for i in range(State.width*State.height):
    block_screen.append((false,255))
#for i in range(width):
#    bottom.append(height)
def convert_pixel_pos(pos):
	return (pos[0]*State.block_size+State.offset,pos[1]*State.block_size)
def display_small_block(pos,color):
    pixel_pos=(pos[0]*State.block_size+State.offset,pos[1]*State.block_size)
    rect=pygame.Rect(pixel_pos,(State.block_size,State.block_size))
    pygame.draw.rect(screen,color,rect)
textured_block=pygame.image.load("block4.bmp")
def get_block(pos):
	return block_screen[(int(pos[1])+0)*State.width+int(pos[0])]
def display_small_block_textured(pos):
    pixel_pos=(pos[0]*State.block_size+State.offset,pos[1]*State.block_size)
    textured_block.set_alpha(get_block(pos)[1])
    screen.blit(textured_block,pixel_pos)
def display_block(pos,surface):
    pixel_pos=(pos[0]*State.block_size+State.offset,pos[1]*State.block_size)
    screen.blit(surface,pixel_pos)
class small_block:   
    def __init__(self,pos,image,test=true):
        #global State.game_over,State.game_over
	self.pos=pos
        if get_block(pos)[0]==true and test==true:
		State.game_over=true
		State.enter_high_score=true
        self.image=image
    def draw(self):
        #display_small_block(self.pos,self.color)
        display_block(self.pos,self.image)
       
    def fill_block_screen(self):
        block_screen[(int(self.pos[1])+0)*State.width+int(self.pos[0])]=[true,255]
    def move_left(self,dis):
        self.pos=(self.pos[0]-dis,self.pos[1])
        if self.pos[0]<0:
            self.pos=(self.pos[0]+dis,self.pos[1])
            return false
        if block_screen[(int(self.pos[1])+0)*State.width+int(self.pos[0])][0]==true:
            self.pos=(self.pos[0]+dis,self.pos[1])
            return false

        return true
    def move_right(self,dis):
        self.pos=(self.pos[0]+dis,self.pos[1])
        if self.pos[0]>=State.width:
            self.pos=(self.pos[0]-dis,self.pos[1])
            return false
        if block_screen[(int(self.pos[1])+0)*State.width+int(self.pos[0])][0]==true:
            self.pos=(self.pos[0]-dis,self.pos[1])
            return false
        return true
    def move_down(self,dis):
        self.pos=(self.pos[0],self.pos[1]+dis)
        if self.pos[1]>State.height-1:
            self.pos=(self.pos[0],self.pos[1]-dis)
            return false
        if self.pos[1]==int(self.pos[1]):
            
            if block_screen[int(self.pos[1])*State.width+int(self.pos[0])][0]==true:#int(self.pos[1]+1) always rounds up
                                                                            # so as soon as we overlap it returns false
                self.pos=(self.pos[0],self.pos[1]-dis)
                return false
            
        else:
            
            if block_screen[(int(self.pos[1])+1)*State.width+int(self.pos[0])][0]==true:#int(self.pos[1]+1) always rounds up
                                                                            # so as soon as we overlap it returns false
                self.pos=(self.pos[0],self.pos[1]-dis)
                return false
            
            
        return true
    def move_up(self,dis):
        self.pos=(self.pos[0],self.pos[1]-dis)
        if self.pos[1]<0:
            self.pos=(self.pos[0],self.pos[1]+dis)
            return false
        if block_screen[(int(self.pos[1])+0)*State.width+int(self.pos[0])][0]==true:
            self.pos=(self.pos[0],self.pos[1]+dis)
            return false
        return true
def draw_small_blocks(Small_Blocks):
    for i in Small_Blocks:
        i.draw()
def draw_small_blocks_shadow(Small_Blocks):
    for i in Small_Blocks:
        i.draw_shadow(pos)
def small_blocks_fill_screen(Small_Blocks):
    for i in Small_Blocks:
        i.fill_block_screen()
def small_blocks_move_left(Small_Blocks,dis):
    return_value=true
    for i in range(len(Small_Blocks)):
        if Small_Blocks[i].move_left(dis)==false:
            return_value=false
            for j in range(i):
                Small_Blocks[j].move_right(dis)
            break
    return return_value
def small_blocks_move_right(Small_Blocks,dis):
    return_value=true
    for i in range(len(Small_Blocks)):
        if Small_Blocks[i].move_right(dis)==false:
            return_value=false
            for j in range(i):
                Small_Blocks[j].move_left(dis)
            break
    return return_value
def small_blocks_move_down(S_Blocks,dis):
    return_value=true
    for i in range(len(S_Blocks)):
        if S_Blocks[i].move_down(dis)==false:
            return_value=false
            for j in range(i):
                S_Blocks[j].move_up(dis)
            break
    return return_value

    

    
class base_block:
    #rot=0
    #pos=0,0
    #speed=0
    #at_bottom=false
   
    def fill_block_screen(self):
          small_blocks_fill_screen(self.Small_Blocks)
    def update(self):
	if small_blocks_move_down(self.Small_Blocks,self.speed)==false:
	    s=self.Small_Blocks
            s[0].pos=(int(s[0].pos[0]),int(s[0].pos[1]+1))
            s[1].pos=(int(s[1].pos[0]),int(s[1].pos[1]+1))
            s[2].pos=(int(s[2].pos[0]),int(s[2].pos[1]+1))
            s[3].pos=(int(s[3].pos[0]),int(s[3].pos[1]+1))
            self.at_bottom=true
            small_blocks_fill_screen(self.Small_Blocks)
            return
        self.pos=(self.pos[0],self.pos[1]+self.speed)
        if State.move_left==true:
            if small_blocks_move_left(self.Small_Blocks,1)==true:
                self.pos=(self.pos[0]-1,self.pos[1])
        if State.move_right==true:
            if small_blocks_move_right(self.Small_Blocks,1)==true:
                self.pos=(self.pos[0]+1,self.pos[1])
        if State.move_down==true:
            for i in range(State.height):
                s=self.Small_Blocks
                s[0].pos=(int(s[0].pos[0]),int(s[0].pos[1]))
                s[1].pos=(int(s[1].pos[0]),int(s[1].pos[1]))
                s[2].pos=(int(s[2].pos[0]),int(s[2].pos[1]))
                s[3].pos=(int(s[3].pos[0]),int(s[3].pos[1]))
                if small_blocks_move_down(self.Small_Blocks,1)==true:
                    self.pos=(self.pos[0],self.pos[1]+1)
                else:
                    break
            #self.pos=(self.pos[0],bottom[self.pos[0]])
            self.at_bottom=true
            small_blocks_fill_screen(self.Small_Blocks)

        
    def draw(self):
	draw_small_blocks(self.Small_Blocks)  
    def draw_shadow(self):
        Blocks=[small_block(i.pos,i.image,false) for i in self.Small_Blocks]
        for i in Blocks:
            i.pos=i.pos[0],int(i.pos[1])
        
        while 1:
            if small_blocks_move_down(Blocks,1)==true:
                continue
            else:
                break
        for block in Blocks:
            block.image.set_alpha(255/2)
        draw_small_blocks(Blocks)
        for block in Blocks:
            block.image.set_alpha()
    def __init__(self,speed,image_path):
        self.image=pygame.image.load(image_path)
        self.speed=speed
        self.rot=0
        self.pos=0,0
        self.at_bottom=false
        self.Small_Blocks=[]
        #self.Small_Blocks.append(small_block((0,0),color))
        #self.Small_Blocks.append(small_block((1,0),color))
        #self.Small_Blocks.append(small_block((2,0),color))
        #self.Small_Blocks.append(small_block((3,0),color))   
class long_block(base_block):   
    def update(self):
        base_block.update(self)
        if self.at_bottom==true:
            return
        if State.rot_block==true:
            S=self.Small_Blocks
            self.rot=self.rot+90
            if self.rot==90:
                if self.pos[1]<3:
                    self.pos=(self.pos[0],3)
                S[0].pos=self.pos
                S[1].pos=(self.pos[0],self.pos[1]-1)
                S[2].pos=(self.pos[0],self.pos[1]-2)
                S[3].pos=(self.pos[0],self.pos[1]-3)
            if self.rot==180:
                self.rot=0
                if self.pos[0]>=State.width-3:
                    self.pos=(State.width-4,self.pos[1])
                S[0].pos=self.pos
                S[1].pos=(self.pos[0]+1,self.pos[1])
                S[2].pos=(self.pos[0]+2,self.pos[1])
                S[3].pos=(self.pos[0]+3,self.pos[1])
                

    def __init__(self,speed):
        base_block.__init__(self,speed,"block2.bmp")
        self.speed=speed
        self.rot=0
        self.pos=0,0
        self.at_bottom=false
        self.Small_Blocks=[]
        self.Small_Blocks.append(small_block((0,0),self.image))
        self.Small_Blocks.append(small_block((1,0),self.image))
        self.Small_Blocks.append(small_block((2,0),self.image))
        self.Small_Blocks.append(small_block((3,0),self.image))
class square_block(base_block):
    def update(self):
        base_block.update(self)
        if self.at_bottom==true:
            return
        if State.rot_block==true:
            S=self.Small_Blocks
            #S[0].pos=self.pos
            #S[1].pos=(self.pos[0],self.pos[1]+1)
            #S[2].pos=(self.pos[0],self.pos[1]+2)
            #S[3].pos=(self.pos[0],self.pos[1]+3)
        
 

    def __init__(self,speed):
        base_block.__init__(self,speed,"block1.bmp")
        self.speed=speed
        self.rot=0
        self.pos=0,0
        self.at_bottom=false
        self.Small_Blocks=[]
        self.Small_Blocks.append(small_block((0,0),self.image))
        self.Small_Blocks.append(small_block((1,1),self.image))
        self.Small_Blocks.append(small_block((1,0),self.image))
        self.Small_Blocks.append(small_block((0,1),self.image))
class l_block(base_block):
    def update(self):
        base_block.update(self)
        if self.at_bottom==true:
            return
        if State.rot_block==true:
            S=self.Small_Blocks
            rot=self.rot
            rot=rot+90
            if rot==360:
                rot=0
            if rot==90:
                if self.pos[0]>=State.width-2:
                    self.pos=State.width-3,self.pos[1]
		if self.pos[1]<1:
			self.pos=1,self.pos[1]
		S[0].pos=self.pos
                S[1].pos=(self.pos[0],self.pos[1]-1)
                S[2].pos=(self.pos[0]+1,self.pos[1]+0)
                S[3].pos=(self.pos[0]+2,self.pos[1]+0)
            elif rot==180:
                if self.pos[0]<1:
			self.pos=1,self.pos[1]
		if self.pos[1]<2:
			self.pos=self.pos[0],2
                S[0].pos=self.pos
                S[1].pos=(self.pos[0],self.pos[1]-1)
                S[2].pos=(self.pos[0]+0,self.pos[1]-2)
                S[3].pos=(self.pos[0]-1,self.pos[1]+0)
            elif rot==270:
                if self.pos[0]<2:
			self.pos=2,self.pos[1]
		if self.pos[1]>State.height-2:
                    self.pos=self.pos[0],State.height-2
                S[0].pos=self.pos
                S[1].pos=(self.pos[0]-1,self.pos[1]+0)
                S[2].pos=(self.pos[0]-2,self.pos[1]+0)
                S[3].pos=(self.pos[0]+0,self.pos[1]+1)
            elif rot==0:
                if self.pos[0]>State.width-2:
			self.pos=State.width-2,self.pos[1]
		if self.pos[1]>State.height-3:
			self.pos=self.pos[0],State.height-3
                S[0].pos=self.pos
                S[1].pos=(self.pos[0]+1,self.pos[1]+0)
                S[2].pos=(self.pos[0]+0,self.pos[1]+1)
                S[3].pos=(self.pos[0]+0,self.pos[1]+2)
            self.rot=rot
                
    def __init__(self,speed):
        base_block.__init__(self,speed,"block2.bmp")
        self.speed=speed
        self.rot=0
        self.pos=0,0
        self.at_botttom=false
        self.Small_Blocks=[]
        self.Small_Blocks.append(small_block((0,0),self.image))
        self.Small_Blocks.append(small_block((1,0),self.image))
        self.Small_Blocks.append(small_block((0,1),self.image))
        self.Small_Blocks.append(small_block((0,2),self.image))
class r_l_block(base_block):
    def update(self):
        base_block.update(self)
        if self.at_bottom==true:
            return
        if State.rot_block==true:
            S=self.Small_Blocks
            rot=self.rot
            rot=rot+90
            if rot==360:
                rot=0
            if rot==90:
                if self.pos[0]>=State.width-2:
			self.pos=State.width-3,self.pos[1]
		if self.pos[1]>=State.height-1:
			self.pos=self.pos[0],State.height-2
                S[0].pos=self.pos
                S[1].pos=(self.pos[0],self.pos[1]+1)
                S[2].pos=(self.pos[0]+1,self.pos[1]+0)
                S[3].pos=(self.pos[0]+2,self.pos[1]+0)
            elif rot==180:
                if self.pos[0]>State.width-2:
		    self.pos=State.width-2,self.pos[1]
		if self.pos[1]<2:
                    self.pos=self.pos[0],2
                S[0].pos=self.pos
                S[1].pos=(self.pos[0],self.pos[1]-1)
                S[2].pos=(self.pos[0]+0,self.pos[1]-2)
                S[3].pos=(self.pos[0]+1,self.pos[1]+0)
            elif rot==270:
                if self.pos[0]<2:
		    self.pos=2,self.pos[1]
		if self.pos[1]<1:
                    self.pos=self.pos[0],1
                S[0].pos=self.pos
                S[1].pos=(self.pos[0]-1,self.pos[1]+0)
                S[2].pos=(self.pos[0]-2,self.pos[1]+0)
                S[3].pos=(self.pos[0]+0,self.pos[1]-1)
            elif rot==0:
                if self.pos[0]<1:
		    self.pos=1,self.pos[1]
		if self.pos[1]>State.height-3:
                    self.pos=self.pos[0],State.height-3
                S[0].pos=self.pos
                S[1].pos=(self.pos[0]-1,self.pos[1]+0)
                S[2].pos=(self.pos[0]+0,self.pos[1]+1)
                S[3].pos=(self.pos[0]+0,self.pos[1]+2)
            self.rot=rot
                
    def __init__(self,speed):
        base_block.__init__(self,speed,"block3.bmp")
        self.speed=speed
        self.rot=0
        self.pos=0,0
        self.at_botttom=false
        self.Small_Blocks=[]
        self.Small_Blocks.append(small_block((0,0),self.image))
        self.Small_Blocks.append(small_block((1,0),self.image))
        self.Small_Blocks.append(small_block((1,1),self.image))
        self.Small_Blocks.append(small_block((1,2),self.image))
class step_block(base_block):
    def update(self):
        base_block.update(self)
        if self.at_bottom==true:
            return
        if State.rot_block==true:
            S=self.Small_Blocks
            rot=self.rot
            rot=rot+90
            if rot==90:
                if self.pos[0]>State.width-2 or self.pos[1]>State.width-2 or self.pos[1]<1:
                    return
                S[0].pos=self.pos
                S[1].pos=(self.pos[0],self.pos[1]-1)
                S[2].pos=(self.pos[0]+1,self.pos[1]+0)
                S[3].pos=(self.pos[0]+1,self.pos[1]+1)
            if rot==180:
                if self.pos[0]>State.width-3 or self.pos[1]>State.height-2:
                    return
                S[0].pos=(self.pos[0],self.pos[1]+1)
                S[1].pos=(self.pos[0]+1,self.pos[1]+1)
                S[2].pos=(self.pos[0]+1,self.pos[1]+0)
                S[3].pos=(self.pos[0]+2,self.pos[1]+0)
                rot=0
            self.rot=rot
                
    def __init__(self,speed):
        base_block.__init__(self,speed,"block4.bmp")
        self.speed=speed
        self.rot=0
        self.pos=0,0
        self.at_botttom=false
        self.Small_Blocks=[]
        self.Small_Blocks.append(small_block((0,1),self.image))
        self.Small_Blocks.append(small_block((1,1),self.image))
        self.Small_Blocks.append(small_block((1,0),self.image))
        self.Small_Blocks.append(small_block((2,0),self.image))
class r_step_block(base_block):
    def update(self):
        base_block.update(self)
        if self.at_bottom==true:
            return
        if State.rot_block==true:
            S=self.Small_Blocks
            rot=self.rot
            rot=rot+90
            if rot==90:
                if self.pos[0]>State.width-2 or self.pos[1]>State.width-2 or self.pos[1]<1:
                    return
                S[0].pos=self.pos
                S[1].pos=(self.pos[0]+1,self.pos[1]-1)
                S[2].pos=(self.pos[0]+1,self.pos[1]+0)
                S[3].pos=(self.pos[0]+0,self.pos[1]+1)
            if rot==180:
                if self.pos[0]>State.width-3 or self.pos[1]>State.height-2:
                    return
                S[0].pos=(self.pos[0],self.pos[1]+0)
                S[1].pos=(self.pos[0]+1,self.pos[1]+0)
                S[2].pos=(self.pos[0]+1,self.pos[1]+1)
                S[3].pos=(self.pos[0]+2,self.pos[1]+1)
                rot=0
            self.rot=rot
                
    def __init__(self,speed):
        base_block.__init__(self,speed,"block4.bmp")
        self.speed=speed
        self.rot=0
        self.pos=0,0
        self.at_botttom=false
        self.Small_Blocks=[]
        self.Small_Blocks.append(small_block((0,0),self.image))
        self.Small_Blocks.append(small_block((1,0),self.image))
        self.Small_Blocks.append(small_block((1,1),self.image))
        self.Small_Blocks.append(small_block((2,1),self.image))
class t_block(base_block):
    def update(self):
        base_block.update(self)
        if self.at_bottom==true:
            return
        if State.rot_block==true:
            S=self.Small_Blocks
            rot=self.rot
            rot=rot+90
            if rot==90:
                if self.pos[0]<1:
                    self.pos=(1,self.pos[1])
                if self.pos[1]<1:
                    self.pos=self.pos[0],1
                if self.pos[1]>State.height-2:
                    self.pos=self.pos[0],State.height-2
                S[0].pos=self.pos[0]-1,self.pos[1]    #
                S[1].pos=self.pos[0],self.pos[1]     ##
                                                      #
                S[2].pos=self.pos[0],self.pos[1]-1
                S[3].pos=self.pos[0],self.pos[1]+1
            if rot==180:
                if self.pos[0]<1:
                    self.pos=1,self.pos[1]
                if self.pos[0]>State.width-2:
                    self.pos=State.width-2,self.pos[1]
                if self.pos[1]>State.height-2:
                    self.pos=self.pos[0],State.height-2
                S[0].pos=self.pos[0],self.pos[1]
                S[1].pos=self.pos[0]-1,self.pos[1]###
                S[2].pos=self.pos[0]+1,self.pos[1] #
                S[3].pos=self.pos[0],self.pos[1]+1
            if rot==270:
                if self.pos[0]>State.width-2:
                    self.pos=State.width-2,self.pos[1]
                if self.pos[1]<1:
                    self.pos=self.pos[0],1
                if self.pos[1]>State.height-2:
                    self.pos=self.pos[0],State.height-2
                S[0].pos=self.pos
                S[1].pos=self.pos[0]+1,self.pos[1]    #
                                                      ##
                S[2].pos=self.pos[0],self.pos[1]-1    #
                S[3].pos=self.pos[0],self.pos[1]+1
            if rot==360:
                if self.pos[0]<1:
                    self.pos=1,self.pos[1]
                if self.pos[0]>State.width-2:
                    self.pos=State.width-2
                if self.pos[1]<1:
                    self.pos=self.pos[0],1
                S[0].pos=self.pos
                S[1].pos=self.pos[0]-1,self.pos[1]
                S[2].pos=self.pos[0],self.pos[1]-1
                S[3].pos=self.pos[0]+1,self.pos[1] #
                rot=0                             ###
            self.rot=rot
                
    def __init__(self,speed):
        base_block.__init__(self,speed,"block1.bmp")
        self.speed=speed
        self.rot=0
        self.pos=0,0
        self.at_botttom=false
        self.Small_Blocks=[]
        self.Small_Blocks.append(small_block((1,0),self.image))
        self.Small_Blocks.append(small_block((0,1),self.image))
        self.Small_Blocks.append(small_block((1,1),self.image))
        self.Small_Blocks.append(small_block((2,1),self.image))
    
