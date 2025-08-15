import gc
import framebuf
import time

# nano gui
from color_setup import ssd
from gui.core.nanogui import refresh
from gui.core.writer import Writer  # Renders custom text fonts
from gui.widgets.label import Label
import gui.fonts.Square_12 as Square_12
import gui.fonts.Aldrich_Regular_30 as Aldrich_Regular_30



class ImagePBM:
    def __init__(self, parent_buffer, image_file, pos_x = None, pos_y = None):
        # Based on source: https://peppe8o.com/raspberry-pi-pico-epaper-eink/
        # WIP
        self.parent_buffer = parent_buffer
        self.image_file = image_file
        self.pos_x = pos_x
        self.pos_y = pos_y
        
        self.w = 0
        self.h = 0
        self.data = None
        self.fbuf = None
        
        self._load_image(image_file)
        
        if self.pos_x is not None and self.pos_y is not None:
            self.show(self.pos_x, self.pos_y)
            
    def update(self, image_file, pos_x = None, pos_y = None):
        self.hide()
        self.image_file = image_file
        self._load_image(image_file)
        
        if pos_x is not None and pos_y is not None:
            self.pos_x = pos_x
            self.pos_y = pos_y
        
        self.show(self.pos_x, self.pos_y)

    def _load_image(self, image_file):
        with open(image_file, 'rb') as f:
            f.readline()
            f.readline()
            size = f.readline().decode('utf-8')
            (self.w, self.h) = size.split('\n')[0].split(' ')
            self.data = bytearray(f.read())
        
    @property
    def width(self):
        return int(self.w)
    
    @property
    def height(self):
        return int(self.h)
    
    def hide(self):
        self.fbuf.fill(0)
        self.parent_buffer.blit(self.fbuf, self.pos_x, self.pos_y, 1)
        
    def show(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        
        msg = f'[{self.__class__.__name__}] Showing image file "{self.image_file}" at ({self.pos_x}, {self.pos_y})\n'
        msg += f'with dimensions of width = {self.w} px and height = {self.h} px.'
        
        print(msg)

        self.fbuf = framebuf.FrameBuffer(self.data, int(self.w), int(self.h), framebuf.MONO_HLSB)
        self.parent_buffer.blit(self.fbuf, self.pos_x, self.pos_y)


# Load fonts for GUI

Writer.set_textpos(ssd, 0, 0)  # In case previous tests have altered it
wri1 = Writer(ssd, Square_12, verbose=False)
wri1.set_clip(True, True, False)

wri2 = Writer(ssd, Aldrich_Regular_30, verbose=False)
wri2.set_clip(True, True, False)


# Start GUI
refresh(ssd, True)  # Initialise and clear display.


# Using micropython's primitive draw functions
# Drawing a border
thickness = 5
width = 296
height = 128

ssd.rect(0, 0, width, thickness, 1, 1) # top
ssd.rect(0, 0, thickness, height, 1, 1) # left
ssd.rect(width - thickness, 0, thickness, height, 1, 1) # right
ssd.rect(0, height - thickness, width, thickness, 1, 1) # bottom

# Displaying some text (standard 8x8 monospace font)
text_margin = 3
text_content = 'Micropython standard 8x8 font'
ssd.text(text_content, thickness + text_margin,
         height - thickness - 8 - text_margin)


offset = 70
# Using nanogui Label class with a custom font
# This label's text is centered and it's value can be updated
large_label = Label(wri2, 30, thickness + offset, width - 2 * thickness- offset, align=2)
large_label.value('Large Font')

small_label = Label(wri1, 70, thickness + offset, width - 2 * thickness- offset, align=2)
small_label.value('Small Font')

image = ImagePBM(ssd, 'Hamster_100.pbm')
image.show(thickness + text_margin, thickness + text_margin)

refresh(ssd)


# --------------------  update gui  content after 10 s -------------------------
time.sleep(10)
large_label.value('Update')
small_label.value('New value!')

# MPY text needs to be paint over by a white filled rect
# to 'delete' it
ssd.rect(thickness + text_margin, height - thickness - 8 - text_margin,
         len(text_content) * 8, 8, 0, 1)

ssd.text('Updated MPY text', thickness + text_margin,
         height - thickness - 8 - text_margin)

image.update('Hamster_meal.pbm',  14, 8)
refresh(ssd)



# --------------------  update gui  content after 10 s -------------------------
# time.sleep(10)
# image.hide()
# 
# refresh(ssd)

print('Demo finished.')