import numpy as np

#Here we load in our coordinates (see read.py), the cell vectors [v_x,v_y,v_z] where v_x = [X_1, X_2, X_3], etc.
#fixed_list contains a list of all atoms that are supposed to be fixed. If none use an empty list []. Numbering starts with 1 up.
#POSCAR file will have fractional coordinates. I have found this is read in correctly with VASP.
class xyzConvert:
    def __init__(self,coordinates,v_x,v_y,v_z,fixed_list):
        Vectors = [v_x,v_y,v_z]
        
        #We create our POSCAR file
        f = open("POSCAR","w")
        print("XYZ to POSCAR",file=f)
        #Print our scaling factor of 1 by default
        print("%0.16f" % 1, file=f)
        #Print the vectors
        for i in Vectors:
            print("%0.16f" % float(i[0]),"%0.16f" % float(i[1]),"%0.16f" % float(i[2]),file=f)

        AtomList = []
        AtomNum = []
        for i in range(len(coordinates.coordinates[0])):
	      #We take the first atom and we have it take value of 1
            if i==0:
                AtomList.append(coordinates.coordinates[0][i][0])
                AtomNum.append(1)
            #If the next atom is different, assign a new atom and give it value of 1
            else:
                if coordinates.coordinates[0][i][0] != AtomList[len(AtomList)-1]:
                    AtomList.append(coordinates.coordinates[0][i][0])
                    AtomNum.append(1)
                #But if the next atom is the same, increment the number of atoms there are by 1
                else:
                    AtomNum[len(AtomNum)-1] += 1
         #Print each of the atom numbers
        for i in AtomList:
            print(i, end=" ",file=f)
        #Print each of the atoms (in order)
        print("",file=f)
        for i in AtomNum:
            print(i, end=" ",file=f)
        print("",file=f)
        print("Selective dynamics",file=f)
        print("Direct",file=f)


        #We print the fractional coordinates by getting the inverse of the cell vectors and multiplying it with the cartesian coordinates
        AtomTot = 0
        for i in AtomNum:
            AtomTot+=i

        for i in range(AtomTot):
            coords = coordinates.coordinates[0][i]
            position = [coords[1],coords[2],coords[3]]
            MatrixMult = np.matmul(position,np.linalg.inv(Vectors))
            if (i+1) in fixed_list:
                print('%0.16f' % MatrixMult[0], '%0.16f' % MatrixMult[1],'%0.16f' % MatrixMult[2],'F','F','F',file=f)  
            else:
                print('%0.16f' % MatrixMult[0], '%0.16f' % MatrixMult[1],'%0.16f' % MatrixMult[2],'T','T','T',file=f)  
        f.close()
