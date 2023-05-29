import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.offsetbox import AnchoredText
import numpy as np
import statistics

#Here the mean square displacement is calculated for the selected group of atoms. selections would be something like: selections = [range(144), range(144,152)], meaning that the self-diffusion coefficient is calculated
# for both range of atoms, individually.
#The below is calculated in terms of Angstrom and picosecond. So adjust your time step value to match this.
#Degrees of freedom is in how many dimensions does the atoms move. 
class msdValues:
    def __init__(self,coordinates,selections,skip,time_step,degrees_of_freedom):
        coordinates = coordinates.coordinates
        
        self.allMSD = []
        self.total_frames = []
        
        for i in range(len(selections)):
            selection = selections[i]
            total_MSD = []
            frames = []
            for j in range(1,len(coordinates),skip):
                new_j = j

                r_0 = []
                r_t = []
                
                for k in selection:
                    r_0.append([coordinates[0][k][1],coordinates[0][k][2],coordinates[0][k][3]])
                    r_t.append([coordinates[new_j][k][1],coordinates[new_j][k][2],coordinates[new_j][k][3]])
                
                r_0 = np.array(r_0)
                r_t = np.array(r_t)
                
                MSD = np.mean(np.abs(r_t-r_0)**2)/(2*degrees_of_freedom)
                time = new_j*time_step
                
                total_MSD.append(MSD)
                frames.append(frame)
            self.allMSD.append(total_MSD)
            self.total_frames = frames

#Here we calculate the self-diffusion coefficient using the MSD values from the first class. We can calculate the self-diffusion coefficient over a particular range of MSD vs Time values for each selection of atoms.
class selfDiff:
    def __init__(self,msdVals,start=None,end=None):
        
        if start==None:
            start=0
        allMSD = msdVals.allMSD
        allTime = msdVals.total_frames
        if end==None:
            end = len(allMSD[0])
        for i in range(len(allMSD)):
            slope = np.polyfit(allTime,allMSD[i],1)[0]
            print("Self-Diffusion Coefficient for Selection %i =" % i, slope)

#Here you can plot MSD vs time, so you can see if the plot is a straight line. Plot parameters are chosen by default. 
class MSDPlot:
    def __init__(self,msdVals):

        width=1920
        height=1440
        thickness = 6
        fontsize=58
        padding=28
        unit="ps"
        width = int(width/80)
        height = int(height/80)
        fig = plt.figure()
        fig.set_size_inches(width,height)
        ax1 = fig.add_subplot(111)
                  
        allMSD = msdVals.allMSD
        allTime = msdVals.total_frames
        for i in range(len(allMSD)):
            plt.plot(allTime,allMSD[i],lw=thickness)

            plt.xlabel("Time (ps)",fontsize=fontsize,labelpad=padding)
            plt.ylabel("MSD Value (Å)",fontsize=fontsize,labelpad=padding)

            plt.xticks(fontsize=50)
            plt.yticks(fontsize=50)

            ax1.tick_params(width=3*thickness,length=10)
            for axis in ['top','bottom','left','right']:
                ax1.spines[axis].set_linewidth(int(1.7*thickness))
            ax1.tick_params(axis='both', which='major', pad=int(padding/1.33))

            fig.savefig('MSD_%d.png' % i, dpi=100, bbox_inches='tight')
            plt.show()
