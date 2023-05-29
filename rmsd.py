import numpy as np

#RMSD from a set of coordinates based on a selection of atoms is calculated here. You can specify where to start the RMSD, how mnany frames to be skipped. You can also decide if you want the RMSD data saved.
class rmsd:
    def __init__(self,coordinates,selection,start=None,step=None,save='Y',num=None):

        coordinates = coordinates.coordinates
   
        RMSD = []
        Time = []
        self.rmsd = []

        if start==None:
            start = 0

        if step == None:
            step = 1

        if num==None:
            num = 1

        if save=='Y':
            open_file = open("RDF_%d.csv"%num,"w")

        for i in range(len(coordinates)):  

            midRMSD = [0,0,0]
            for j in selection:
                midRMSD[0] += (coordinates[i][j][1] - coordinates[0][j][1])**2
                midRMSD[1] += (coordinates[i][j][2] - coordinates[0][j][2])**2
                midRMSD[2] += (coordinates[i][j][3] - coordinates[0][j][3])**2
            midRMSD = np.sqrt(np.sum(np.array(midRMSD))/len(selection))

            if save=='Y':
                print(i*step+start,midRMSD,file=open_file)

            RMSD.append(midRMSD)
            Time.append(i*step + start)
        if save=='Y':
            open_file.close()

        self.rmsd = [Time,RMSD]

#Here we plot the RMSD data. You can import multiple RMSD values as e.g. value=[RMSD1,RMSD2,RMSD]. Each of these RMSD datasets are analyzed and plotted together.
#You can specify the time unit used for the plot, labels used in the plot, width of the plot, etc. Usually I keep the default
class plotRMSD:
    def __init__(self,value,labels=None,unit=None,location=None,width=None,height=None,thickness=None,fontsize=None,padding=None):
        import matplotlib
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches
        from matplotlib.offsetbox import AnchoredText
        from matplotlib.pyplot import figure

        X = []
        Y = []

        for i in range(len(value)):
            X.append((value[i].rmsd)[0])
            Y.append((value[i].rmsd)[1])

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

        if unit==None:
            unit="ps"

        width = int(width/80)
        height = int(height/80)

        fig = plt.figure()
        fig.set_size_inches(width,height)
        ax1 = fig.add_subplot(111)
        if labels==None:
            for i in range(len(X)):
                plt.plot(X[i],Y[i],lw=thickness,label="%d"%(i+1))
        else:
            for i in range(len(X)):
                plt.plot(X[i],Y[i],lw=thickness,label=labels[i])

        #Uncomment this if you want to plot the y-values only along a certain range 
        #plt.ylim([A, B])

        #Uncomment this if you want to plot a vertical line along the plotts
        #plt.axvline(x=X,ls=':',lw=10,color="black")

        plt.xlabel("Time (%s)"%unit,fontsize=fontsize,labelpad=padding)
        plt.ylabel("RMSD (Å)",fontsize=fontsize,labelpad=padding)

        plt.xticks(fontsize=50)
        plt.yticks(fontsize=50)

        ax1.tick_params(width=3*thickness,length=10)
        for axis in ['top','bottom','left','right']:
            ax1.spines[axis].set_linewidth(int(1.7*thickness))
        ax1.tick_params(axis='both', which='major', pad=int(padding/1.33))

        if location==None:
            plt.legend(loc='best',fontsize=int(fontsize/2))
        ax1.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), fancybox=True, shadow=True, ncol=5)
        
        fig.savefig('RMSD.png', dpi=100, bbox_inches='tight')
        plt.show()
