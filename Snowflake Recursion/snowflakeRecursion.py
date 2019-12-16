import datetime
import os
import fontTools.ttLib.ttFont as ttFont

message = "HAPPY HOLIDAYS"



# counting how many times it ultimately renders your text
class Counter(object) :
    def __init__(self, fun) :
        self._fun = fun
        self.counter=0
    def __call__(self,*args, **kwargs) :
        self.counter += 1
        return self._fun(*args, **kwargs)


# set canvas size. was dynamically scaling it as the function got more haywire
scale_artboard = 7
w = 500 * scale_artboard
h = 500 * scale_artboard



# calculating the set width of your message
otf = '/path/to/otf'
f = ttFont.TTFont(otf)
glyph_set = f.getGlyphSet(preferCFF=True)

set_width = 0
for letter in message:
    if letter == " ":
        letter = "space"
    set_width += glyph_set[letter].width
    
    
    
# radius of center empty space
mid_gap = 150
font_size = 56
flakes = 5

# amount the font size decreases each time it recurs
size_red = 9

# amount of splaying
flake_tightness = 5

#how far up the subflakes are chocked up
choke = 3 #integer


cut_off = font_size / 2
angle = 360 / flakes


# the recursive function
def drawFlake(f_s):
    
    font(otf)
    tracking(5)
    word_width = (f_s / 1000) * set_width
    
    vert_fix = -0.37*f_s
    
    if f_s > cut_off:
        
        fontSize(f_s)
        # fill(1)
        text(message, (w/2 + mid_gap, h/2 + vert_fix), align = "left")
        
        f_s -= size_red
        vert_fix = -0.37*f_s
        
        fontSize(f_s)
        # inside subflakes
        with savedState():
            translate(word_width / choke, f_s / 1.3)
            rotate(angle/flake_tightness, center = (w/2, h/2 + vert_fix))
            # recursion
            drawFlake(f_s)
            
        with savedState():
            translate(word_width / choke, - f_s / 1.2)
            rotate(-angle/flake_tightness, center = (w/2, h/2))
            # recursion
            drawFlake(f_s)
            
        # outside subflakes
        with savedState():
            translate(word_width, f_s / 1.3)
            rotate(angle/(flake_tightness/2), center = (w/2, h/2 + vert_fix))
            drawFlake(f_s)
            
        with savedState():
            translate(word_width, -f_s/1.2)
            rotate(-angle/(flake_tightness/2), center = (w/2, h/2 + vert_fix))
            # recursion
            drawFlake(f_s)
    
            

drawFlake = Counter(drawFlake)




# make the page and do it all
newPage(w,h)
fill(0)
rect(0,0,w,h)
fill(1)
for flake in range(flakes):
    with savedState():
        rotate(angle*flake, center = (w/2, h/2))
        drawFlake(font_size)
        
print(drawFlake.counter, " flake-bits")  
   
now = datetime.datetime.now()
timestamp = now.strftime("%Y-%m-%d_%H-%M")
new_path = f"_snowFlakeRecursion_{timestamp}.jpg"
saveImage(new_path)


# # make animation

# frames = 60
# runs = 4

# range_min = 3
# range_max = 15

# for run in range(runs):
#     for frame in range(frames):
    
#         newPage(w,h)
#         frameDuration(1/30)
#         fill(0)
#         rect(0,0,w,h)
#         fill(1)
    
#         dx = pi * frame / frames
#         delta = pow(sin(dx), 3)
#         flake_tightness = delta * (range_max - range_min) + range_min
    
#         for flake in range(flakes):
#             with savedState():
#                 rotate(angle*flake, center = (w/2, h/2))
#                 drawFlake(font_size)
                
now = datetime.datetime.now()
timestamp = now.strftime("%Y-%m-%d_%H-%M")
new_path = f"_snowFlakeRecursion_{timestamp}.mp4"
saveImage(new_path)
