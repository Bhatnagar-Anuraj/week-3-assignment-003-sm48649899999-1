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
    """Create a simple building (scaled cube) at a given position.

    Args:
        width (float): Width along X axis.
        height (float): Height along Y axis.
        depth (float): Depth along Z axis.
        position (tuple): (x, y, z) ground position.

    Returns:
        str: Name of building transform.
    """

    # Creates a cube for the building and its dimensions
    building = cmds.polyCube(w=width, h=height, d=depth)[0]

    # telling the cube where to go and where to sit on the ground
    cmds.move(position[0], position[1] + height / 2.0, position[2], building)

    # returns object name
    return building


def create_tree(trunk_radius=0.3, trunk_height=3, canopy_radius=2, position=(0, 0, 0)):
    """Create a simple tree using a cylinder trunk and sphere canopy.

    Args:
        trunk_radius (float): Radius of trunk.
        trunk_height (float): Height of trunk.
        canopy_radius (float): Radius of canopy.
        position (tuple): Ground position.

    Returns:
        str: Name of tree group.
    """

    # Creates a cylinder for the trunk and its dimensions
    trunk = cmds.polyCylinder(r=trunk_radius, h=trunk_height)[0]

    # positions trunk on ground
    cmds.move(0, trunk_height / 2.0, 0, trunk)

    # Creates a sphere for canopy and its dimensions
    canopy = cmds.polySphere(r=canopy_radius)[0]

    # places canopy on top of trunk
    cmds.move(0, trunk_height + canopy_radius, 0, canopy)

    # Group trunk and canopy together
    tree_grp = cmds.group(trunk, canopy)

    # move whole tree to position
    cmds.move(position[0], position[1], position[2], tree_grp)

    return tree_grp


def create_fence(length=10, height=1.5, post_count=6, position=(0, 0, 0)):
    """Create a simple fence using posts and a rail.

    Args:
        length (float): Total fence length.
        height (float): Height of posts.
        post_count (int): Number of posts.
        position (tuple): Start position.

    Returns:
        str: Name of fence group.
    """

    # the posts will be spaced out horizontally
    parts = []
    spacing = length / (post_count - 1)

    for i in range(post_count):
        post = cmds.polyCube(w=0.2, h=height, d=0.2)[0]

        # position each post along the fence
        cmds.move(position[0] + i * spacing,
                  position[1] + height / 2.0,
                  position[2],
                  post)

        parts.append(post)

    # now creating the rail
    rail = cmds.polyCube(w=length, h=0.2, d=0.2)[0]

    # position rail on top of posts
    cmds.move(position[0] + length / 2.0,
              position[1] + height - 0.1,
              position[2],
              rail)

    parts.append(rail)

    # Group fence together
    fence_group = cmds.group(*parts)

    # move whole fence to position
    cmds.move(position[0], position[1], position[2], fence_group)

    return fence_group


def create_lamp_post(pole_height=5, light_radius=0.5, position=(0, 0, 0)):
    """Create a street lamp using a pole and light sphere.

    Args:
        pole_height (float): Height of lamp pole.
        light_radius (float): Radius of light.
        position (tuple): Base position.

    Returns:
        str: Name of lamp group.
    """

    # Creating pole from a cylinder and its dimensions
    pole = cmds.polyCylinder(r=0.1, h=pole_height)[0]

    # position pole on ground
    cmds.move(0, pole_height / 2.0, 0, pole)

    # Create light from a sphere and its dimensions
    light = cmds.polySphere(r=light_radius)[0]

    # place light on top of pole
    cmds.move(0, pole_height + light_radius, 0, light)

    # Group lamp parts together
    lamp_grp = cmds.group(pole, light)

    # move lamp to position
    cmds.move(position[0], position[1], position[2], lamp_grp)

    return lamp_grp


def place_in_circle(create_func, count=8, radius=10, center=(0, 0, 0), **kwargs):
    """Place objects in a circular arrangement using a function.

    Args:
        create_func (callable): Function that creates an object.
        count (int): Number of objects.
        radius (float): Circle radius.
        center (tuple): Center point.
        **kwargs: Extra args for create_func.

    Returns:
        list: Names of created objects.
    """

    results = []

    # group for objects in the circle
    group = cmds.group(em=True, name="circle_group")

    # Calculates placement around circle
    for i in range(count):
        angle = 2 * math.pi * i / count

        # Calculate x and z position
        position_x = center[0] + radius * math.cos(angle)
        position_z = center[2] + radius * math.sin(angle)

        # create object using passed function
        obj = create_func(position=(position_x, center[1], position_z), **kwargs)

        # parent into group
        cmds.parent(obj, group)

        results.append(obj)

    return results
