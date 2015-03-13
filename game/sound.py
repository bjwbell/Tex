import sys,pygame
false=False
true=True
rotate_snd=pygame.mixer.Sound("sounds/rotate.wav")
at_bottom_snd=pygame.mixer.Sound("sounds/at_bottom.wav")
#pygame.mixer.music.load("sounds/track.wav")
class state:
	def __init__(self):
		self.rotate=false
		self.at_bottom=false
		self.play_track=false
		self.enabled=false
State=state()
def Play_Music():
	if State.enabled==true:
		print 'music disabled'
		#pygame.mixer.music.play()
def Stop_Music():
	print 'music disabled'
	#pygame.mixer.music.stop()
def Play():
	global rotate_snd,at_bottom_snd
	if State.enabled==false:
		return
	if State.rotate==true:
		rotate_snd.play()
	if State.at_bottom==true:
		at_bottom_snd.play()
