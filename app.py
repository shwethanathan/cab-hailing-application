

 
#Function to get user input, returns pickup, drop, vehicle  
def user_input(locations):
    pickup=input("Enter pick up location: ")
    drop=input("Enter drop location: ")
    vehicle=input("Enter vehicle preference: ")
    return pickup, drop, vehicle

#Function to find shortest distance of pick up point to every other node, returns distances, paths
def shortest_distance(locations, adj_matrix, pickup):
    
    #Numbering the locations for ease, we use nodes in djikstra and our output will be in nodes
    nodes=[i for i in range(len(locations))]
    source=locations.index(pickup)
    
    #Setting the variables
    distances={ node: float("inf") for node in nodes }
    paths={node:[] for node in nodes}
    
    distances[source]=0
    paths[source].append(pickup) 
    
    
    def djikstra(adj_matrix, source, unvisited, distances, paths):
        
        #Removing source from unvisited
        if source in unvisited:
            unvisited.remove(source)
        
        
        #Base case
        if not unvisited :
            return distances,paths
            
            
        #For finding the next source node, i.e closest adjacent node
        next_source_dist=float("inf")
        next_source_node= None
        
        #Checks adjacent unvisited nodes
        for node in unvisited:
            if adj_matrix[source][node]!=0:
                
                
                #print("checking: ",node)
                #if new path from source is shorter than previous
                if distances[source] + adj_matrix[source][node]  < distances[node]:
                    #update distance
                    distances[node] = distances[source] + adj_matrix[source][node]
                    #update path
                    paths[node] = paths[source] +[node]
                
                #to find closest adjacent node   
                if adj_matrix[source][node]<next_source_dist:
                    next_source_node=node
                    next_source_dist=adj_matrix[source][node]
        
        #to trace back if reached and end 
        if next_source_node is None:
            next_source_node=paths[source][-2]
            
        return djikstra(adj_matrix,next_source_node,unvisited,distances,paths)
    
    distances, paths= djikstra(adj_matrix, source, nodes, distances,paths)
    
    #Converting the nodes back to locations in our output
    op_distances={locations[node]:distance for node,distance in distances.items()}
    op_paths={locations[node]:path for node,path in paths.items()}
    
    return op_distances, op_paths

#Function to calculate travel time, returns time in minutes 
def time(dist, speed):
    return dist/speed*60

#Function to calculate fare, returns fare
def fare(rates, base_dist, base_charges, dist, vehicle):
    if dist<=base_dist:
        return base_charges[vehicle]
    else:
        return base_charges[vehicle] + (dist-base_dist)*rates[vehicle]

#Function to allocate cab given cab data, returns Cab ID
def allocation(cabs, distances, vehicle, drop):
    
    #to sort the distances
    distances={value:key for key,value in distances.items()}  
    keys=sorted(distances.keys())
    distances=OrderedDict({distances[key]:key for key in keys})
    
    #filters cabs of preferred vehicle
    cabs = cabs[cabs["Vehicle"]== vehicle]

    ID=None
    
    #finds closest cab
    for node, distance in distances.items():
        if node in cabs["Location"]:
            cabs = cabs[cabs["Location"] == node]
            ID=cabs.index(cabs["Trip Count"]==max(cabs["Trip Count"]))
            break
    
    #If no cab found
    if ID==None:
        return None
    
    #If cab found
    if ID!=None:
        cab_location=cabs.loc[ID, "Location"]
        
        #Update cab info
        cabs.loc[ID, "Trip Count"]+=1
        cabs.loc[ID, "Location"]= drop
            
        return cabs.loc[ID, "Driver"],cabs.loc[ID, "Plate no."], cab_location

#Display allocation
def display(driver, plate, cab_location, waiting, trip_path, trip_distance, trip_time, fare):
    print("Driver: ", driver)
    print("Plate no: ",plate)
    print("Cab location: ",cab_location)
    print("Waiting Time: ", waiting)
    print("Trip route: ", trip_path[0], end="")
    for node in trip_path[1:]:
        print(" --> ", node, end="") 
    print("Trip distance: ", trip_distance)
    print("\nTrip time: ", trip_time)
    print("Fare: ", fare)
   
#Removes innaccessible nodes from locations and adj_matrix, return new locations, adj_matrix
def remove_na_location(locations, adj_matrix, na_locations):
    
    for location in na_locations:
        
        adj_matrix.pop(locations.index(location)) #removes row
        for row in adj_matrix:
            row.pop(location.index(location))
        locations.remove(location) #removes from locations
    
    return adj_matrix, locations
    
    


#main
import pandas as pd
from collections import OrderedDict

#----------------------VARIABLE DECLARATIONS------------------------

#Map variables
locations=["A","B","C","D","E","F","G","H","I","J","K"]
             #A  B  C  D  E  F  G  H  I  J  K
adj_matrix=[[ 0,10, 0, 0, 0, 5, 0, 0, 0,10, 0],                 
            [10, 0, 5, 7, 0, 0, 0, 0, 0, 0, 0],
            [ 0, 5, 0, 0, 0, 0, 6, 5, 0, 8, 0],
            [ 0, 7, 0, 0, 8, 0, 0, 0, 0, 4, 0],
            [ 0, 0, 0, 8, 0, 0, 0, 0, 4, 3, 0],
            [ 5, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0],
            [ 0, 0, 6, 0, 0, 9, 0, 9, 0, 0, 0],
            [ 0, 0, 5, 0, 0, 0, 9, 0, 0, 0, 0],
            [ 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 7],
            [ 0, 0, 8, 4, 3, 0, 0, 0, 0, 0, 0],
            [ 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0]]
na_locations=["A","D"]


#Fare variables 
base_charges = {"mini":40,"sedan":60,"suv":80}
rates= {"mini":20,"sedan":25,"suv":30}
base_dist=3 #km

speed= 60 #kmph

#Get Cab data
cabs=pd.read_excel("/Users/sshwetha/Downloads/cab_data (1).xlsx")
cabs["Location"] = cabs["Location"].apply(lambda x: x.lower())
#cabs["Vehicle"] = cabs["Vehicle"].apply(lambda x: x.lower())


#------------------------------------------------------------------

#Get user input
pickup, drop, vehicle= user_input(locations)

#remove inaccessible locations
adj_matrix, locations= remove_na_location(locations, adj_matrix, na_locations)
print("Locations removed")

#Gets distances and paths to every node from pickup
distances, paths = shortest_distance(locations, adj_matrix, pickup)
print("Distances found")

#Calculate travel distance
trip_dist= distances[drop]


#Calculate Fare
fare=fare(rates, base_dist, base_charges, trip_dist, vehicle)
print("Fare and travel distance calculated")

#Allocate Cab
if allocation(cabs, distances, vehicle, drop)!=None:
    driver, plate, cab_location = allocation(cabs, distances, vehicle, drop)
    print("Cab Allocated")


    #Calculate waiting time
    waiting=time(distances[cab_location],speed)
    
    
    #Calculate trip time
    trip_time=time(trip_dist,speed)
    
    #Calculate trip_path
    trip_path=paths[drop]
    
    display(driver, plate, cab_location, waiting, trip_path, trip_dist, trip_time, fare)

else:
    print("No Cab Found")
