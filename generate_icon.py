from PIL import Image, ImageDraw, ImageFilter
import math

SIZE=512
base=Image.new("RGBA",(SIZE,SIZE),(5,5,14,255))
glow=Image.new("RGBA",(SIZE,SIZE),(0,0,0,0))
g=ImageDraw.Draw(glow)

# neon aura
for r,a in [(210,20),(190,26),(165,34)]:
    g.ellipse((256-r,256-r,256+r,256+r),fill=(140,66,255,a))
glow=glow.filter(ImageFilter.GaussianBlur(32))
base=Image.alpha_composite(base,glow)

art=Image.new("RGBA",(SIZE,SIZE),(0,0,0,0))
d=ImageDraw.Draw(art)

# Pac-Man shaped bomb body
cx,cy=270,275
R=112
# wedge mouth points upward-right for a classic Pac-Man silhouette
pts=[]
for i in range(360):
    ang=math.radians(i-55)
    if -55<=i-360*(i>55)<=55: # unused; body is easier as polygon below
        pass
# Circle with a triangular mouth cutout
d.ellipse((cx-R,cy-R,cx+R,cy+R),fill=(255,243,74,255),outline=(255,255,255,255),width=5)
d.polygon([(cx,cy),(cx+115,cy-62),(cx+115,cy+62)],fill=(5,5,14,255))

# bomb fuse
d.line((cx-8,cy-R,cx+5,cy-R-42,cx+28,cy-R-58),fill=(255,43,214,255),width=9,joint="curve")
d.ellipse((cx+20,cy-R-67,cx+40,cy-R-47),fill=(255,243,74,255))

# cyberpunk snake wrapped around bomb: thick polyline + segmented highlights
snake=[]
for i in range(190):
    a=i/189*math.pi*1.72 + math.pi*.18
    rad=R+30+10*math.sin(i/12)
    x=cx+rad*math.cos(a)
    y=cy+rad*.68*math.sin(a)
    snake.append((x,y))
d.line(snake,fill=(0,246,255,255),width=30,joint="curve")
d.line(snake,fill=(8,45,70,255),width=17,joint="curve")
d.line(snake,fill=(0,246,255,255),width=6,joint="curve")

# snake head
hx,hy=snake[-1]
d.ellipse((hx-20,hy-20,hx+20,hy+20),fill=(0,246,255,255))
d.ellipse((hx-8,hy-8,hx-2,hy-2),fill=(255,255,255,255))
d.ellipse((hx+4,hy-8,hx+10,hy-2),fill=(255,255,255,255))

# fuse spark
for ang in range(0,360,60):
    rr=30
    x=cx+28+math.cos(math.radians(ang))*rr
    y=cy-R-58+math.sin(math.radians(ang))*rr
    d.line((cx+28,cy-R-58,x,y),fill=(255,43,214,210),width=4)

# glow passes
for blur,alpha in [(28,110),(14,150),(6,190)]:
    layer=art.copy()
    layer.putalpha(layer.getchannel("A").point(lambda p:p*alpha//255))
    layer=layer.filter(ImageFilter.GaussianBlur(blur))
    base=Image.alpha_composite(base,layer)

base=Image.alpha_composite(base,art)
base.resize((192,192),Image.Resampling.LANCZOS).save("icon-192.png")
base.resize((512,512),Image.Resampling.LANCZOS).save("icon.png")
print("Generated icon.png and icon-192.png")
