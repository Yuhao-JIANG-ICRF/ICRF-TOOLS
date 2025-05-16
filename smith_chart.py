#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 15 15:23:45 2025

@author: YJ281217
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 09:36:06 2025

@author: YJ281217
"""

# %%
'import Library or Package and release ram & close fig' 
import numpy as np
from load import fun_load_touchstone as flt
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

# %% define of simth_chart

def smith_Smatrix(S, num=1, display_mode='points_and_arrows'):
    """
    Plot a Smith chart and mark the S-matrix points on it.
    
    Parameters:
    -----------
    S : complex or array of complex
        The S-matrix values to plot on the Smith chart
    num : int
        Figure number
    display_mode : str
        'points_and_arrows': Show points and connect them with arrows (original behavior)
        'line_with_arrow': Only draw lines with arrow at the end point, no points
        'points_only': Only draw points, no lines or arrows
    """
    chart_color = [0.5, 0.5, 0.5]  # Gray color for the chart lines
    
    theta = np.linspace(0, 2*np.pi, 10001)
    rx = [0, 0.2, 0.5, 1, 2, 5, 10]  # Resistance circles
    ry = [0.2, 0.5, 1, 2, 10]  # Reactance circles
    
    fig = plt.figure(num, figsize=(6.5, 5.5))
    ax = fig.add_subplot(111)
    
    # Plot resistance circles
    for r in rx:
        x = 1/(r+1) * np.cos(theta) + r/(r+1)
        y = 1/(r+1) * np.sin(theta)
        ax.plot(x, y, '-', color=chart_color, linewidth=0.5)
    
    # Plot unit circle
    x = np.cos(theta)
    y = np.sin(theta)
    ax.plot(x, y, 'k', linewidth=1)
    
    # Plot horizontal axis
    ax.plot([-1, 1], [0, 0], '-', color=chart_color, linewidth=0.5)
    
    # Plot reactance circles
    for r in ry:
        x = 1/r * np.cos(theta) + 1
        y = 1/r * np.sin(theta) + 1/r
        
        # Filter points to only include those inside the unit circle
        mask = (x**2 + y**2) <= 1
        
        # Plot positive reactance
        ax.plot(x[mask], y[mask], '-', color=chart_color, linewidth=0.5)
        
        # Plot negative reactance
        ax.plot(x[mask], -y[mask], '-', color=chart_color, linewidth=0.5)
    
    ax.set_aspect('equal')
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.axis('off')
    
    # Add annotations
    Z_text_color = [0.5, 0, 0]  # Dark red color for text
    
    # Annotate reactance circles
    for xx in ry:
        alpha_xx = 2 * np.arctan(1/xx)
        ax.text(1.1*np.cos(alpha_xx), 1.1*np.sin(alpha_xx), f"+{xx:.1f}",
                 horizontalalignment='center', verticalalignment='center',
                 fontsize=12, color=Z_text_color)
        ax.text(1.1*np.cos(alpha_xx), -1.1*np.sin(alpha_xx), f"-{xx:.1f}",
                 horizontalalignment='center', verticalalignment='center',
                 fontsize=12, color=Z_text_color)
    
    # Annotate resistance circles
    for rr in rx[1:]:  # Skip the first element (0)
        xc = rr / (1 + rr)  # Circle center x-coordinate
        rd = 1 / (1 + rr)   # Circle radius
        ax.text(xc - rd, 0, f"{rr:.1f}", 
                 horizontalalignment='left', verticalalignment='bottom',
                 color=Z_text_color, rotation=90, fontsize=12)
    
    # Special annotations for 0 and infinity
    ax.text(-1.1, 0, "0.0", 
             horizontalalignment='center', verticalalignment='center',
             color=Z_text_color, fontsize=12)
    ax.text(1.1, 0, "$\infty$", 
             horizontalalignment='center', verticalalignment='center',
             color=Z_text_color, fontsize=12)
    
    # Ensure S is a numpy array
    S = np.asarray(S)
    
    # Handle different display modes
    if len(S) > 1:
        if display_mode == 'points_only':
            # Only draw points, no lines or arrows
            ax.scatter(np.real(S), np.imag(S), marker='*', color='blue', s=120, linewidth=2, zorder=5)
            
            # Add point labels
            #for i, s_point in enumerate(S):
               # ax.text(np.real(s_point) + 0.05, np.imag(s_point) + 0.05, f"S{i+1}",
                      #  fontsize=10, color='blue', zorder=6)
                
        elif display_mode == 'line_with_arrow':
            # Draw only line with arrow at end, no points
            if len(S) > 1:
                # Create a single continuous line through all points
                x_points = np.real(S)
                y_points = np.imag(S)
                
                # Draw the main line without the last segment
                if len(S) > 2:
                    ax.plot(x_points[:-1], y_points[:-1], '-', color='blue', linewidth=2, zorder=4)
                
                # Draw the last segment with an arrow
                arrow = FancyArrowPatch(
                    (x_points[-2], y_points[-2]),  # Start from second-to-last point
                    (x_points[-1], y_points[-1]),  # End at last point
                    arrowstyle='-|>', 
                    mutation_scale=15,
                    color='blue',
                    linewidth=2,
                    zorder=4
                )
                ax.add_patch(arrow)
                
                # Add point labels if desired (commented out by default)
                # for i, s_point in enumerate(S):
                #     ax.text(np.real(s_point) + 0.05, np.imag(s_point) + 0.05, f"S{i+1}",
                #             fontsize=10, color='blue', zorder=6)
                
        else:  # 'points_and_arrows' (default behavior)
            # Draw points
            ax.scatter(np.real(S), np.imag(S), marker='o', color='blue', s=60, zorder=5)
            
            # Add arrows connecting points in sequence
            for i in range(len(S) - 1):
                start = (np.real(S[i]), np.imag(S[i]))
                end = (np.real(S[i+1]), np.imag(S[i+1]))
                
                arrow = FancyArrowPatch(
                    start, end, 
                    arrowstyle='-|>', 
                    mutation_scale=15,  # Arrow size
                    color='red',
                    linewidth=2,
                    zorder=4
                )
                ax.add_patch(arrow)
            
            # Add point labels
            #for i, s_point in enumerate(S):
               # ax.text(np.real(s_point) + 0.05, np.imag(s_point) + 0.05, f"S{i+1}",
                       # fontsize=10, color='blue', zorder=6)
    else:
        # Single point case - always draw the point
        ax.scatter(np.real(S), np.imag(S), marker='*', color='blue', s=120, linewidth=1.5, zorder=5)
    
    fig.set_facecolor('white')
    
    return fig

# Example usage:
if __name__ == "__main__":
    # Example S-parameters (complex values inside the unit circle)
    S = np.array([0.3 + 0.4j, -0.2 + 0.6j, -0.5 - 0.3j])
    
    # Create three figures to demonstrate all modes
    smith_Smatrix(S, 1, display_mode='points_and_arrows')
    
    smith_Smatrix(S, 2, display_mode='line_with_arrow')
    
    smith_Smatrix(S, 3, display_mode='points_only')
    # %% data file
    pre = 'input/example/'
    fname = 'smatrix_aug-like.s4p'
    fre_unit = 'Hz'
    # %% read data
    fre_units = {'MHz':1e6,'Hz':1}
    fre_u = fre_units[fre_unit]
    #load s4p file, trans to freauency and Smatrix
    fre,S = flt(pre+fname)
    fre = fre*fre_u
    # %% set the data
    x= fre
    S11 = np.array([Smatrix[0,0] for Smatrix in S])
    # %% plot smith chart
    smith_Smatrix(S11, 4,display_mode='line_with_arrow')
    plt.show()




