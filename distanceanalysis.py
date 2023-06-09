import numpy as np
import statistics

#Calculates the distance between two points
def dist(A,B):
    return np.sqrt((A[0]-B[0])**2+(A[1]-B[1])**2+(A[2]-B[2])**2)

#Use this class if you want to calculate the average minimum distance between two selection of points from the coordinates.
class aveDist:
    def __init__(self,coordinates,selection1,selection2):

        numberofatoms = len(coordinates.coordinates[0])
        numberofrows = len(coordinates.coordinates)

        self.distance = []

        thecoords = []
        for i in range((numberofrows)):
            print("%d/%d" % (i,numberofrows))
            minimum_distances = []

            for m in selection1:
                min_dist = 500
                for k in selection2:
                    if k!=m:
                        distances = dist([coordinates.coordinates[i][m][1],coordinates.coordinates[i][m][2],coordinates.coordinates[i][m][3]],[coordinates.coordinates[i][k][1],coordinates.coordinates[i][k][2],coordinates.coordinates[i][k][3]])
                        if distances<min_dist:
                            min_dist = distances
                minimum_distances.append(min_dist)
            average_dist = 0
            for m in minimum_distances:
                average_dist += m
            self.distance.append(average_dist/len(minimum_distances))

            thecoords = []

#Use this class if you want to calculate the minimum distance between two selection of points
class minDist:
    def __init__(self,coordinates,selection1,selection2):

        numberofatoms = len(coordinates.coordinates[0])
        numberofrows = len(coordinates.coordinates)

        self.distance = []

        thecoords = []
        for i in range((numberofrows)):
            print("%d/%d" % (i,numberofrows))
            #coords = []
            #for j in range(numberofatoms):
            #    temp_coords = [coordinates.coordinates[i][j][1],coordinates.coordinates[i][j][2],coordinates.coordinates[i][j][3]]
            #    coords.append(temp_coords)

            #thecoords.append(coords)
            minimum_distances = []

            for m in selection1:
                min_dist = 500
                for k in selection2:
                    if k!=m:
                        distances = dist([coordinates.coordinates[i][m][1],coordinates.coordinates[i][m][2],coordinates.coordinates[i][m][3]],[coordinates.coordinates[i][k][1],coordinates.coordinates[i][k][2],coordinates.coordinates[i][k][3]])
                        #distances = dist(thecoords[0][k],thecoords[0][m])
                        if distances<min_dist:
                            min_dist = distances
                minimum_distances.append(min_dist)
            self.distance.append(min(minimum_distances))

            thecoords = []

#Use this class to plot the average or total minimum distance. You need the distances, specify where the time started, the time step used and the unit of time used.    
class plotaveDist:
    def __init__(self,distances,timestart,timestep,timeunit,Title=None,width=None,height=None,thickness=None,fontsize=None,padding=None):
        import matplotlib
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches
        from matplotlib.offsetbox import AnchoredText
        from matplotlib.pyplot import figure

        dist = distances.distance
        Time = []

        for i in range(len(dist)):
            Time.append(i*timestep+timestart)

        if width==None:
            width=1920
        if height==None:
            height=1440

        if thickness==None:
            thickness = 6
        if fontsize==None:
            fontsize=58
        if padding==None:
            padding=28

        width = int(width/80)
        height = int(height/80)

        fig = plt.figure()
        fig.set_size_inches(width,height)
        ax1 = fig.add_subplot(111)
        plt.plot(Time,dist,lw=thickness)

        plt.axvline(x=51,ls=':',lw=10,color="black")
        plt.axvline(x=0,ls=':',lw=10,color="black")
        plt.axvline(x=111,ls=':',lw=10,color="black")

        if Title!=None:
            plt.title(Title,fontsize=fontsize,pad=padding)

        plt.xlabel("Time (%s)" % timeunit,fontsize=fontsize,labelpad=padding)
        plt.ylabel("Distance (Å)",fontsize=fontsize,labelpad=padding)

        plt.xticks(fontsize=50)
        plt.yticks(fontsize=50)

        ax1.tick_params(width=3*thickness,length=10)
        for axis in ['top','bottom','left','right']:
            ax1.spines[axis].set_linewidth(int(1.7*thickness))
        ax1.tick_params(axis='both', which='major', pad=int(padding/1.33))
        
        fig.savefig('Dist.png', dpi=100, bbox_inches='tight')
        plt.show()
