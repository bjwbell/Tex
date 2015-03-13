import pygame,sys,string

char_pixel_w=10
char_pixel_h=15

class print_to_screen:
	def __init__(self,screen):
		self.screen=screen
		self.al=pygame.image.load('alphabet.bmp')
		self.img_num=pygame.image.load("num.bmp")
		
	def printscr(self,text,pos):
		text=text.lower()
		for i in text:
		
			self.display_char(i,pos)
			pos=pos[0]+10,pos[1]
	def print_num(self,text,pos):
		char_width=10
		text=str(text)
		
		for i in text:
			pos=(pos[0]+char_width,pos[1])
			img_pos=0

			for j in range(int(i)):
				img_pos+=10
	
			self.screen.blit(self.img_num,pos,(img_pos,0,10,20))
	def display_char(self,char,pos):
		al=self.al
		if string.find(string.digits,char)!=-1:
			self.print_num(char,pos)
		if char=='a':
			self.screen.blit(al,pos,(0,4,10,13))
		if char=='b':
			self.screen.blit(al,pos,(10,4,10,13))
		if char=='c':
			self.screen.blit(al,pos,(20,4,10,13))
		if char=='d':
			self.screen.blit(al,pos,(30,4,10,13))
		if char=='e':
			self.screen.blit(al,pos,(40,4,10,13))
		if char=='f':
			self.screen.blit(al,pos,(50,4,10,13))
		if char=='g':
			self.screen.blit(al,pos,(60,4,10,13))
		if char=='h':
			self.screen.blit(al,pos,(70,4,10,13))
		if char=='i':
			self.screen.blit(al,pos,(80,4,10,13))
		if char=='j':
			self.screen.blit(al,pos,(90,4,10,13))
		if char=='k':
			self.screen.blit(al,pos,(100,4,10,13))
		if char=='l':
			self.screen.blit(al,pos,(110,4,10,13))
		if char=='m':
			self.screen.blit(al,pos,(120,4,10,13))
		if char=='n':
			self.screen.blit(al,pos,(130,4,10,13))
		if char=='o':
			self.screen.blit(al,pos,(140,4,10,13))
		if char=='p':
			self.screen.blit(al,pos,(150,4,10,13))
		if char=='q':
			self.screen.blit(al,pos,(160,4,10,13))
		if char=='r':
			self.screen.blit(al,pos,(170,4,10,13))
		if char=='s':
			self.screen.blit(al,pos,(180,4,10,13))
		if char=='t':
			self.screen.blit(al,pos,(190,4,10,13))
		if char=='u':
			self.screen.blit(al,pos,(200,4,10,13))
		if char=='v':
			self.screen.blit(al,pos,(210,4,10,13))
		if char=='w':
			self.screen.blit(al,pos,(220,4,10,13))
		if char=='x':
			self.screen.blit(al,pos,(230,4,10,13))
		if char=='y':
			self.screen.blit(al,pos,(240,4,10,13))
		if char=='z':
			self.screen.blit(al,pos,(250,4,10,13))
			
			