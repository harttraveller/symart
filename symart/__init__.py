import numpy as np
import matplotlib.pyplot as plt
import math

class SymmetryGroup:
    def __init__(self,points,reflections,rotations,size_mean=30,size_stdev=10):
        self.points = points
        self.reflections = reflections
        self.rotations = rotations
        self.n = 1
        self.size_mean = size_mean
        self.size_stdev = size_stdev

    def deg2rad(self,deg):
        return deg*(np.pi/180)

    def rotate(self,point,angle):
        origin = (0,0)
        angle = self.deg2rad(angle)
        ox, oy = origin
        px, py = point
        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        return qx, qy

    def deg2slope(self,deg):
        if deg == 90:
            deg += 1/1e10
        return np.sin(self.deg2rad(deg))/np.cos(self.deg2rad(deg))

    def reflect(self,point,angle):
        m = self.deg2slope(angle)
        d = (point[0] + (point[1]*m))/(1 + m**2)
        x1 = (2*d) - point[0]
        y1 = (2*d*m) - point[1]
        return (x1,y1)

    def apply_reflections(self):
        reflected_points_x = []
        reflected_points_y = []
        for j in self.reflections:
            for k in self.points:
                x,y = self.reflect((k[0],k[1]),j)
                reflected_points_x.append(x)
                reflected_points_y.append(y)
        return reflected_points_x, reflected_points_y

    def apply_rotations(self):
        rotated_points_x = []
        rotated_points_y = []
        for j in self.rotations:
            for k in self.points:
                x,y = self.rotate((k[0],k[1]),j)
                rotated_points_x.append(x)
                rotated_points_y.append(y)
        return rotated_points_x,rotated_points_y

    def show(self,xlim=(-20,20),ylim=(-20,20)):
        fig = plt.figure(figsize=(8,8))
        ax = fig.add_subplot(111)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        plt.xlim(xlim)
        plt.ylim(ylim)
        reflected_points_x,reflected_points_y = self.apply_reflections()
        rotated_points_x,rotated_points_y = self.apply_rotations()
        original_points_x = [i[0] for i in self.points]
        original_points_y = [i[1] for i in self.points]
        sizes = np.random.normal(self.size_mean,self.size_stdev,len(original_points_x))
        colors = np.linspace(0,1,len(original_points_x))
        ax.scatter(original_points_x,original_points_y,s=sizes,c=colors)
        if len(reflected_points_x) > 0:
            sizes = np.random.normal(self.size_mean,self.size_stdev,len(reflected_points_x))
            colors = np.linspace(0,1,len(reflected_points_x))
            ax.scatter(reflected_points_x,reflected_points_y,s=sizes,c=colors)
        if len(rotated_points_x) > 0:
            sizes = np.random.normal(self.size_mean,self.size_stdev,len(rotated_points_x))
            colors = np.linspace(0,1,len(rotated_points_x))
            ax.scatter(rotated_points_x,rotated_points_y,s=sizes,c=colors)
