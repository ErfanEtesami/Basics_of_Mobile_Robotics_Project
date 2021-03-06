import math
import numpy as np
import matplotlib.pyplot as plt

    
def plot(ax1, ax2, ax3, x_est, P_est, fig):
    """
    Plots all the gaussians
    
    param ax1: axis to plot
    param ax2: axis to plot
    param ax3: axis to plot
    param x_est: last estimated state of Thymio
    param P_est: Last estimated covariance matrix of Thymio
    """

    x1, y1 = gauss(x_est[0][0], P_est[0][0])
    x2, y2 = gauss(x_est[1][0], P_est[1][1])
    x3, y3 = gauss(x_est[2][0], P_est[2][2], 1)
    
    ax1.clear()
    ax2.clear()
    ax3.clear()

    ax1.set_xlabel('X (mm)')
    ax1.set_ylabel('Gauss')
    
    ax2.set_xlabel('Y (mm)')
    ax2.set_ylabel('Gauss')
    
    ax3.set_xlabel('Theta (deg)')
    ax3.set_ylabel('Gauss')
    
    ax1.plot(x1, y1, 'g')
    ax2.plot(x2, y2, 'r')
    ax3.plot(x3, y3, 'y')
    fig.canvas.draw()

  

def gauss(mu, var, deg = 0):
    """
    Computes all the gaussians
    """
    
    if deg == 0 :
        x = np.linspace(mu - 5 , mu + 5, 200)
        
    else :
        var *= (180/math.pi)**2
        mu *= (180/math.pi)
        x = np.linspace(mu - 6,  mu + 6, 200)
        
    y = []
    
    for e in x:
        y.append(1/math.sqrt(2 * math.pi * var) * math.exp(-(e - mu)**2/(2 * var)))
        
        

    return x, y     


def rotate(angle, coords):
    """
    Rotates the coordinates of a matrix by the desired angle
    :param angle: angle in radians by which we want to rotate
    :return: numpy.array() that contains rotated coordinates
    """
    R = np.array(((np.cos(angle), -np.sin(angle)),
                  (np.sin(angle),  np.cos(angle))))
    
    return R.dot(coords.transpose()).transpose()
     
    
def plot_test(ax1, ax2, ax3, ax4, x_est, P_est, fig):
    """
    Manages the plotting for the test of Kalman
    
    param ax1: axis to plot
    param ax2: axis to plot
    param ax3: axis to plot
    param ax4: axis to plot
    param x_est: last estimated state of Thymio
    param P_est: Last estimated covariance matrix of Thymio
    """

    # Thymio outline
    center_offset = np.array([5.5,5.5])
    thymio_coords = np.array([[0,0], [11,0], [11,8.5], [10.2, 9.3], 
                              [8, 10.4], [5.5,11], [3.1, 10.5], 
                              [0.9, 9.4], [0, 8.5], [0,0]]) - center_offset
                              
    thymio_coords *= 10
    
    rotated_thymio_coords = rotate(- x_est[2][0], thymio_coords) 
    abs_Thymio_coords = rotated_thymio_coords + np.array([x_est[1][0], x_est[0][0]])
    x1 = abs_Thymio_coords[:, 0]
    y1 = abs_Thymio_coords[:, 1]
    
    x2, y2 = gauss(x_est[0][0], P_est[0][0])
    x3, y3 = gauss(x_est[1][0], P_est[1][1])
    x4, y4 = gauss(x_est[2][0], P_est[2][2], 1)
    
    ax1.clear()
    ax2.clear()
    ax3.clear()
    ax4.clear()
    
    ax1.set_xlabel('Y')
    ax1.set_ylabel('X')
    ax1.set_xlim(0,1280)
    ax1.set_ylim(0,720)
    ax1.invert_yaxis()
    ax1.set_aspect('equal', 'box')

    ax2.set_xlabel('X (mm)')
    ax2.set_ylabel('Gauss')
    
    ax3.set_xlabel('Y (mm)')
    ax3.set_ylabel('Gauss')
    
    ax4.set_xlabel('Theta (deg)')
    ax4.set_ylabel('Gauss')
    
    ax1.plot(x1, y1, 'b')
    ax2.plot(x2, y2, 'g')
    ax3.plot(x3, y3, 'r')
    ax4.plot(x4, y4, 'y')
    fig.canvas.draw()    
    