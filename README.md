# cab-hailing-application
Cab Hailing API Application using FastAPI

## Problem Statement
The aim is  to develop a Cab Hailing API Application that assigns rides to customers based on their location and vehicle preference. The customer will input their present location as well as their preferred vehicle type. Given these, the closest vehicle of the preferred type must be assigned to them.  The customers must be charged a fixed base fare along with additional charges based on the distance traveled. The cab details, fare,  trip route, trip time and waiting time must be displayed to the customer.

## Requirements
1) The customer should be able request a ride by specifying pick up location, drop location and vehicle preference.
2) The system must allocate a cab of the preferred vehicle type nearest to the pick up location.
3) The fare must be calculated with fixed base fare along with additional charges based on distance travel.
4) The fare must also vary based on the vehicle type of the ride.
5) The customers must be allocated equitably between the cabs so that all drivers can take a fare share of trips per day.
6) The application must update the cab data by incrementing the trip count and changing the location of the allocated cab to drop location.
7) The cab details (vehicle type, driver name, license plate no.), fare, waiting time, trip time and shortest trip route must be displayed to the customer.
8) The application must be scalable to a change in the number of nodes (in the matrix of the graph to represent the map) or a change in the number of drivers.

## CONSTRAINTS
1) The number of drivers is fixed
2) The number of graph nodes is fixed.
3) Some graph nodes are inaccessible.

