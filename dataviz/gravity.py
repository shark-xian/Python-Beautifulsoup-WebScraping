import sys
import matplotlib.pyplot as plt
sys.path.append('..')
from pillar import *
from PIL import ImageOps
from toolz.functoolz import memoize

def magnitude_array(arr, normalised=True):
    mag = np.vectorize(np.linalg.norm)(arr)
    return mag / mag.max() if normalised else mag

def direction_array(arr):
    def direction(v):
        angle = np.arctan2(v[0], v[1]) / (2 * np.pi)
        return angle + 1 if angle < 0 else angle
    return np.vectorize(direction)(arr)

# slow precise calculation

def inverse_square_array(w, h):
    def generate(i, j):
        vec = np.array([w-1-i, h-1-j])
        norm = np.linalg.norm(vec)
        return vec / ((norm ** 3) + int(norm == 0))
    return np.fromfunction(np.frompyfunc(generate, 2, 1), (2*w-1, 2*h-1), dtype=int)
    
def gravity_array(arr):
    w,h = arr.shape
    isq = inverse_square_array(w, h)
    def convolve(i, j): return (arr * isq[w-1-i:w-1-i+w,h-1-j:h-1-j+h]).sum()
    return np.fromfunction(np.frompyfunc(convolve, 2, 1), arr.shape, dtype=int)

# faster quadtree estimate

class QuadTree(object):

    def __new__(cls, array, x=0, y=0):
        """Generate hierarchical QuadTree object, or None if the array is zero."""
        w,h = array.shape[0], array.shape[1]
        assert w == h, "QuadTree input array must be a square"
        if array.size == 1: # leaf node
            if array[0,0] == 0: return None
            children = None
        else: # internal node
            assert w % 2 == 0, "QuadTree input array size be a power of two"
            children = [QuadTree(array[i:i+w//2,j:j+h//2], x+i, y+j) for (i,j) in itertools.product([0,w//2],[0,h//2])]
            if not any(children): return None
        self = super(QuadTree, cls).__new__(cls)
        self.children = children
        return self

    def __init__(self, array, x=0, y=0):
        """Initialize a QuadTree object."""
        self.width = array.shape[0]
        if array.size == 1:
            self.mass = array[0,0]
            self.com = np.array([x,y])
        else:
            self.mass = sum(c.mass for c in self.children if c is not None)
            self.com = sum(c.com * c.mass for c in self.children if c is not None) / self.mass
            
    def __repr__(self):
        return "<QuadTree mass={} com={}>".format(self.mass, self.com)

def gravity(qtree, loc, theta):
    v = loc - qtree.com
    d = np.linalg.norm(v)
    if qtree.width == 1 or d > 0 and qtree.width / d < theta:
        return 0 if d == 0 else v * qtree.mass / (d**3)
    return sum(gravity(c, loc, theta) for c in qtree.children if c is not None)
   
def qtree_gravity_array(arr, theta=0.8, memo=False):
    padded_size = 1 << (max(arr.shape)-1).bit_length()
    padded = np.pad(arr, [(0, padded_size - arr.shape[0]), (0, padded_size - arr.shape[1])], mode='constant')
    qtree = QuadTree(padded)
    def calculate(i, j): return gravity(qtree, np.array([i, j]), theta, normer)
    return np.fromfunction(np.frompyfunc(calculate, 2, 1), arr.shape, dtype=int)
    
# visualisation

def heatmap(grav, cmap="hot"):
    cmap = plt.get_cmap(cmap)
    mag =  np.uint8(magnitude_array(grav) * 255)
    return Image.fromarray(cmap(mag, bytes=True))
    
def hsvmap(grav):
    hue, sat, val = direction_array(grav), np.full(grav.shape, 0.7), magnitude_array(grav)
    stacked = np.stack((np.uint8(hue * 255), np.uint8(sat * 255), np.uint8(val * 255)), axis=2)
    return Image.fromarray(stacked, mode="HSV").convert("RGBA")
   
def icon_to_array(file="icons/color.png", width=64):
    img = Image.open(file).remove_transparency().resize_fixed_aspect(width=width).convert('L')
    return np.array(ImageOps.invert(img)) / 256
    
def array_to_img(arr, base="red"):
    rgba = ImageColor.getrgba(base)
    def colfn(channel): return np.uint8(255 - ((255 - channel) * arr / arr.max()))
    stacked = np.stack((colfn(rgba.red), colfn(rgba.green), colfn(rgba.blue)), axis=2)
    return Image.fromarray(stacked)
