import sys,pygame,random,pygame.time
class swirl:
	
	def Draw(self):
		self.surface.blit(self.img_rot,self.pos)
	def Update(self,angle):
		self.angle+=angle
		self.img_rot=pygame.transform.rotate(self.img,self.angle)
		self.img_rot.set_alpha(self.alpha)
		self.img.set_alpha(self.alpha)
		self.img_rot.lock()
		self.img_rot.set_colorkey(self.img_rot.get_at((0,0)))
		self.img_rot.unlock()
	def Trans(self,alpha):
		self.alpha=alpha
	def Pos(self,new_pos):
		self.pos=new_pos
	def __init__(self,image_path,surface):
		self.img=pygame.image.load(image_path)
		self.img_rot=self.img
		self.surface=surface
		self.pos=0,0
		self.angle=0
		self.alpha=255