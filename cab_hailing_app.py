#----------------------------IMPORTS--------------------------------
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
from collections import OrderedDict
from fastapi.staticfiles import StaticFiles

#-----------------------FUNCTION DEFINITIONS-----------------------
    
#FUNCTION TO FIND SHORTEST DISTANCE OF PICK UP POINT TO EVERY OTHER NODE, RETURNS DISTANCES, PATHS DICTIONARIES
def shortest_distance(locations, adj_matrix, pickup):
    
    #Numbering the locations for ease, we use nodes in djikstra and our output will be in nodes
    nodes=[i for i in range(len(locations))]
    source=locations.index(pickup)
    
    #Initiliaizing the variables
    distances={ node: float("inf") for node in nodes }
    paths={node:[] for node in nodes}
    
    distances[source]=0
    paths[source].append(source) 
    
    #Djikstra's algorithm
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
                
                #if new path from source is shorter than previous
                if distances[source] + adj_matrix[source][node]  < distances[node]:
                    #update distance
                    distances[node] = distances[source] + adj_matrix[source][node]
                    #update path
                    paths[node] = paths[source] +[node]
                
                #for finding closest adjacent node   
                if adj_matrix[source][node]<next_source_dist:
                    next_source_node=node
                    next_source_dist=adj_matrix[source][node]
        
        #to continue if reached a dead end or adjacent unvisited nodes not available
         for node in unvisited:
             if distances[node]<next_source_dist:
                next_source_node=node
                next_source_dist=distances[node]
                    
        return djikstra(adj_matrix,next_source_node,unvisited,distances,paths)
    
    #Calling djikstra
    distances, paths= djikstra(adj_matrix, source, nodes, distances,paths)
    
    #Converting the nodes back to locations in our djikstra output
    op_distances={locations[node]:distance for node,distance in distances.items()}
    op_paths={locations[node]:[locations[i] for i in path] for node,path in paths.items()}
    
    return op_distances, op_paths



#FUNCTION TO CALCULATE TRAVEL TIME, RETURNS TIME IN MINUTES 
def time(dist, speed):
    return dist*60/speed



#FUNCTION TO CALCULATE FARE, RETURNS FARE
def fare_calculation(rates, base_dist, base_charges, dist, vehicle):
    if dist<=base_dist:
        return base_charges[vehicle]
    else:
        return base_charges[vehicle] + (dist-base_dist)*rates[vehicle]



#FUNCTION TO ALLOCATE CAB GIVEN CAB DATA, RETURNS DRIVER NAME, PLATE NO., CAB LOCATION
def allocation(cabs, distances, vehicle, drop):
    #prints cab data in the terminal for reference
    print(cabs)
    
    #to sort the distances
    distances={value:key for key,value in distances.items()}  
    keys=sorted(distances.keys())
    distances=OrderedDict({distances[key]:key for key in keys})
    
    #filters cabs of preferred vehicle
    cabs = cabs[cabs["Vehicle"]== vehicle]
    
    ID=None
    
    #finds closest cab
    for location, distance in distances.items():
        if location in cabs["Location"].tolist():
            #filter cabs of closest location
            cabs = cabs[cabs["Location"] == location]
            ID = cabs[cabs["Trip Count"] == cabs["Trip Count"].min()].index[0]
            break
    
    #If cab found
    if ID!=None:
        return cabs.loc[ID, "Driver"],cabs.loc[ID, "Plate no."],cabs.loc[ID, "Location"]
    
       
    #If no cab found
    else:
        return None



#REMOVES INNACCESSIBLE NODES FROM LOCATIONS AND ADJ_MATRIX, RETURNS NEW LOCATIONS, NEW ADJ_MATRIX
def remove_na_location(locations, adj_matrix, na_locations):
    
    for location in na_locations:
        adj_matrix.pop(locations.index(location)) #removes from row in adj_matrix
        for row in adj_matrix:
            row.pop(location.index(location)) #removes from columns in adji_matrix
        locations.remove(location) #removes from locations
    
    return adj_matrix, locations




#TO GET COMPLETE FINAL RESULT, RETURNS DICTIONARY OF VALUES TO BE PASSED INTO HTML RESPONSE
def get_result(
    request: Request,
    pickup: str = Form(...),
    drop: str = Form(...),
    vehicle: str = Form(...),
    locations: list = None,
    adj_matrix: list = None,
    na_locations: list = None,
    base_charges: dict = None,
    rates: dict = None,
    base_dist: float = None,
    speed: float = None,
    cabs: pd.DataFrame = None
):

    try:
        #Gets distances and paths to every node from pickup
        distances, paths = shortest_distance(locations, adj_matrix, pickup)
    
        #Allocate cab
        driver, plate, cab_location = allocation(cabs, distances, vehicle, drop)

        #Calculate waiting time
        waiting=time(distances[cab_location],speed)
        
        #Calculate travel distance
        trip_dist= distances[drop]
        
        #Calculate trip time
        trip_time=time(trip_dist,speed)
        
        #Calculate trip_path
        trip_path=" --> ".join(paths[drop])

        #Calculate Fare
        fare=fare_calculation(rates, base_dist, base_charges, trip_dist, vehicle)
        
        return {"request": request, "driver": driver, "plate": plate,
             "cab_location": cab_location, "waiting": waiting,
             "trip_path": trip_path, "trip_distance": trip_dist,
             "trip_time": trip_time, "fare": fare,"inaccess":" ".join(na_locations)}
        
    #If no cab was allocated
    except:
         return None



#------------------------------MAIN--------------------------------


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/Users/sshwetha/Desktop/static", StaticFiles(directory="static"), name="static")

#------INITIALIZING VARIABLES--------
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

#remove inaccessible nodes
adj_matrix, locations= remove_na_location(locations, adj_matrix, na_locations)


#Fare variables 
base_charges = {"mini":40,"sedan":60,"suv":80}
rates= {"mini":20,"sedan":25,"suv":30}
base_dist=3 #km

speed= 40 #kmph

#Get Cab data
cabs=pd.read_excel("/Users/sshwetha/Downloads/cab_data.xlsx")
cabs["Location"] = cabs["Location"].apply(lambda x: x.upper())
cabs["Vehicle"] = cabs["Vehicle"].apply(lambda x: x.lower())

#---------------------------------


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("booking-form.html", {"request": request, "inaccess": " ".join(na_locations)})

@app.post("/cab-hailing/")
def show_result( request: Request, pickup: str = Form(...),  drop: str = Form(...), vehicle: str = Form(...) ):
    
    result =get_result(
        request,
        pickup.upper(),
        drop.upper(),
        vehicle,
        locations=locations,
        adj_matrix=adj_matrix,
        na_locations=na_locations,
        base_charges=base_charges,
        rates=rates,
        base_dist=base_dist,
        speed=speed,
        cabs=cabs
    )
    
    if result != None:
        return templates.TemplateResponse("booking-result.html", result)
    
    else:
        return "No cab found"


    


    
    
