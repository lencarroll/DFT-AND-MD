import numpy as np
import os
from os import path
import shutil
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.offsetbox import AnchoredText
import cv2
import sys
import pandas as pd

class twoDPlot:
    def __init__(self,coordinates,skip):

        # A directory "Images" is created in the working directory. This is where the frames are saved.
        directory = "Images"
        parent_dir = "."
        # If the "Images" folder exists, it is deleted and re-created
        if os.path.exists("./Images") == False:
            outpath = os.path.join(parent_dir,directory)
            os.mkdir(outpath)
        else:
            shutil.rmtree("./Images")
            outpath = os.path.join(parent_dir, directory)
            os.mkdir(outpath)

        #We setup the plot here
        fig,ax = plt.subplots()
        plt.rc('grid', linestyle=':', color='gray', linewidth=1)

        # Here we calculate the minimum and maximum X, Y values throughout all frames. This ensures that we construct the plot space correctly, so we don't have atoms moving off-screen
        min_X = sys.float_info.max
        min_Y = sys.float_info.max
        max_X = -1*sys.float_info.max
        max_Y = -1*sys.float_info.max

        for i in range(len(coordinates.coordinates)):
            for j in range(len(coordinates.coordinates[i])):
                coords_X = coordinates.coordinates[i][j][1]
                coords_Y = coordinates.coordinates[i][j][2]
                if coords_X < min_X:
                    min_X = coords_X
                if coords_Y < min_Y:
                    min_Y = coords_Y
                if coords_X > max_X:
                    max_X = coords_X
                if coords_Y > max_Y:
                    max_Y = coords_Y

        # Padding of 4 Angstrom is created around X and Y axes to ensure that atoms don't disappear off-screen
        min_X, min_Y = min_X - 4, min_X - 4
        max_X, max_Y = max_X + 4, max_Y + 4

        #The lists below are storing all the elements of the periodic table, their size for the plot and the color assigned to them. The color was randomly chosen.
        ptable = ['H','He','Li','Be','B','C','N','O','F','Ne','Na','Mg','Al','Si','P','S','Cl','Ar','K','Ca','Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn','Ga','Ge','As','Se','Br','Kr','Rb','Sr','Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','In','Sn','Sb','Te','I','Xe','Cs','Ba','La','Ce','Pr','Nd','Pm','Sm','Eu','Gd','Tb','Dy','Ho','Er','Tm','Yb','Lu','Hf','Ta','W','Re','Os','Ir','Pt','Au','Hg','Tl','Pb','Bi','Po','At','Rn','Fr','Ra','Ac','Th','Pa','U','Np','Pu','Am','Cm','Bk','Cf','Es','Fm','Md','No','Lr','Rf','Db','Sg','Bh','Hs','Mt','Ds','Rg','Cn','Nh','Fl','Mc','Lv','Ts','Og','Un']
        colorlist = ['#ADADAD', '#0578c6', '#838931', '#e82e6a', '#e58918', '#404040', '#004A7F', '#FF0000', '#c70102', '#bfdf85', '#013e99', '#98f7c6', '#ee383d', '#d5a4ca', '#b3c8be', '#960892', '#fb7a9d', '#26d389', '#5ebc33', '#89263e', '#10f9bd', '#bee760', '#205df5', '#b10bab', '#4163da', '#9ca948', '#31a9f3', '#b33d74', '#FF6A00', '#30ff79', '#b7d1b8', '#a092bc', '#8139f6', '#57ffd2', '#21685d', '#9eb570', '#4ccf48', '#41be51', '#2f1861', '#c90799', '#508a1d', '#7c1464', '#48a64b', '#31fa8e', '#9e5fbd', '#c77094', '#7f60b7', '#f66f74', '#715856', '#d221e4', '#de99e2', '#29c2a9', '#6069c2', '#0cc49d', '#642786', '#e405b6', '#560dd3', '#7006d7', '#f04d9d', '#5c1b63', '#cb920f', '#61521a', '#e6da8a', '#da25bc', '#bd4b95', '#94a8ec', '#f054a6', '#bc7424', '#b6582d', '#494d80', '#239f1f', '#3d738d', '#cf9c04', '#77b7c7', '#e6a211', '#c6f2cb', '#246d90', '#054298', '#FFD800', '#2e0e29', '#b03d4b', '#612d01', '#347408', '#65d366', '#057faf', '#69cf90', '#587960', '#24d8c0', '#ac6a12', '#58226c', '#ac851a', '#97adf3', '#da8f0c', '#726883', '#bb7b8b', '#40150a', '#a6c2b6', '#790946', '#38232e', '#41e8c0', '#41d468', '#4edd68', '#3f2fb9', '#3082a8', '#3cbd53', '#4b9395', '#29bdf3', '#d40c42', '#2c219c', '#6de5ef', '#d7cd83', '#6ef13a', '#e03729', '#677b60', '#632e7e', '#9a265a', '#741b0c', '#261741','#000000']
        radiuslist = [100, 60, 580, 420, 340, 280, 260, 240, 200, 160, 720, 600, 500, 440, 400, 400, 400, 284, 880, 720, 640, 560, 540, 560, 560, 560, 540, 540, 540, 540, 520, 500, 460, 460, 460, 440, 940, 800, 720, 620, 580, 580, 540, 520, 540, 560, 640, 620, 620, 580, 580, 560, 560, 540, 1040, 860, 780, 740, 740, 740, 740, 740, 780, 720, 700, 700, 700, 700, 700, 700, 700, 620, 580, 540, 540, 520, 540, 540, 540, 600, 760, 720, 640, 760, 800, 840, 1120, 860, 780, 720, 720, 700, 700, 700, 700, 700, 700, 680, 680, 680, 660, 660, 660, 660, 660, 660, 660, 660, 660, 660, 660, 660, 660, 660, 660, 660, 660, 660]

        #Function to get the color of the atom
        def atom_color(X):
            return colorlist[ptable.index(X)]

        #Function to get the color and label for the atom plot legend
        def atom_labels(X):
           label = X
           color = atom_color(X)
           return "mpatches.Patch(color='%s', label='%s')" % (color,label)

        #Function to determine the size of the atom in the plot
        def atom_size(X):
            return radiuslist[ptable.index(X)]

        #Function used to make the plot of the frames
        def f(j):
            ax.clear() #clears the plots as to make sure multiple plots aren't made on the same file

            headers = ["Atom", "X", "Y", "Z"]
            df = pd.DataFrame(coordinates.coordinates[j], columns=headers)
            df = df.sort_values(by ='Z', ascending = True) #The dataframe is sorted as to have the atom with the minimum z value at the top of the dataframe, while the one with the maximim z value at the bottom
            df = df.reset_index(drop=True) #The index of the dataframe is once again reset, without doing this, the plot can look funky

            col = []
            
            for i in df.index:
                col.append(atom_color(df['Atom'].iloc[i]))              
            x, y, z = df['X'], df['Y'], df['Z']
            size = []
            min_Z = min(df['Z'])
            # The Z axis values are adjusted as we need to use these adjusted values for determining the relative size of the atom
            z_alt = z - min_Z

            #Here the size of the atoms in the plot are put together
            for i in df.index:
                size.append(atom_size(df['Atom'].iloc[i])+2*z_alt.iloc[i]*np.tan(np.arctan((atom_size(df['Atom'].iloc[i])/0.4-atom_size(df['Atom'].iloc[i]))/(2*10))))
            #Here the plot is made, with a black border around the points
            for i in range(len(col)):
                ax.scatter(x.iloc[i],y.iloc[i],c=col[i],s=size[i]*int(((19.6/6.4))**2),edgecolors='black',marker='o',lw=2)
            #Creates 4 A space all around the outer atoms as to not have it disappear when atoms move out of frame
            ax.set_ylim(min_Y,max_Y)
            ax.set_xlim(min_X,max_X)
            atom_types = []
            #Here the labels of atoms are put together
            for i in df.index:
                if df['Atom'].iloc[i] not in atom_types:
                    atom_types.append(df['Atom'].iloc[i])
            plt.legend(handles=[eval(atom_labels(i)) for i in atom_types],bbox_to_anchor=(1,1), loc="upper left",fontsize=20)
            plt.grid(True)
            plt.xlabel("X (Å)",fontsize=58,labelpad=28)
            plt.ylabel("Y (Å)",fontsize=58,labelpad=28)
            plt.yticks(fontsize=50)
            plt.xticks(fontsize=50)
            plt.gcf().set_size_inches(19.6, 14.4)
            ax.tick_params(width=18,length=10)
            for axis in ['top','bottom','left','right']:
                ax.spines[axis].set_linewidth(int(1.7*6))
            ax.tick_params(axis='both', which='major', pad=int(28/1.33))
            #Minimum and maxmum Z values are plotted as to keep track how the Z component is changing
            anchored_text = AnchoredText("min_Z = %0.5f\nmax_Z = %0.5f" % (min_Z,max(df['Z'])), loc="lower left")
            ax.add_artist(anchored_text)
            plt.draw()
            fig.savefig(path.join(outpath,"frame_{00}.jpg".format(j)),bbox_inches ="tight",dpi=100)

        for j in range(0,len(coordinates.coordinates),skip):
            f(j)

class makeVideo:
    #Here we can take the images from the "Images" folder and make a video out of it. It is saved as video.avi by default, and 24 fps.
    def __init__(self, coordinates, skip, fps):
        image_folder = 'Images'
        video_name = 'video.avi'
        images = []
        for j in range(0,len(coordinates.coordinates),skip):
            images.append('frame_%d.jpg' % j)
        frame = cv2.imread(os.path.join(image_folder, images[0]))
        height, width, layers = frame.shape
        video = cv2.VideoWriter(video_name, 0, fps, (width,height))
        for image in images:
            video.write(cv2.imread(os.path.join(image_folder, image)))
        cv2.destroyAllWindows()
        video.release()
