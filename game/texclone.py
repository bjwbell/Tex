import sys,pygame,random,pygame.time,string,pickle
import core,swirl,screen_print,sound
true=True
false=False
lost=false
showing_high_scores=false
block_shadow=true
fall_speed=0.0
starting_speed=0.1
background=pygame.image.load("game_background.bmp")
pause=false
game_menu=false
quit=false
entering_starting_level=false
def draw_game_background():
    core.screen.blit(background,(0,0))
    core.screen.blit(background,(core.State.offset+core.State.width*core.State.block_size,0))
def clear_row(row_num):
    for i in range(core.State.width):
        core.block_screen[row_num*core.State.width+i]=(false,255)
    #    if row_num==bottom[i]:
    #        bottom[i]=bottom[i]+1
    for j in range(1,core.State.height-1):
        for i in range(core.State.width):
            if core.block_screen[(core.State.height-j)*core.State.width+i][0][0]==false:
                core.block_screen[(core.State.height-j)*core.State.width+i]=core.block_screen[(core.State.height-(j+1))*core.State.width+i]
                core.block_screen[(core.State.height-(j+1))*core.State.width+i]=(false,255)
def display_blocks():
    for j in range(core.State.height):
        for i in range(core.State.width):
            if core.block_screen[j*core.State.width+i][0]==true:
               core.display_small_block_textured((i,j))

Display=screen_print.print_to_screen(core.screen)

class eater:
    num_blocks_eaten=0
    v=0.03
    pos=0,core.State.height-1
    count=0
    dif=0.08

    def Dificulty(self,dif):
        if dif=='easy':
             self.dif=0.06
             self.v=0.08
        elif dif=='medium':
            self.dif=0.04
            self.v=0.04
        elif dif=='hard':
            self.dif=0.02
            self.v=0.01
    def Draw(self):
            core.screen.blit(self.img_level,(0,460))
            #print self.pos[0],self.pos[1],self.alpha
            core.block_screen[self.pos[1]*core.State.width+self.pos[0]]=(core.get_block(self.pos)[0],self.alpha)
            self.Swirl.Trans(255)#self.alpha)
            self.Swirl.Draw()
            Display.print_num(int(self.lines_cleared/3.0),(40,460))
    def speed_up(self):
        if core.block_screen[self.pos[1]*core.State.width+self.pos[0]][0]==true:
                return true
        else:
                return false
    def slow_down(self):
        if core.block_screen[self.pos[1]*core.State.width+self.pos[0]][0]==true:
                return false
        for i in range(self.pos[1]-1):
                if core.block_screen[i*core.State.width+self.pos[0]][0]==true:
                        return true
        return false

    def update_speed(self):
         if self.speed_up()==true:
            self.v=self.v+self.dif*5
         elif self.slow_down()==true:
            if self.num_blocks_eaten>=50:
                self.v=self.v-0.0075*10
            if self.num_blocks_eaten>=25 and self.num_blocks_eaten<50:
                self.v=self.v-0.005*10
            if self.num_blocks_eaten>=10 and self.num_blocks_eaten<25:
                self.v=self.v-0.001*10
            if self.num_blocks_eaten<10:    
                self.v=self.v-0.0008*10
         if self.v>=0.1:
            self.v=0.1
         if self.v<=0.0015:
            self.v=0.0015
#             
    def update(self):
        self.count=self.count+self.v
        pos=core.convert_pixel_pos(self.pos)
        self.Swirl.Pos(pos)
        
        self.Swirl.Update(0)
        
        if self.count<1:
            self.alpha=(1-self.count)*255
            #core.display_small_block(self.pos,(255,255,255))
            return
        else:
            self.count=0
            self.alpha=(1-self.count)*255        
        self.update_speed()
        if core.block_screen[self.pos[1]*core.State.width+self.pos[0]][0]==true:
            self.num_blocks_eaten=self.num_blocks_eaten+1
        core.block_screen[self.pos[1]*core.State.width+self.pos[0]]=(false,255)
        
        #core.display_small_block(self.pos,(255,0,0))
        for i in range(core.State.height-1,1,-1):
            core.block_screen[i*core.State.width+self.pos[0]]=core.block_screen[(i-1)*core.State.width+self.pos[0]]
        if self.pos[0]<core.State.width-1:
            self.pos=self.pos[0]+1,self.pos[1]
        else:
            self.lines_cleared=self.lines_cleared+1
            self.pos=0,self.pos[1]


    
    def __init__(self):
        self.Dificulty('easy')
        self.Swirl=swirl.swirl("swirl.bmp",core.screen)
        self.Swirl.Pos((0,480))
        self.alpha=255
        self.lines_cleared=0
        self.img_level=pygame.image.load("graphics/level.bmp")
def trad_tetris():
    for j in range(core.State.height):
        filled=true
        for i in range(core.State.width):
            if core.block_screen[j*core.State.width+i][0]==false:
                filled=false
        if filled==true:
            clear_row(j)
    
blocks=[]
#blocks.append(square_block((0,200,255),0.1))
blocks.append(core.square_block(starting_speed))
Eater=eater()
rand=random.randrange(7)
rand_next=random.randrange(7)
L_B=core.l_block(fall_speed)
S_B=core.square_block(fall_speed)
Long_B=core.long_block(fall_speed)
R_L_B=core.r_l_block(fall_speed)
R_Step_B=core.r_step_block(fall_speed)
T_B=core.t_block(fall_speed)
Step_B=core.step_block(fall_speed)
block_dic={0:L_B,1:S_B,2:Long_B,3:R_L_B,4:R_Step_B,5:T_B,6:Step_B}

def draw_preview(rand_next):
        Block=block_dic[rand_next]
        old_pos=Block.pos
        pos=core.State.offset*core.State.block_size/core.State.block_size,core.State.height/2
        pos=core.State.offset/core.State.block_size,-1
        s=Block.Small_Blocks
        img_back_ground=pygame.image.load("background_preview.bmp")
        s[0].pos=s[0].pos[0]-pos[0],s[0].pos[1]-pos[1]
        s[1].pos=s[1].pos[0]-pos[0],s[1].pos[1]-pos[1]
        s[2].pos=s[2].pos[0]-pos[0],s[2].pos[1]-pos[1]
        s[3].pos=s[3].pos[0]-pos[0],s[3].pos[1]-pos[1]
        Block.Small_Blocks=s

        core.screen.blit(img_back_ground,(0,core.State.block_size/2),(0,0,core.State.block_size*4,core.State.block_size*4))
        Block.draw()
        
        s[0].pos=s[0].pos[0]+pos[0],s[0].pos[1]+pos[1]
        s[1].pos=s[1].pos[0]+pos[0],s[1].pos[1]+pos[1]
        s[2].pos=s[2].pos[0]+pos[0],s[2].pos[1]+pos[1]
        s[3].pos=s[3].pos[0]+pos[0],s[3].pos[1]+pos[1]
Sound_State=sound.state()
def update_tex_game():
    global lost,fall_speed,starting_speed,rand,rand_next
    fall_speed=Eater.lines_cleared/50.0+starting_speed
    sound.State.at_bottom=false
    sound.State.rotate=core.State.rot_block
    if blocks[len(blocks)-1].at_bottom==true:
        sound.State.at_bottom=true    
        rand_next=random.randrange(7)
        if rand==0:
            blocks.append(core.l_block(fall_speed))
        elif rand==1:
            blocks.append(core.square_block(fall_speed))
        elif rand==2:
            blocks.append(core.long_block(fall_speed))
        elif rand==3:
            blocks.append(core.r_l_block(fall_speed))
        elif rand==4:
            blocks.append(core.r_step_block(fall_speed))
        elif rand==5:
            blocks.append(core.t_block(fall_speed))
        else:
            blocks.append(core.step_block(fall_speed))
        rand=rand_next
    blocks[len(blocks)-1].speed=fall_speed
    blocks[len(blocks)-1].update()
    blocks[len(blocks)-1].draw()
    if(block_shadow):
        blocks[len(blocks)-1].draw_shadow()
    draw_preview(rand_next)
            
    #for i in blocks:
     #   i.draw()
    display_blocks()
   # for i in blocks:
    #    display_block(i)
    #for i in bottom:
     #   if i<=0:
     #       print 'Game Over'
      #      pygame.quit()
#trad_tetris()
    Eater.update()
    #for j in range(height):
        #update_row(height-j)    
class input:
    KEY_UP=false
    KEY_DOWN=false
    k_enter=false
    k_down=false
    k_up=false
    k_left=false
    k_right=false
    key_pressed=false

Input=input()    

class ui:

    #num_items=2
    
    def draw(self):
        if self.focus==false:
            return
        width=core.State.screen_width
        height=core.State.screen_height
        c=self.current_selection
        for i in self.items:
                i[0].set_alpha(255)

        for i in self.items:
                if i[1]==true:
                        i[0].set_alpha(25)
        self.items[self.current_selection][0].set_alpha(125)

        y=0
        for i in self.items:
                core.screen.blit(i[0],(width/2-i[0].get_width()/2,y),i[0].get_rect())
                y+=50

         
    def update(self):
        global showing_high_scores
        if self.focus==false:
            return

        if Input.k_down==true:
            Input.k_down=false
            if self.current_selection<len(self.items)-1:
                self.current_selection=self.current_selection+1
            else:
                self.current_selection=0
        if Input.k_up==true:
            Input.k_up=false
            if self.current_selection>0:
                self.current_selection=self.current_selection-1
            else:
                self.current_selection=len(self.items)-1            
        if Input.k_enter==true and Input.KEY_DOWN==true:
                Input.k_enter=false
                c=self.current_selection
                j=0
                #self.focus=false
                for i in self.items:
                        if j==c:
                                i=i[0],true
                                self.func[j](self)
                        #else:
                                #i=i[0],false
                        j+=1
        Input.KEY_UP=false
        Input.KEY_DOWN=false
    def add_item(self,img,func):
            if type(img)==str:
                    img=pygame.image.load(img)
                    img.set_colorkey((255,255,255))
            self.items.append((img,false))
            self.func.append(func)
    def set_function(func):
            self.func.append(func)
    def __init__(self,play_func,high_scores_func,image1="Play.bmp",image2="high_scores.bmp"):
        self.focus=true
        self.current_selection=0

        self.items=[]
        self.func=[]
        play=pygame.image.load(image1)
        self.items.append((play,false))
        play.set_colorkey((255,255,255))
        play.set_alpha(100)
        self.func.append(play_func)
        show_high_scores=pygame.image.load(image2)
        self.items.append((show_high_scores,false))
        show_high_scores.set_colorkey((255,255,255))
        self.func.append(high_scores_func)


def UI_play(obj):
        obj.focus=false
        print 'play pressed'
def UI_high_scores(obj):
        global showing_high_scores
        showing_high_scores=true
        #obj.focus=true
        print 'high_scores pressed'
UI=ui(UI_play,UI_high_scores)

def UI_full_screen(UI):
        pygame.display.toggle_fullscreen()
        #UI.focus=true
def Togle_Sound():
        print 'togleing sound'
        sound.State.enabled=not sound.State.enabled
        en=sound.State.enabled
        if en==true:
                sound.Play_Music()
        if en==false:
                sound.Stop_Music()
def UI_Togle_Sound(obj):
        Togle_Sound()
def UI_Togle_Shadow(obj):
        global block_shadow
        print 'toggleing block shadow'
        block_shadow=not block_shadow
        print 'block_shadow:',block_shadow
def UI_Starting_Level(obj):
        global entering_starting_level
        print 'setting entering_starting_level to true'
        entering_starting_level=true
UI.add_item("graphics/full_screen.bmp",UI_full_screen)
UI.add_item("graphics/sound.bmp",UI_Togle_Sound)
UI.add_item("graphics/block_shadow.bmp",UI_Togle_Shadow)
UI.add_item("graphics/starting_level.bmp",UI_Starting_Level)
Ptr=screen_print.print_to_screen(core.screen)
keys=[]
def Togle_Pause():
    global pause
    pause=not pause
def Togle_Game_Menu():
        global game_menu,pause
        game_menu=not game_menu
        pause=game_menu

def load_high_scores(file):
    high_score=[]
    f=open(file,'r')
    for line in f.readlines():
        tmp=line.split('=')
        high_score.append((tmp[0],tmp[1]))
    f.close()
    return high_score
def write_high_scores(high_score,file):
    f=open(file,'w')
    for score in high_score:
        print 'score:',score
        sti=str(score[0])+"="+str(score[1])+'\n'
        print 'sti:',sti
        f.write(sti)
    f.close()
try:
        file=open('high_score.txt','r')
        high_score=load_high_scores('high_score.txt')
        #high_score=pickle.load(file)
except IOError:
        high_score=[]
def new_high_score(lines,high):
        if lines>=lowest_score(high)[1]:
                return true
        else:
                return false
def lowest_score(high):
        count=0
        for i in high:
                if count==0:
                        low=i
                if i[1]<low[1]:
                        low=i
                count+=1
        return low
def remove_lowest_score(high):
        low=lowest_score(high)
        high.remove(low)
max_score_len=10

def enter_level():
        global Ptr,keys#,high_score
        if pygame.key.get_focused()==false:
                return
        #if len(high_score)>=5:
        #        if new_high_score(Eater.lines_cleared,high_score)!=true:
        #                return true
        #        remove_lowest_score(high_score)
        
        count=0
        string=''
        for i in keys:
                string+=i
        Ptr.printscr("enter your level",(core.State.screen_width/2,0))
        pygame.draw.rect(core.screen,core.white,((core.State.screen_width/2,40,screen_print.char_pixel_w*len(string),screen_print.char_pixel_h)))
        Ptr.printscr(string,(core.State.screen_width/2,40))
        #pygame.key.set_repeat(500,300)
        #for i in pygame.key.get_pressed():
        key=Input.key_pressed
        count=key
        if Input.KEY_DOWN==true:
                #print i,count
                
                
                #if i==false or count==301 or count==300:
                #        count+=1
                        #continue
                if count==pygame.K_LSHIFT:
                        count+=1
                        #continue
                #print i,count
                print pygame.key.name(count)
                if count==pygame.K_RETURN:
                        Eater.lines_cleared=int(string)*3
                        #pickle.dump(high_score,file)
                        #print 'return pressed'
                        keys=[]
                        return true
                if count==pygame.K_BACKSPACE:
                        if len(keys)>0:
                                keys.pop()
                        return false
                if count==pygame.K_SPACE:
                        keys.append(' ')
                        return false

                
                keys.append(pygame.key.name(count))
                
                        
                count+=1

        return false
def enter_score():
        global Ptr,keys,high_score
        if pygame.key.get_focused()==false:
                return
        if len(high_score)>=5:
                if new_high_score(Eater.lines_cleared,high_score)!=true:
                        return true
                remove_lowest_score(high_score)
        
        count=0
        string=''
        for i in keys:
                string+=i
        Ptr.printscr("enter your name",(core.State.screen_width/2,0))
        pygame.draw.rect(core.screen,core.white,((core.State.screen_width/2,40,screen_print.char_pixel_w*len(string),screen_print.char_pixel_h)))
        Ptr.printscr(string,(core.State.screen_width/2,40))
        #pygame.key.set_repeat(500,300)
        #for i in pygame.key.get_pressed():
        key=Input.key_pressed
        count=key
        if Input.KEY_DOWN==true:
                #print i,count
                
                
                #if i==false or count==301 or count==300:
                #        count+=1
                        #continue
                if count==pygame.K_LSHIFT:
                        count+=1
                        #continue
                #print i,count
                print pygame.key.name(count)
                if count==pygame.K_RETURN:
                        high_score.append((string,Eater.lines_cleared))
                        write_high_scores(high_score,'high_score.txt')
                        #pickle.dump(high_score,file)
                        #print 'return pressed'
                        keys=[]
                        return true
                if count==pygame.K_BACKSPACE:
                        if len(keys)>0:
                                keys.pop()
                        return false
                if count==pygame.K_SPACE:
                        keys.append(' ')
                        return false

                if len(keys)<max_score_len:
                        keys.append(pygame.key.name(count))
                
                        
                count+=1

        return false
def display_high_scores():
        global Ptr,high_score
        count=40
        max_len=max_score_len*10
        if core.State.screen_width/2+max_len>=core.State.screen_width-20:
                max_len=core.State.screen_width+100
        Ptr.printscr("High Scores",(core.State.screen_width/2,0))
        for i in high_score:
                #print 'i[0] is ',str(i)
                Ptr.printscr(i[0],(core.State.screen_width/2,count))
                Ptr.printscr(str(i[1]),(core.State.screen_width/2+max_len,count))
                count+=20
def borked_key_pressed():
        key_pressed()
        for i in pygame.key.get_pressed():
                print i
                if pygame.key.name(i)=='unknown key':
                        continue
                if i==pygame.K_RETURN:
                        continue
                if pygame.key.name(i)!='unknown key':
                        print pygame.key.name(i)
                if i!=pygame.K_NUMLOCK and i!=pygame.K_CAPSLOCK and i!=pygame.K_SCROLLOCK:
                        print pygame.key.name(i)
                        print 'returning true'
                        return true
        return false
def key_pressed():
        for i in pygame.key.get_pressed():
                print i
                if i!=pygame.K_NUMLOCK and i!=pygame.K_CAPSLOCK and i!=pygame.K_SCROLLOCK:
                        return true
        return false 
#def Set_Dificulty():
    #if UI.easy_selected==true:
    #    Eater.Dificulty('easy')
    #if UI.medium_selected==true:
    #    Eater.Dificulty('medium')
    #if UI.expert_selected==true:
    #    Eater.Dificulty('expert')
def display_pause():
    image=pygame.image.load("graphics/pause.bmp")
    pos=int(core.screen.get_width()/2.0-image.get_width()/2.0+0.5),int(core.screen.get_height()/2.0-image.get_height()/2.0+0.5)
    core.screen.blit(image,pos)
def New_Game():
        global game_menu,fall_speed,starting_speed,showing_high_scores
        game_menu=false
        UI.focus=true
        showing_high_scores=false
        fall_speed=0.0
        starting_speed=0.1

        for i in range(core.State.width*core.State.height):
                core.block_screen[i]=(false,255)
def UI_New_Game(UI):
        New_Game()
def Quit():
        global quit
        quit=true
        print 'quiting'
        
        #pygame.quit()
        #sys.exit()
def UI_Quit(UI):
        Quit()
Game_Menu_UI=ui(UI_New_Game,UI_Togle_Sound,"graphics/new_game.bmp","graphics/sound.bmp")
Game_Menu_UI.add_item("graphics/block_shadow.bmp",UI_Togle_Shadow)
Game_Menu_UI.add_item("graphics/quit.bmp",UI_Quit)
UI.add_item("graphics/quit.bmp",UI_Quit)
def update():
    global showing_high_scores,entering_starting_level
    fill_color=200,230,255
    core.screen.fill(fill_color)
    if game_menu==true:
        Game_Menu_UI.focus=true
        Game_Menu_UI.update()
        Game_Menu_UI.draw()
        return 
    if pause==true:
        display_pause()
        return
    #display_high_scores()
    #return
    if entering_starting_level==true:
        if enter_level()==false:
                return
        else:
                entering_starting_level=false
                #Input.k_down=false
                #Input.KEY_DOWN=false
                #Input.KEY_UP=false
                return
    if core.State.enter_high_score==true:
        if enter_score()==false:
                return
        else:
                core.State.enter_high_score=false
                showing_high_scores=true
                return
    if core.State.game_over==true:
            #core.State.enter_high_score=false
            #print 'displaying high_scores'
            if showing_high_scores==true:
                core.screen.fill(fill_color)
                display_high_scores()
                if Input.KEY_DOWN==true:
                                showing_high_scores=false

            else:
                #showing_high_scores=false
                core.State.game_over=false
                New_Game()
    else:
            
        if UI.focus==false:
                draw_game_background()
                update_tex_game()
                sound.Play()
        if showing_high_scores==false:
                UI.update()
                UI.draw()
                if UI.focus==false:
                        Eater.Draw()
        if UI.focus==true:
                if showing_high_scores==true:
                        core.screen.fill(fill_color)
                        display_high_scores()
                        if Input.KEY_DOWN==true:
                                showing_high_scores=false
                                UI.items[1]=UI.items[1][0],false
                                print 'not showing high_scores'

                        return

                #Set_Dificulty()

    #pygame.display.flip()




t1=0
t2=0
first_time=true
time=0

pygame.mouse.set_visible(false)

def run():
        global t1,t2,first_time,time,pause,quit
        while not quit:
            t1=pygame.time.get_ticks()
    
            core.State.rot_block=false
            core.State.move_down=false
            Input.KEY_UP=false
            Input.KEY_DOWN=false
            pygame.event.pump()
            if first_time==true:
                t2=pygame.time.get_ticks()
                first_time=false
                continue
            else:
        
                t=t1-t2
        
                time=time+t
                if time<80000:
                    continue
                else:
                    time=0
            t2=pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.KEYUP:
                    Input.KEY_UP=true
                    
                    if event.key == pygame.K_LEFT:
                        core.State.move_left=false
                        Input.k_left=false
                    if event.key == pygame.K_RIGHT:
                        core.State.move_right=false
                        Input.k_right=false
                    if event.key==pygame.K_DOWN:
                        core.State.move_down=true
                        Input.k_down=false
                    if event.key==pygame.K_UP:
                        Input.k_up=false
                        core.State.rot_block=true
                    if event.key==pygame.K_RETURN:
                        Input.k_enter=false
                if event.type == pygame.KEYDOWN:
                    Input.KEY_DOWN=true
                    Input.key_pressed=event.key
                    if event.key == pygame.K_LEFT:
                        Input.k_left=true
                        core.State.move_left=true
                    if event.key == pygame.K_RIGHT:
                        Input.k_right=true
                        core.State.move_right=true
                    if event.key==pygame.K_DOWN:
                        Input.k_down=true
                    if event.key==pygame.K_UP:
                        Input.k_up=true
                        
                    if event.key==pygame.K_RETURN:
                        if pause==true:
                            Togle_Pause()
                        Input.k_enter=true
                    if event.key==pygame.K_ESCAPE:
                        Togle_Game_Menu()
                        #Togle_Pause()
                    if event.key==pygame.K_p:
                        Togle_Pause()
                        #pygame.quit()
                        #sys.exit()
                
#            if event.key == K_UP
#            if event.key == K_DOWN:
                        
            update()
            pygame.display.flip()
        pygame.quit()
            
    

