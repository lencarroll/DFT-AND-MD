import numpy as np

#Calculate the distance between two points
def dist(A,B):
    return np.sqrt((A[1]-B[1])**2+(A[2]-B[2])**2+(A[3]-B[3])**2)

#Based on the two selection of points (for your coordinates), the number of neighbours in the distance shell r+dr is calculated. Here you specify the minimum and maximum values for the distance range, and the dr or shell thickness value
class getNums:
    def __init__(self,coordinates,selection1,selection2,minimum_distance,maximum_distance,dr):

        if '.' in str(dr):
            decimal = len(str(dr)) - str(dr).index('.') - 1
        else:
            decimal = dr

        Values_r = []
        self.Values_n = []
      
        for i in np.arange(minimum_distance, maximum_distance + dr, dr):
            Values_r.append(round(dr*round(i/dr),decimal))
            self.Values_n.append(0)
     
        for i in selection2:
            for j in selection1:
                if selection1==selection2:
                    if j!=i:
                        getDist = round(dr*round(dist(coordinates[j],coordinates[i])/dr),decimal)
                        try:
                            r_index = Values_r.index(getDist)
                            self.Values_n[r_index] += 0.5
                        except ValueError:
                            continue
                else:
                    if j!=i:
                        if i in selection1 and j in selection2:
                            getDist = round(dr*round(dist(coordinates[j],coordinates[i])/dr),decimal)
                            try:
                                r_index = Values_r.index(getDist)
                                self.Values_n[r_index] += 0.5
                            except ValueError:
                                continue
                        else:
                            getDist = round(dr*round(dist(coordinates[j],coordinates[i])/dr),decimal)
                            try:
                                r_index = Values_r.index(getDist)
                                self.Values_n[r_index] += 1
                            except ValueError:
                                continue

        self.non_Values = self.Values_n.copy()

        for i in range(len(self.Values_n)):
            self.Values_n[i] = self.Values_n[i]/((4/3)*np.pi*(Values_r[i]+dr)**3 - (4/3)*np.pi*(Values_r[i])**3)

#Here we prepare the dataset from the getNums values relative to the distance
class intRDF:
    def __init__(self,coordinates,selection1,selection2,minimum_distance,maximum_distance,dr):

        coordinates = coordinates.coordinates

        allRDF = []

        for i in range(len(coordinates)):
            RDF = getNums(coordinates[i],selection1,selection2,minimum_distance,maximum_distance,dr).non_Values
            allRDF.append(np.array(RDF))
        RDF = np.mean(allRDF,axis=0)

        allRDF = []

        Distance = []
        
        for i in np.arange(minimum_distance, maximum_distance + dr, dr):
            Distance.append(i)

        self.X = []
        self.Y = []

        for i in range(len(RDF)):
            self.X.append(Distance[i])
            self.Y.append(RDF[i])

#Use this if you want a normalized RDF, use this class. 
class normalRDF:
    def __init__(self,coordinates,selection1,selection2,minimum_distance,maximum_distance,dr):

        coordinates = coordinates.coordinates

        allRDF = []

        for i in range(len(coordinates)):
            RDF = getNums(coordinates[i],selection1,selection2,minimum_distance,maximum_distance,dr).Values_n
            allRDF.append(np.array(RDF))
        RDF = np.mean(allRDF,axis=0)

        allRDF = []

        Distance = []
        
        for i in np.arange(minimum_distance, maximum_distance + dr, dr):
            Distance.append(i)

        min_RDF = 0
        index_RDF = 0

        for i in np.arange(-1,-len(RDF),-1):
            if RDF[i] != 0.0:
                min_RDF = RDF[i]
                index_RDF = len(RDF)+i+1
                break
 
        self.X = []
        self.Y = []

        for i in range(index_RDF):
            self.X.append(Distance[i])
            self.Y.append(RDF[i]/min_RDF)

#If you don't want a normalized RDF, use this class. You will have to add the system's volume though.
class calcRDF:
    def __init__(self,coordinates,selection1,selection2,minimum_distance,maximum_distance,dr,volume):

        coordinates = coordinates.coordinates

        allRDF = []

        for i in range(len(coordinates)):
            if selection1 != selection2:
                RDF = np.array(getNums(coordinates[i],selection1,selection2,minimum_distance,maximum_distance,dr).Values_n)*volume/(len(selection1)*len(selection2))
            else:
                RDF = np.array(getNums(coordinates[i],selection1,selection2,minimum_distance,maximum_distance,dr).Values_n)*volume/(len(selection1)*(len(selection2)-1))
            allRDF.append(np.array(RDF))
        RDF = np.mean(allRDF,axis=0)

        allRDF = []

        Distance = []
        
        for i in np.arange(minimum_distance, maximum_distance + dr, dr):
            Distance.append(i)

        self.X = []
        self.Y = []

        for i in range(len(RDF)):
            self.X.append(Distance[i])
            self.Y.append(RDF[i])

#If you want to sum the values over a peak (important for intRDF), then use this class. Specify the minimum and maximum distance value for the peak, the RDF data it should calculate it from and the dr/thickness value you used.
class peakCalc:
    def __init__(self,rdf,peak1,peak2,dr):
        X = rdf.X
        Y = rdf.Y

        peak1 = dr*round(peak1/dr)
        peak2 = dr*round(peak2/dr)

        self.interactions = 0

        for i in range(len(X)):
            if X[i]>=peak1 and X[i]<=peak2:
                self.interactions += Y[i]
      
#Use this if you want to plot the data from intRDF.
class plotInt:
    def __init__(self,rdf,Title=None,width=None,height=None,thickness=None,fontsize=None,padding=None):
        import matplotlib
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches
        from matplotlib.offsetbox import AnchoredText
        from matplotlib.pyplot import figure

        X = rdf.X
        Y = rdf.Y

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
        plt.plot(X,Y,lw=thickness)
        if Title!=None:
            plt.title(Title,fontsize=fontsize,pad=padding)

        plt.xlabel("Distance (Å)",fontsize=fontsize,labelpad=padding)
        plt.ylabel("No. of O-O Interactions",fontsize=fontsize,labelpad=padding)

        plt.xticks(fontsize=50)
        plt.yticks(fontsize=50)

        ax1.tick_params(width=3*thickness,length=10)
        for axis in ['top','bottom','left','right']:
            ax1.spines[axis].set_linewidth(int(1.7*thickness))
        ax1.tick_params(axis='both', which='major', pad=int(padding/1.33))
        
        fig.savefig('RDF_Int.png', dpi=100, bbox_inches='tight')
        plt.show()

#This plots the RDF, whether it is normalized or not.
class plotRDF:
    def __init__(self,rdf,Title=None,width=None,height=None,thickness=None,fontsize=None,padding=None):
        import matplotlib
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches
        from matplotlib.offsetbox import AnchoredText
        from matplotlib.pyplot import figure

        X = rdf.X
        Y = rdf.Y

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
        plt.plot(X,Y,lw=thickness)
        if Title!=None:
            plt.title(Title,fontsize=fontsize,pad=padding)

        plt.xlabel("Distance (Å)",fontsize=fontsize,labelpad=padding)
        plt.ylabel("RDF",fontsize=fontsize,labelpad=padding)

        plt.xticks(fontsize=50)
        plt.yticks(fontsize=50)

        ax1.tick_params(width=3*thickness,length=10)
        for axis in ['top','bottom','left','right']:
            ax1.spines[axis].set_linewidth(int(1.7*thickness))
        ax1.tick_params(axis='both', which='major', pad=int(padding/1.33))
        
        fig.savefig('RDF_Plot.png', dpi=100, bbox_inches='tight')
        plt.show()
