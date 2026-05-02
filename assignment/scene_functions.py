"""
DIGM 131 - Assignment 3: Function Library (scene_functions.py)
===============================================================

OBJECTIVE:
    Create a library of reusable functions that each generate a specific
    type of scene element. This module will be imported by main_scene.py.

REQUIREMENTS:
    1. Implement at least 5 reusable functions.
    2. Every function must have a complete docstring with Args and Returns.
    3. Every function must accept parameters for position and/or size so
       they can be reused at different locations and scales.
    4. Every function must return the name(s) of the Maya object(s) it creates.
    5. Follow PEP 8 naming conventions (snake_case for functions/variables).

GRADING CRITERIA:
    - [30%] At least 5 functions, each creating a distinct scene element.
    - [25%] Functions accept parameters and use them (not hard-coded values).
    - [20%] Every function has a complete docstring (summary, Args, Returns).
    - [15%] Functions return the created object name(s).
    - [10%] Clean, readable code following PEP 8.
"""

import maya.cmds as cmds
import math

def create_building(width=4, height=8, depth=4, position=(0, 0, 0)):
    """Create a simple building from a cube, placed on the ground plane.
    obj = cmds.polyCube(w=width, h=height, d=depth)[0]

    The building is a single scaled cube whose base sits at ground level
    (y = 0) at the given position.

    Args:
        width (float): Width of the building along the X axis.
        height (float): Height of the building along the Y axis.
        depth (float): Depth of the building along the Z axis.
        position (tuple): (x, y, z) ground-level position. The building
            base will rest at this point; y is typically 0.

    Returns:
        str: The name of the created building transform node.
    """
    # TODO: Implement this function.
    #   1. Create a polyCube with the given width, height, and depth.
    #   2. Move it so its base sits on the ground at 'position'.
    #      Hint: offset Y by height / 2.0.
    #   3. Return the object name.

    # Creates a cube for the building and it's demensions
    building = cmds.polyCube(width = width, height = height, depth = depth)[0]
    
    # telling the cube where to go and where to sit on the ground  
    cmds.move(position[0], position[1] + height / 2.0, position[2], building)
    
    # returns objects to their name 
    return building

def create_tree(trunk_radius=0.3, trunk_height=3, canopy_radius=2, position=(0, 0, 0)):
    """Create a simple tree using a cylinder trunk and a sphere canopy.

    Args:
        trunk_radius (float): Radius of the cylindrical trunk.
        trunk_height (float): Height of the trunk cylinder.
        canopy_radius (float): Radius of the sphere used for the canopy.
        position (tuple): (x, y, z) ground-level position for the tree base.

    Returns:
        str: The name of a group node containing the trunk and canopy.
    """
    # TODO: Implement this function.
    #   1. Create a polyCylinder for the trunk and position it.
    #   2. Create a polySphere for the canopy, positioned on top of the trunk.
    #   3. Group trunk and canopy together using cmds.group().
    #   4. Move the group to 'position'.
    #   5. Return the group name.
                    
    # Creates a cylinder for the trunk, it's demensions, and where to sit on the ground
    trunk = cmds.polyCylinder(radius=trunk_radius, height=trunk_height)[0] 
    cmds.move(0, trunk_height / 2.0, 0, trunk)
    
    # Creates a sphere, it's demensions, nd where to sit on top of the trunk
    canopy = cmds.polySphere(radius=canopy_radius)[0]
    cmds.move(0, trunk_height + canopy_radius, 0, canopy)
    
    # Group trunk and canopy together and return the group name
    tree_grp = cmds.group(trunk, canopy, name="tree_grp")
    cmds.move(position[0], position[1], position[2], tree_grp)
    
    return tree_grp

def create_fence(length=10, height=1.5, post_count=6, position=(0, 0, 0)):
    """Create a simple fence made of posts and rails.

    The fence runs along the X axis starting at the given position.

    Args:
        length (float): Total length of the fence along the X axis.
        height (float): Height of the fence posts.
        post_count (int): Number of vertical posts (must be >= 2).
        position (tuple): (x, y, z) starting position of the fence.

    Returns:
        str: The name of a group node containing all fence parts.
    """
    # TODO: Implement this function.
    #   1. Calculate spacing between posts: length / (post_count - 1).
    #   2. Loop to create 'post_count' thin, tall cubes as posts.
    #   3. Create a long, thin cube as a horizontal rail connecting them.
    #   4. Group everything and move to 'position'.
    #   5. Return the group name.

    # the post will be spaced out horizontally
    parts = []
    spacing = length / (post_count -1)
 
  for i in range(post_count):
        post = cmds.polyCube(width=0.2, height=height, depth=0.2)[0]
        cmds.move(i * spacing, height / 2.0, 0, post)
        parts.append(post)

    #now creaitng the rails    
    rail = cmds.polyCube(width=length, height=0.2, depth=0.2)[0]
    cmds.move(position[0] + length / 2.0, position[1] + height - 0.1, position[2], rail)
    parts.append(rail)

    # Group fence together and return the group name
    fence_group = cmds.group(parts)
    cmds.move(position[0], position[1], position[2], fence_group)

    return fence_group
 

def create_lamp_post(pole_height=5, light_radius=0.5, position=(0, 0, 0)):
    """Create a street lamp using acylinder pole and a sphere light.

    Args:
        pole_height (float): Height of the lamp pole.
        light_radius (float): Radius of the sphere representing the light.
        position (tuple): (x, y, z) ground-level position.

    Returns:
        str: The name of a group node containing the pole and light.
    """
    # TODO: Implement this function.
    #   1. Create a thin polyCylinder for the pole.
    #   2. Create a polySphere for the light, placed at the top of the pole.
    #   3. Group them, move to 'position', and return the group name.

    # Creating pole from a cylinder, it's dimensions, and where it will sit on the ground 
    pole = cmds.polyCylinder(radius=0.1, height=pole_height)[0]
    cmds.move(0, pole_height/ 2.0, 0, pole)
    
    # Create light from a sphere, it's dimensions, and where it sits on top of pole
    light = cmds.polySphere(radius=light_radius)[0]
    cmds.move(0, pole_height + light_radius, 0, light)
    
    # Group lamp together and return the group name
    lamp_grp = cmds.group(pole, light, name="lamp_grp")
    
    return lamp_grp

 # placing objects in a circle
def place_in_circle(create_func, count=8, radius=10, center=(0, 0, 0),
                     **kwargs):
    
    """Place objects created by 'create_func' in a circular arrangement.

    This is a higher-order function: it takes another function as an
    argument and calls it repeatedly to place objects around a circle.

    Args:
        create_func (callable): A function from this module (e.g.,
            create_tree) that accepts a 'position' keyword argument
            and returns an object name.
        count (int): Number of objects to place around the circle.
        radius (float): Radius of the circle.
        center (tuple): (x, y, z) center of the circle.
        **kwargs: Additional keyword arguments passed to create_func
            (e.g., trunk_height=4).

    Returns:
        list: A list of object/group names created by create_func.
    """
    # TODO: Implement this function.
    #   1. Import the math module (at the top of the file or here).
    #   2. Loop 'count' times. For each iteration:
    #       a. Calculate the angle: angle = 2 * math.pi * i / count
    #       b. Calculate x = center[0] + radius * math.cos(angle)
    #       c. Calculate z = center[2] + radius * math.sin(angle)
    #       d. Call create_func(position=(x, center[1], z), **kwargs)
    #       e. Append the returned name to a results list.
    #   3. Return the results list.
    
    results = []
    group = cmds.group(empty=True, name="circle_group")                     
   
# Calculates the angle                
    for i in range(count):
        angle = (2 * math.pi / count) * i

        # Calculate x and z with radius 
        position_x = center[0] + math.cos(angle) * radius
        position_z = center[2] + math.sin(angle) * radius
        
        obj = create_func(position=(position_x, center[1], position_z), **kwargs)
        results.append(obj)
                         
    #returns results
    return results
