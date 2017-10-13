import mcpi.minecraft as minecraft
import mcpi.block as block
import time
import random
import RPi.GPIO as GPIO

mc = minecraft.Minecraft.create();


x_shape=[[1,0,0,0,1],[0,1,0,1,0],[0,0,1,0,0],[0,0,1,0,0],[0,1,0,1,0],[1,0,0,0,1]]
y_shape=[[1,0,0,0,1],[1,1,0,1,1],[0,1,1,1,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0]]
z_shape=[[1,1,1,1,1],[0,0,0,1,1],[0,0,1,1,0],[0,1,1,0,0],[1,1,0,0,0],[1,1,1,1,1]]

def make_shape(shape, x, y, z, color, onZPlane=True): # x, y, z refer to position of the upper left corner
    for row, line in enumerate(shape):
        for col, cell in enumerate(line):
            mc.setBlock(x+col if onZPlane else x, y-row, z if onZPlane else z-col, block.WOOL.id if cell==1 else block.AIR.id, color)

def reset():
    mc.setBlocks(-128,0,-128,128,64,128,block.AIR.id)
    mc.setBlocks(-128,-1,-128,128,-1,128,block.GRASS.id)
    mc.player.setPos(0,0,0)

def make_axes():
    mc.setBlocks(-20, 0, -20, 0, 0, -20, block.WOOL.id, 15) # x
    make_shape(x_shape, 0, 6, -20, 14)
    mc.setBlocks(-20, 0, -20, -20, 20, -20, block.WOOL.id, 15) # y
    make_shape(y_shape, -19, 25, -20, 14)
    mc.setBlocks(-20, 0, -20, -20, 0, 0, block.WOOL.id, 15) # z
    make_shape(z_shape, -20, 6, 0, 14, False)

def CreateWalls(size,baseheight,height,material,battlements,walkway):
  # Create 4 walls with a specified width, height and material.
  # Battlements and walkways can also be added to the top edges.
 
  mc.setBlocks(-size,baseheight+1,-size,size,baseheight+height,-size,material)
  mc.setBlocks(-size,baseheight+1,-size,-size,baseheight+height,size,material)
  mc.setBlocks(size,baseheight+1,size,-size,baseheight+height,size,material)
  mc.setBlocks(size,baseheight+1,size,size,baseheight+height,-size,material) 
 
  # Add battlements to top edge
  if battlements==True:
    for x in range(0,(2*size)+1,2):
      mc.setBlock(size,baseheight+height+1,(x-size),material)
      mc.setBlock(-size,baseheight+height+1,(x-size),material)
      mc.setBlock((x-size),baseheight+height+1,size,material)
      mc.setBlock((x-size),baseheight+height+1,-size,material)
 
  # Add wooden walkways
  if walkway==True:
    mc.setBlocks(-size+1,baseheight+height-1,size-1,size-1,baseheight+height-1,size-1,block.WOOD_PLANKS)
    mc.setBlocks(-size+1,baseheight+height-1,-size+1,size-1,baseheight+height-1,-size+1,block.WOOD_PLANKS)
    mc.setBlocks(-size+1,baseheight+height-1,-size+1,-size+1,baseheight+height-1,size-1,block.WOOD_PLANKS)
    mc.setBlocks(size-1,baseheight+height-1,-size+1,size-1,baseheight+height-1,size-1,block.WOOD_PLANKS)  
 
def CreateLandscape(moatwidth,moatdepth,islandwidth):
  # Set upper half to air
  mc.setBlocks(-100,1,-100,100,35,100,block.AIR)
  # Set lower half of world to dirt with a layer of grass
  #mc.setBlocks(-100,-1,-100,100,-128,100,block.DIRT)
  mc.setBlocks(-100,0,-100,100,0,100,block.GRASS)
  # Create water moat
  mc.setBlocks(-moatwidth,0,-moatwidth,moatwidth,-moatdepth,moatwidth,block.WATER)
  # Create island inside moat
  mc.setBlocks(-islandwidth,0,-islandwidth,islandwidth,1,islandwidth,block.GRASS)  
 
def CreateKeep(size,baseheight,levels):
  # Create a keep with a specified number
  # of floors levels and a roof
  height=(levels*5)+5
 
  CreateWalls(size,baseheight,height,block.STONE_BRICK,True,True)
 
  # Floors &amp; Windows
  for level in range(1,levels+1):
    mc.setBlocks(-size+1,(level*5)+baseheight,-size+1,size-1,(level*5)+baseheight,size-1,block.WOOD_PLANKS)
 
  # Windows
  for level in range(1,levels+1):
    CreateWindows(0,(level*5)+baseheight+2,size,"N")
    CreateWindows(0,(level*5)+baseheight+2,-size,"S")
    CreateWindows(-size,(level*5)+baseheight+2,0,"W")
    CreateWindows(size,(level*5)+baseheight+2,0,"E")
 
  # Door
  mc.setBlocks(0,baseheight+1,size,0,baseheight+2,size,block.AIR)
 
def CreateWindows(x,y,z,dir):
 
  if dir=="N" or dir=="S":
    z1=z
    z2=z
    x1=x-2
    x2=x+2
 
  if dir=="E" or dir=="W":
    z1=z-2
    z2=z+2
    x1=x
    x2=x
 
  mc.setBlocks(x1,y,z1,x1,y+1,z1,block.AIR)
  mc.setBlocks(x2,y,z2,x2,y+1,z2,block.AIR) 
 
  if dir=="N":
    a=3
  if dir=="S":
    a=2
  if dir=="W":
    a=0
  if dir=="E":
    a=1
 
  mc.setBlock(x1,y-1,z1,109,a)
  mc.setBlock(x2,y-1,z2,109,a)
 
def castle():
    print("Create ground and moat")
    CreateLandscape(33,10,23)  
     
    print("Create outer walls")
    CreateWalls(21,1,5,block.STONE_BRICK,True,True)
     
    print("Create inner walls")
    CreateWalls(13,1,6,block.STONE_BRICK,True,True)
          
    print("Create Keep with 4 levels")
    CreateKeep(5,1,4)
     
    print("Position player on Keep's walkway")
    mc.player.setPos(0,30,4)

def roof(t, pos_x, pos_y, pos_z, size_x, size_z):
    height = (size_x+1)/2
    for x in range(0, size_x):
        y = x if x<height else size_x-1-x
        mc.setBlocks(pos_x+x, pos_y+y, pos_z, pos_x+x, pos_y+y+1, pos_z+size_z, t)
        if(y+1<=height):
            mc.setBlocks(pos_x+x, pos_y+y+2, pos_z, pos_x+x, pos_y+height+1, pos_z+size_z, block.AIR.id)

def house(roof_block, wall_block, x, y, z, width, depth, height):
    # assemble your function here!
    mc.setBlocks(x, y, z, x+width-1, y+height-1, z+depth-1, wall_block)
    mc.setBlocks(x+1, y, z+1, x+width-2, y+height-1, z+depth-2, block.AIR.id)
    roof(roof_block, x-1, y+height-width/2, z-1, width+2, depth+2)
    mc.setBlocks(x+(width-1)/2, y, z, x+width/2, y+2, z, block.AIR.id)

def village():
    reset()
    blocks = [block.SANDSTONE, block.SNOW_BLOCK, block.STONE, block.BRICK_BLOCK, block.MELON]
    for i in range(0, 10):
        house(blocks[random.randrange(0,len(blocks))],blocks[random.randrange(0,len(blocks))],i*10,0,0,random.randrange(5,8),random.randrange(5,8), random.randrange(6,15))
    mc.player.setPos(20,0,30)

def megaJump():
    x, y, z, = mc.player.getTilePos()
    mc.player.setPos(x,100,z)
