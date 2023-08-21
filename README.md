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
6) The cab details (vehicle type, driver name, license plate no.), fare, waiting time, trip time and shortest trip route must be displayed to the customer.
7) The application must be scalable to a change in the number of nodes (in the matrix of the graph to represent the map) or a change in the number of drivers.

## CONSTRAINTS
1) The number of drivers is fixed
2) The number of graph nodes is fixed.
3) Some graph nodes are inaccessible.

## Output

The requirements are entered in the form page.


![image](https://github.com/shwethanathan/cab-hailing-application/assets/126972707/6247923d-3b4f-4d4c-a648-21ef9779bb2a)



   
The closest available cab of the specified vehicle type is allocated.


![image](https://github.com/shwethanathan/cab-hailing-application/assets/126972707/2d7169c1-ded5-4f0b-b593-0a873a6fa3e4)




If the an innaccessible node is given as pick up or drop location, or if cab of preference is not available (for example: mini is not available in the cab data), the following output is displayed.


![image](https://github.com/shwethanathan/cab-hailing-application/assets/126972707/7d0f1b48-5d89-48f3-a963-cbaadbe2280e)





