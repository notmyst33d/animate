#!/usr/bin/env python3
import os
import sys
import json
import shutil

import cairosvg
import numpy as np

try:
    shutil.rmtree("out")
except:
    pass
os.mkdir("out")

if len(sys.argv) < 3:
    print("Usage: animate.py my_animation.json my_design.svg")
    exit()

animation_data = json.loads(open(sys.argv[1], "r").read())
svg_file = open(sys.argv[2], "r").read()

current_frame = 0

for loop in range(0, animation_data["loop"]):
    for entry in animation_data["data"]:
        frame_data = zip(
            # Interpolate X and Y of the point 1 and point 2
            np.linspace(
                entry["pos1_position_from"][0],
                entry["pos1_position_to"][0], num=entry["frames"]
            ),
            np.linspace(
                entry["pos1_position_from"][1],
                entry["pos1_position_to"][1], num=entry["frames"]
            ),
            np.linspace(
                entry["pos2_position_from"][0],
                entry["pos2_position_to"][0], num=entry["frames"]
            ),
            np.linspace(
                entry["pos2_position_from"][1],
                entry["pos2_position_to"][1], num=entry["frames"]
            ),
            # Interpolate RGB values of the point 1
            np.linspace(
                entry["pos1_color_from"][0],
                entry["pos1_color_to"][0], num=entry["frames"], dtype=int
            ),
            np.linspace(
                entry["pos1_color_from"][1],
                entry["pos1_color_to"][1], num=entry["frames"], dtype=int
            ),
            np.linspace(
                entry["pos1_color_from"][2],
                entry["pos1_color_to"][2], num=entry["frames"], dtype=int
            ),
            # Interpolate RGB values of the point 2
            np.linspace(
                entry["pos2_color_from"][0],
                entry["pos2_color_to"][0], num=entry["frames"], dtype=int
            ),
            np.linspace(
                entry["pos2_color_from"][1],
                entry["pos2_color_to"][1], num=entry["frames"], dtype=int
            ),
            np.linspace(
                entry["pos2_color_from"][2],
                entry["pos2_color_to"][2], num=entry["frames"], dtype=int
            ),
        )

        # Render the interpolated frames
        for pos1_x, pos1_y, pos2_x, pos2_y, pos1_r, pos1_g, pos1_b, pos2_r, pos2_g, pos2_b in frame_data:
            # Copy original SVG file
            inter_frame = svg_file

            # Place interpolated X and Y
            inter_frame = inter_frame.replace(
                "{pos1_x}", str(pos1_x))
            inter_frame = inter_frame.replace(
                "{pos1_y}", str(pos1_y))
            inter_frame = inter_frame.replace(
                "{pos2_x}", str(pos2_x))
            inter_frame = inter_frame.replace(
                "{pos2_y}", str(pos2_y))

            # Place interpolated RGB
            inter_frame = inter_frame.replace(
                "{pos1_color}", f"{pos1_r},{pos1_g},{pos1_b}")
            inter_frame = inter_frame.replace(
                "{pos2_color}", f"{pos2_r},{pos2_g},{pos2_b}")

            cairosvg.svg2png(
                bytestring=inter_frame.encode(),
                write_to=f"out/{current_frame}.png"
            )

            print(f"Rendered frame {current_frame}")
            current_frame += 1

os.system(
    f"ffmpeg -y -r {animation_data['fps']} -i out/%0d.png -pix_fmt yuv420p \"{animation_data['name']}.{animation_data['ext']}\"")
