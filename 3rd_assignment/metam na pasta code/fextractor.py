import os
import argparse

#CSF1819: 
    #Here you should add more features to the feature vector (features=[]) representing a cell trace

    #Function extract receives as input two sequences:
    #    times: timestamp of each cell
    #    sizes: direction of each cell (-1 / +1)

    #As of now, the only feature being used to distinguish between page loads is the total
    # amount of cells in each cell sequence and is given by len(times).

    # Shall some feature be missing due to impossibility of its calculation, 
    #please replace its value with "X". It will be replaced later.

def extract(times, sizes):
    features = []

    #Average size of cells
    features.append(512/len(times))
    #Tempo demorado
    features.append(times[-1])
    #Numero de outgoing cells
    features.append(sizes.count(1))
    #Numero de incoming cells
    features.append(sizes.count(-1))
    
    #ORDERING
    #for j in range(0,len(sizes)):
    #    if sizes[j] == 1:
    #        aux = []
    #        counterCells = j
    #        counterIncCells = 0
    #        for i in range(j-1,-1,-1):
    #            if(sizes[i] == -1):
    #                counterIncCells += 1
    #            if(sizes[i] == 1):
    #                break
    #        features.append(counterCells)
    #        features.append(counterIncCells)
    
    #CONCENTRATION


    ####BURSTS####
    outgoingBursts = getBurstSizes(sizes,1)
    incomingBursts = getBurstSizes(sizes,-1)
    #Numero de Bursts
    features.append(len(outgoingBursts))
    features.append(len(incomingBursts))
    #Numero de Non-Bursts
    #features.append(len(sizes)-len(outgoingBursts))
    #features.append(len(sizes)-len(incomingBursts))
    #tamanho do maior burst
    if(len(outgoingBursts) == 0):
        features.append('X')
    else:
        features.append(max(outgoingBursts))
    if(len(incomingBursts) == 0):
        features.append('X')
    else:
        features.append(max(incomingBursts))
    #tamanho do menor burst
    if(len(outgoingBursts) == 0):
        features.append('X')
    else:
        features.append(min(outgoingBursts))
    if(len(incomingBursts) == 0):
        features.append('X')
    else:
        features.append(min(incomingBursts))
    #media de tamanho dos bursts
    if(len(outgoingBursts) == 0):
        features.append('X')
    else:
        features.append((sum(outgoingBursts)+0.0)/len(outgoingBursts))
    if(len(incomingBursts) == 0):
        features.append('X')
    else:
        features.append((sum(incomingBursts)+0.0)/len(incomingBursts))
    
    return features

def getBurstSizes(lista, direction):
    counter=1
    aux=[]
    for i in range(1,len(lista)):
        if lista[i-1] == lista[i] == direction:
            counter += 1
        else:
	    if counter >= 2:
                aux.append(counter)
            counter = 1
    if lista[-1] == lista[-2] == direction:
        aux.append(counter)
    return aux


def impute_missing(x):
        """Accepts a list of features containing 'X' in
        place of missing values. Consistently with the code
        by Cai et al, replaces 'X' with -1.
        """
        for i in range(len(x)):
            if x[i] == 'X':
                x[i] = -1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract feature vectors')
    parser.add_argument('--traces', type=str, help='Original traces directory.',
                        required=True)
    parser.add_argument('--out', type=str, help='Output directory for features.',
                        required=True)
    args = parser.parse_args()

    if not os.path.isdir(args.out):
        os.makedirs(args.out)

    #this takes quite a while
    print "Gathering features for monitored sites..."
    for site in range(0, 100):
        print site
        for instance in range(0, 90):
            fname = str(site) + "-" + str(instance)
            #Set up times, sizes
            f = open(args.traces + "/" + fname, "r")
            times = []
            sizes = []
            for x in f:
                x = x.split("\t")
                times.append(float(x[0]))
                sizes.append(int(x[1]))
            f.close()
    
            #Extract features. All features are non-negative numbers or X. 
            features = extract(times, sizes)

            #Replace X by -1 (Cai et al.)
            impute_missing(features)

            fout = open(args.out + "/" + fname + ".features", "w")
            for x in features[:-1]:
                fout.write(repr(x) + ",")
            fout.write(repr(features[-1]))
            fout.close()

    print "Finished gathering features for monitored sites."

    print "Gathering features for non-monitored sites..."
    #open world
    for site in range(0, 9000):
        print site
        fname = str(site)
        #Set up times, sizes
        f = open(args.traces + "/" + fname, "r")
        times = []
        sizes = []
        for x in f:
            x = x.split("\t")
            times.append(float(x[0]))
            sizes.append(int(x[1]))
        f.close()
    
        #Extract features. All features are non-negative numbers or X. 
        features = extract(times, sizes)

        #Replace X by -1 (Cai et al.)
        impute_missing(features)

        fout = open(args.out + "/" + fname + ".features", "w")
        for x in features[:-1]:
            fout.write(repr(x) + ",")
        fout.write(repr(features[-1]))
        fout.close()

    print "Finished gathering features for non-monitored sites."
    f.close()
