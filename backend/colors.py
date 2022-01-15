# In RGB Format
colors = [
   [255,0,0], # Red
   [0,255,0], # Lime
   [0,0,255], # Blue
   [255,255,0], # Yellow
   [0,255,255], # Cyan
   [255,0,255], # Magenta
   [255,128,0], # Orange
   [127,0,255], # Purple
   [255,153,255], # Pink
]

# OpenCV uses BGR instead of RGB for some reason
# So here we reverse all elements of the array
colors = [tuple(reversed(color)) for color in colors]


def get_color(num):
    return colors[num % len(colors)]