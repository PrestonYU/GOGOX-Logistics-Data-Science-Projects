#!/usr/bin/env python
# coding: utf-8

# In[1]:


#########################################################################
# Created by Preston Yu (TW Team)
# 2021-01-15
#########################################################################
# First 1 : Import Google Sheet to Jupyter Notebook
from __future__ import print_function
import gspread
from df2gspread import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import time
import numpy as np
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver.pywrapcp import RoutingIndexManager, RoutingModel

    # The scope is always look like this so we did not need to change anything
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    # Name of our Service Account Key
    # https://console.developers.xxxxxxxxxxx
google_key_file = 'xxxxxxxxx'
credentials = ServiceAccountCredentials.from_json_keyfile_name(google_key_file, scope)
gc = gspread.authorize(credentials)

    # Opening the worksheet by using Worksheet ID
workbook = gc.open_by_key('xxxxxxxxx')

# Selecting which sheet to pulling the data
sheet = workbook.worksheet('_raw4')

# Pulling the data and transform it to the data frame
values = sheet.get_all_values()
df = pd.DataFrame(values[:], columns = values[0])
df = df[1:]
df = df.reset_index(drop = True)


# In[2]:


import warnings
warnings.filterwarnings("ignore")

dff = df.iloc[:,0:11]

dff['time_matrix'] = ''
for i in range(0,len(dff)):
    time_matrix = []
    for j in range(0,len(dff)):
        time_matrix.append(int(round(((pow(pow(float(dff['Latitude'][i])-float(dff['Latitude'][j]),2) + pow(float(dff['Longitude'][i])-float(dff['Longitude'][j]),2),0.5)*111)/20)*60)))
    dff['time_matrix'][i] = time_matrix

dff['distance_matrix'] = ''
for i in range(0,len(dff)):
    distance_matrix = []
    for j in range(0,len(dff)):
        distance_matrix.append(int(round((pow(pow(float(dff['Latitude'][i])-float(dff['Latitude'][j]),2) + pow(float(dff['Longitude'][i])-float(dff['Longitude'][j]),2),0.5)*111000))))
    dff['distance_matrix'][i] = distance_matrix

for k in range(0,len(dff)):
    dff['time_windows'][k] = eval(dff['time_windows'][k])

dfff = []
for l in range(0,len(dff['pickups_deliveries'][(dff['pickups_deliveries'].notnull() == True) & (dff['pickups_deliveries'] != '')].reset_index(drop=True))):
    dfff.append(eval(dff['pickups_deliveries'][(dff['pickups_deliveries'].notnull() == True) & (dff['pickups_deliveries'] != '')].reset_index(drop=True)[l]))


# In[3]:


def create_data_model():
    """Stores the data for the problem."""
    data = {}
    data['time_matrix'] = pd.Series.tolist(dff['time_matrix'])
    
    data['time_windows'] = pd.Series.tolist(dff['time_windows'])
    
    data['distance_matrix'] = pd.Series.tolist(dff['distance_matrix'])
    
    data['pickups_deliveries'] = dfff
    
    data['num_vehicles'] = int(workbook.worksheet('Result').acell('D1').value)
    data['depot'] = 0
    return data


# In[ ]:


from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

########################################################
## Vehicles Routing Problem with Time Windows (VRPTW) ##
########################################################

def print_solution1(data, manager, routing, solution):
    """Prints solution on console."""
    time_dimension = routing.GetDimensionOrDie('Time')
    total_time = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        while not routing.IsEnd(index):
            time_var = time_dimension.CumulVar(index)
            plan_output += '{0} Time({1},{2}) -> '.format(
                manager.IndexToNode(index), solution.Min(time_var),
                solution.Max(time_var))
            index = solution.Value(routing.NextVar(index))
        time_var = time_dimension.CumulVar(index)
        plan_output += '{0} Time({1},{2})\n'.format(manager.IndexToNode(index),
                                                    solution.Min(time_var),
                                                    solution.Max(time_var))
        plan_output += 'Time of the route: {}min\n'.format(
            solution.Min(time_var))
        print(plan_output)
        total_time += solution.Min(time_var)
    print('Total time of all routes: {}min'.format(total_time))


def main1():
    """Solve the VRP with time windows."""
    # Instantiate the data problem.
    data1 = create_data_model()

    # Create the routing index manager.
    manager1 = pywrapcp.RoutingIndexManager(len(data1['time_matrix']),
                                           data1['num_vehicles'], data1['depot'])

    # Create Routing Model.
    routing1 = pywrapcp.RoutingModel(manager1)

    # Create and register a transit callback.
    def time_callback1(from_index, to_index):
        """Returns the travel time between the two nodes."""
        # Convert from routing variable Index to time matrix NodeIndex.
        from_node = manager1.IndexToNode(np.int64(from_index))
        to_node = manager1.IndexToNode(np.int64(to_index))
        return data1['time_matrix'][from_node][to_node]

    
    transit_callback_index1 = routing1.RegisterTransitCallback(time_callback1)

    # Define cost of each arc.
    routing1.SetArcCostEvaluatorOfAllVehicles(transit_callback_index1)

    # Add Time Windows constraint.
    time = 'Time'
    routing1.AddDimension(
        transit_callback_index1,
        10000000000000000,  # allow waiting time
        10000000000000000,  # maximum time per vehicle
        False,  # Don't force start cumul to zero.
        time)
    time_dimension = routing1.GetDimensionOrDie(time)
    # Add time window constraints for each location except depot.
    for location_idx, time_window in enumerate(data1['time_windows']):
        if location_idx == 0:
            continue
        index = manager1.NodeToIndex(location_idx)
        time_dimension.CumulVar(index).SetRange(time_window[0],time_window[0]+time_window[1])
    # Add time window constraints for each vehicle start node.
    for vehicle_id in range(data1['num_vehicles']):
        index = routing1.Start(vehicle_id)
        time_dimension.CumulVar(index).SetRange(data1['time_windows'][0][0]
                                              ,data1['time_windows'][0][1])

    # Instantiate route start and end times to produce feasible times.
    for i in range(data1['num_vehicles']):
        routing1.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing1.Start(i)))
        routing1.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing1.End(i)))

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.LOCAL_CHEAPEST_ARC)

    # Solve the problem.
    solution1 = routing1.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution1:
        print_solution1(data1, manager1, routing1, solution1)

        
##########################################
## Simple Pickup Delivery Problem (PDP) ##
##########################################

def print_solution2(data, manager, routing, solution):
    """Prints solution on console."""
    total_distance = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += ' {} -> '.format(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += '{}\n'.format(manager.IndexToNode(index))
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        print(plan_output)
        total_distance += route_distance
    print('Total Distance of all routes: {}m'.format(total_distance))


def main2():
    """Entry point of the program."""
    # Instantiate the data problem.
    data2 = create_data_model()

    # Create the routing index manager.
    manager2 = pywrapcp.RoutingIndexManager(len(data2['distance_matrix']),
                                           data2['num_vehicles'], data2['depot'])

    # Create Routing Model.
    routing2 = pywrapcp.RoutingModel(manager2)


    # Define cost of each arc.
    def distance_callback2(from_index, to_index):
        """Returns the manhattan distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager2.IndexToNode(np.int64(from_index))
        to_node = manager2.IndexToNode(np.int64(to_index))
        return data2['distance_matrix'][from_node][to_node]

    transit_callback_index2 = routing2.RegisterTransitCallback(distance_callback2)
    routing2.SetArcCostEvaluatorOfAllVehicles(transit_callback_index2)

    # Add Distance constraint.
    dimension_name = 'Distance'
    routing2.AddDimension(
        transit_callback_index2,
        10000000000000000,  # no slack
        10000000000000000,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name)
    distance_dimension = routing2.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # Define Transportation Requests.
    for request in data2['pickups_deliveries']:
        pickup_index = manager2.NodeToIndex(request[0])
        delivery_index = manager2.NodeToIndex(request[1])
        routing2.AddPickupAndDelivery(pickup_index, delivery_index)
        routing2.solver().Add(
            routing2.VehicleVar(pickup_index) == routing2.VehicleVar(
                delivery_index))
        routing2.solver().Add(
            distance_dimension.CumulVar(pickup_index) <=
            distance_dimension.CumulVar(delivery_index))

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.time_limit.seconds = 30
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION)

    # Solve the problem.
    solution2 = routing2.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution2:
        print_solution2(data2, manager2, routing2, solution2)

        
###########################################################
## Simple Pickup Delivery Problem - FIFO Rule (PDP-FIFO) ##
###########################################################

#https://github.com/google/or-tools/blob/stable/ortools/constraint_solver/samples/vrp_pickup_delivery_fifo.py

def print_solution3(data, manager, routing, assignment):
    """Prints assignment on console."""
    total_distance = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += ' {} -> '.format(manager.IndexToNode(index))
            previous_index = index
            index = assignment.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += '{}\n'.format(manager.IndexToNode(index))
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        print(plan_output)
        total_distance += route_distance
    print('Total Distance of all routes: {}m'.format(total_distance))



def main3():
    """Entry point of the program."""
    # Instantiate the data problem.
    data3 = create_data_model()


    # Create the routing index manager.
    manager3 = pywrapcp.RoutingIndexManager(len(data3['distance_matrix']),
                                           data3['num_vehicles'], data3['depot'])

    # Create Routing Model.
    routing3 = pywrapcp.RoutingModel(manager3)


    # Define cost of each arc.
    def distance_callback3(from_index, to_index):
        """Returns the manhattan distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager3.IndexToNode(np.int64(from_index))
        to_node = manager3.IndexToNode(np.int64(to_index))
        return data3['distance_matrix'][from_node][to_node]

    transit_callback_index3 = routing3.RegisterTransitCallback(distance_callback3)
    routing3.SetArcCostEvaluatorOfAllVehicles(transit_callback_index3)

    # Add Distance constraint.
    dimension_name = 'Distance'
    routing3.AddDimension(
        transit_callback_index3,
        10000000000000000,  # no slack
        10000000000000000,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name)
    distance_dimension = routing3.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)
    
    # Define Transportation Requests.
    for request in data3['pickups_deliveries']:
        pickup_index = manager3.NodeToIndex(request[0])
        delivery_index = manager3.NodeToIndex(request[1])
        routing3.AddPickupAndDelivery(pickup_index, delivery_index)
        routing3.solver().Add(
            routing3.VehicleVar(pickup_index) == routing3.VehicleVar(
                delivery_index))
        routing3.solver().Add(
            distance_dimension.CumulVar(pickup_index) <=
            distance_dimension.CumulVar(delivery_index))
    routing3.SetPickupAndDeliveryPolicyOfAllVehicles(
        pywrapcp.RoutingModel.PICKUP_AND_DELIVERY_FIFO)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION)

    # Solve the problem.
    assignment3 = routing3.SolveWithParameters(search_parameters)

    # Print solution on console.
    if assignment3:
        print_solution3(data3, manager3, routing3, assignment3)

        
##############################################################
## Pickups and Deliveries with Time Windows Problem (PDPTW) ##
##############################################################

#https://github.com/google/or-tools/issues/1587

# todo replace with time one
def print_solution4(data, manager, routing, assignment):
    """Prints assignment on console."""
    time_dimension = routing.GetDimensionOrDie('Time')
    total_time = 0
    for vehicle_id in range(data['num_vehicles']):

        # Model inspection. Returns the variable index of the starting node of a vehicle route.
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        while not routing.IsEnd(index):
            time_var = time_dimension.CumulVar(index)
            plan_output += '{0} Time({1},{2}) -> '.format(
                manager.IndexToNode(index), assignment.Min(time_var),
                assignment.Max(time_var))
            index = assignment.Value(routing.NextVar(index))

        # handles the end location
        time_var = time_dimension.CumulVar(index)
        plan_output += '{0} Time({1},{2})\n'.format(
            manager.IndexToNode(index), assignment.Min(time_var),
            assignment.Max(time_var))
        plan_output += 'Time of the route: {}min\n'.format(
            assignment.Min(time_var))
        print(plan_output)
        total_time += assignment.Min(time_var)
    print('Total time of all routes: {}min'.format(total_time))


def main4():
    """Solve the VRP with time windows."""
    # Instantiate the data problem.
    data4 = create_data_model()

    # Create the routing index manager.
    manager4 = pywrapcp.RoutingIndexManager(
        len(data4['time_matrix']), data4['num_vehicles'], data4['depot'])

    # Create Routing Model.
    routing4 = pywrapcp.RoutingModel(manager4)

    def time_callback4(from_index, to_index):
        """Returns the travel time between the two nodes."""
        # Convert from routing variable Index to time matrix NodeIndex.
        from_node = manager4.IndexToNode(np.int64(from_index))
        to_node = manager4.IndexToNode(np.int64(to_index))
        return data4['time_matrix'][from_node][to_node]

    transit_callback_index4 = routing4.RegisterTransitCallback(time_callback4)
    routing4.SetArcCostEvaluatorOfAllVehicles(transit_callback_index4)

    # The code creates a dimension for the travel time of the vehicles, similar to the dimensions
    # for travel distance or demands in previous examples. Dimensions keep track of quantities that
    # accumulate over a vehicle's route. In the code above, time_dimension.CumulVar(index) is the
    # cumulative travel time when a vehicle arrives at the location with the given index.
    time = 'Time'
    routing4.AddDimension(
        transit_callback_index4,
        10000000000000000,  # allow waiting time
        10000000000000000,  # maximum time per vehicle
        False,  # Don't force start cumul to zero.
        time)
    # Returns a dimension from its name. Dies if the dimension does not exist.
    time_dimension = routing4.GetDimensionOrDie(time)

    # Add time window constraints for each location except depot.
    for location_idx, time_window in enumerate(data4['time_windows']):
        if location_idx == 0:  # idx 0 and 1 are the driver and customer
            continue

        # NodeToIndex returns -1 for end nodes
        index = manager4.NodeToIndex(location_idx)
        time_dimension.CumulVar(index).SetRange(time_window[0], time_window[0]+time_window[1])

    # Not sure if I need this? Removed for now
    # Add time window constraints for each vehicle start node.
    for vehicle_id in range(data4['num_vehicles']):
    # Model inspection. Returns the variable index of the starting node of a vehicle route.
         start_index = routing4.Start(vehicle_id)
         time_dimension.CumulVar(start_index).SetRange(data4['time_windows'][0][0],
                                                       data4['time_windows'][0][1])

    for i in range(data4['num_vehicles']):
        routing4.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing4.Start(i)))
        routing4.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing4.End(i)))

    # Define Transportation Requests.
    for request in data4['pickups_deliveries']:
        pickup_index = manager4.NodeToIndex(request[0])
        delivery_index = manager4.NodeToIndex(request[1])
        routing4.AddPickupAndDelivery(pickup_index, delivery_index)
        routing4.solver().Add(
            routing4.VehicleVar(pickup_index) == routing4.VehicleVar(
                delivery_index))
        routing4.solver().Add(
            time_dimension.CumulVar(pickup_index) <=
            time_dimension.CumulVar(delivery_index))

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.time_limit.seconds = 30
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    assignment4 = routing4.SolveWithParameters(search_parameters)

    if assignment4:
        print_solution4(data4, manager4, routing4, assignment4)
        
        
        

""" Initiate """

if __name__ == '__main__':
    if workbook.worksheet('Result').acell('B1').value == 'VRPTW':
        main1()  
    elif workbook.worksheet('Result').acell('B1').value == 'PDP':
        main2()
    elif workbook.worksheet('Result').acell('B1').value == 'PDP FIFO':
        main3() 
    elif workbook.worksheet('Result').acell('B1').value == 'PDP TW':
        main4()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




