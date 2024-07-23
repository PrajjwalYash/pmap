import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os
def layout(ns, mission_details):

    cur_path = os.getcwd()
    # Panel dimensions
    panel_width = mission_details['L']
    panel_height = mission_details['W']

    # Subpanel dimensions
    subpanel_width = panel_width/mission_details['sub_panel_num_width']
    subpanel_height = panel_height/ mission_details['sub_panel_num_height']

    # Rectangle dimensions
    rect_width = ns/11 * 0.04
    rect_height = 11 * 0.08

    # Spacing
    spacing_x = 0.001
    spacing_y = 0.001

    # Initialize variables
    rectangles = []
    subpanel_rectangles = set()  # Set to keep track of rectangles in each subpanel

    # Function to check if a rectangle is within a subpanel
    def is_within_subpanel(x, y, subpanel_x, subpanel_y):
        return x >= subpanel_x and x + rect_width <= subpanel_x + subpanel_width and y >= subpanel_y and y + rect_height <= subpanel_y + subpanel_height

    # Generate rectangles for each subpanel
    for i in range(int(panel_width / subpanel_width)):
        for j in range(int(panel_height / subpanel_height)):
            # Calculate starting coordinates of the subpanel
            subpanel_x = i * subpanel_width
            subpanel_y = j * subpanel_height
            
            # Add rectangles to the subpanel
            current_x = subpanel_x
            current_y = subpanel_y
            while current_y + rect_height <= subpanel_y + subpanel_height:
                while current_x + rect_width <= subpanel_x + subpanel_width:
                    # Check if rectangle is within the subpanel and not already in another subpanel
                    if is_within_subpanel(current_x, current_y, subpanel_x, subpanel_y) and (current_x, current_y) not in subpanel_rectangles:
                        rect = Rectangle((current_x, current_y), rect_width, rect_height, edgecolor='black', facecolor='none')
                        rectangles.append(rect)
                        subpanel_rectangles.add((current_x, current_y))
                    
                    current_x += rect_width + spacing_x
                current_x = subpanel_x
                current_y += rect_height + spacing_y

    # Plotting
    fig, ax = plt.subplots(figsize=(20,12))
    ax.set_xlim(0, panel_width)
    ax.set_ylim(0, panel_height)

    # Add rectangles to the plot
    for rect in rectangles:
        ax.add_patch(rect)

    ax.set_aspect('equal', 'box')
    ax.invert_yaxis()
    ax.axhline(subpanel_height, ls='--', color='forestgreen')
    ax.axhline(subpanel_height * 2, ls='--', color='forestgreen')
    ax.axvline(subpanel_width, ls='--', color='forestgreen')
    ax.set_title(mission_details['mission_name']+' \n solar array layout visualization', fontsize = 30)
    folder_path = os.path.join(cur_path, 'Plots/', mission_details['mission_name']+'_panel_layout.png')
    plt.savefig(folder_path)

    # Number of rectangles
    num_rectangles = len(rectangles)
    print("Number of parallels from layout:", num_rectangles)
    return num_rectangles
