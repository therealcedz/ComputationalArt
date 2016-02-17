""" TODO: Put your header comment here 
@author: Cedric Kim

Computational Art program
"""

import random
import math
from PIL import Image

####FUNCTIONS FOR COMPUTATIONAL IMAGING##########
#################################################
#################################################
def build_random_function(min_depth, max_depth, t_present):         ###if t_present = false, can use in movie function
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """
    random_depth = random.randint(0, max_depth - min_depth)        #create random number between min and max_depth
    if(max_depth <= random_depth + 1):                          #will run end case between min and max_depth
        if t_present:
            random_number = random.randint(1,3)                        #choose x or y or t at random
        else:
            random_number = random.randint(1,2)                        #choose x or y at random
        if random_number == 1:
            return ['x']
        elif random_number == 2:
            return ['y']
        else:
            return ['t']
    else:
        random_number = random.randint(1,6)                        #choose any of these 6 functions at random
        if(random_number == 1):
            return ['prod', build_random_function(min_depth - 1, max_depth - 1, t_present), build_random_function(min_depth - 1, max_depth - 1, t_present)]
        elif(random_number == 2):
            return ['avg', build_random_function(min_depth - 1, max_depth - 1, t_present), build_random_function(min_depth - 1, max_depth - 1, t_present)]
        elif(random_number == 3):
            return ['cos_pi', build_random_function(min_depth - 1, max_depth - 1, t_present)]
        elif(random_number == 4):
            return ['sin_pi', build_random_function(min_depth - 1, max_depth - 1, t_present)]
        elif(random_number == 5):
            return['power', build_random_function(min_depth - 1, max_depth - 1, t_present)]
        else:
            return['abs', build_random_function(min_depth - 1, max_depth - 1, t_present)]

def evaluate_random_function(f, x, y, t):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(["x"],-0.5, 0.75, 0.9)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02, 0.5)
        0.02
        >>> evaluate_random_function(["k"],0.1,0.02, 0.5)
        0
        >>> evaluate_random_function(["cos_pi", ["y"]],0.5,1, 0.5)
        -1.0
        >>> evaluate_random_function(["prod", ["x"], ["y"]],0.5,0.5, 0.5)
        0.25
        >>> evaluate_random_function(["avg", ["x"], ["t"]],0.5,0.5, 0.5)
        0.5
        >>> evaluate_random_function(["power", ["t"]],0.5,0.5, 0.5)
        0.25
    """
    if f[0] == 'avg':             #take first string in list, check which function
        return (evaluate_random_function(f[1], x, y, t) + evaluate_random_function(f[2], x, y, t))/2
    elif f[0] == 'cos_pi':
        return math.cos(math.pi*evaluate_random_function(f[1], x, y, t))
    elif f[0] == 'sin_pi':
        return math.sin(math.pi*evaluate_random_function(f[1], x, y, t))
    elif f[0] == 'prod':
        return (evaluate_random_function(f[1], x, y, t)*evaluate_random_function(f[2], x, y, t))
    elif f[0] == 'power':
        return evaluate_random_function(f[1], x, y, t)**2
    elif f[0] == 'abs':
        return abs(evaluate_random_function(f[1], x, y, t))
    elif f[0] == 'x':
        return x
    elif f[0] == 'y':
        return y
    elif f[0] == 't':
        return t
    else:
        return 0                #if string is not x or y, or any function

def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
        >>> remap_interval(5, 1, 2, 4, 5)           #this doctest tests if val is out of the input range
        0
        >>> remap_interval(5, 1, 1, 5, 7)
        0
        >>> remap_interval(5, 1, 5, 6, 8)
        8.0
    """
    if(val > input_interval_end or val < input_interval_start):                #checks val in input range
        return 0
    input_interval_length = input_interval_end - input_interval_start             #take input difference
    output_interval_length = output_interval_end - output_interval_start        #take output difference
    if(input_interval_length == 0 or output_interval_length == 0):              # checks division by 0
        return 0
    input_interval_ratio = 1.0*(val - input_interval_start)/ input_interval_length    #create the scaling factor
    
    return input_interval_ratio*output_interval_length + output_interval_start  #scale input to output, and add output start

def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)

def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(7,9, False)
    green_function = build_random_function(7,9, False)
    blue_function = build_random_function(7,9, False)
    #last parameter is false, meaning t will not be in the function
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    t = 0
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y, t)),
                    color_map(evaluate_random_function(green_function, x, y, t)),
                    color_map(evaluate_random_function(blue_function, x, y, t))
                    )

    #im.save('/movie_art', 'PNG')
    im.save(filename)



####FUNCTIONS FOR COMPUTATIONAL MOVIE############
#################################################
#################################################


def generate_movie(x_size = 350, y_size = 350, frames = 200):
    """ Generate computational art and save multiple image files.
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - runs once!
    red_function = build_random_function(8,9, True)
    green_function = build_random_function(8,9, True)
    blue_function = build_random_function(8,9, True)
    print red_function
    print green_function
    print blue_function
    # true means there will be functions of t within the function
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for k in range(frames):         #this takes care of the time dimension
        for i in range(x_size):
            for j in range(y_size):
                x = remap_interval(i, 0, x_size, -1, 1)
                y = remap_interval(j, 0, y_size, -1, 1)
                t = remap_interval(k, 0, frames, -1, 1)
                pixels[i, j] = (
                        color_map(evaluate_random_function(red_function, x, y, t)),
                        color_map(evaluate_random_function(green_function, x, y, t)),
                        color_map(evaluate_random_function(blue_function, x, y, t))
                        )

        frame_number = 'frame{}'.format(k)   ##creates new file for each k
        im.save('/home/cedric/ComputationalArt/movie_art/' + frame_number + '.png', 'PNG')  ##stores it in movie_art
        ##change path file to make this program run

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    #doctest.run_docstring_examples(evaluate_random_function, globals())
    # Create some computational art!

    ###uncomment this to generate art
    #generate_art("myart.png")

    ###uncomment this to generate frames for a movie
    generate_movie()








