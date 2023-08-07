
# NAME: CHELLARAPU PRIYANKA
# Roll Number: CS20B022
# Course: CS3205 Jan. 2023 semester
# Lab number: 2
# Date of submission: 05 April 23
# I confirm that the source file is entirely written by me without
# resorting to any dishonest means.
# Website(s) that I used for basic socket programming code are:
# URL(s): https://pythontic.com/modules/socket/udp-client-server-example

import socket
import threading
import os
import multiprocessing
import time
import threading
import sys
import random

msgFromClient       = "Hello UDP Server"

N = 8

Node_id = 0

serverAddressPort   = ("127.0.0.1", 12040)

clientAddress = "127.0.0.1"
clientPort = 10020


lock = threading.Lock()

bufferSize = 1024

s =[]

start = time.time()
end = time.time()

CloseEverything = False
#neighbors = [] * N
#receive = [] * N

HELLO_INTERVAL = 1
LSA_INTERVAL = 3
SPF_INTERVAL = 20

inpfile = ""

for i in range(1, len(sys.argv)):
    if(sys.argv[i] == '-i'):
        Node_id = int(sys.argv[i+1])
        i = i+1
    elif(sys.argv[i] == '-f'):
        inpfile = sys.argv[i+1]
        i = i+1
    elif(sys.argv[i] == '-o'):
        outfile = sys.argv[i+1]
        i = i+1
    elif(sys.argv[i] == '-h'):
        HELLO_INTERVAL = int(sys.argv[i+1])
        i = i+1
    elif(sys.argv[i] == '-a'):
        LSA_INTERVAL = int(sys.argv[i+1])
        i = i+1
    elif(sys.argv[i] == '-s'):
        SPF_INTERVAL = int(sys.argv[i+1])
        i = i+1


file_inp = open(inpfile, 'r')
Lines = file_inp.readlines()
tup = (Lines[0].strip().split(' '))
N = int(tup[0])
E = int(tup[1])

#neighbors = [[1, 2], [2, 3], [4], [5], [3, 5], []]
neighbors = []
for i in range(N):
    neighbors.append([])

receive = []
for i in range(N):
    receive.append([])
#receive = [[], [0], [0, 1], [1, 4], [2], [3, 4]]

min_max = []
for i in range(N):
    min_max_el = []
    for j in range(N):
        min_max_el.append((0, 0))
    min_max.append(min_max_el)

cost = []
for i in range(N):
    cost.append({})

sockets = []

topology = []
for i in range(N):
    elem_top = []
    for j in range(N):
        elem_top.append({})
    topology.append(elem_top)

seqNo = 0


do_update = True

for i in range(E):
    line_s = Lines[i + 1].split(' ')
    #print(line_s[0])
    edge_from = int(line_s[0])
    edge_to = int(line_s[1])
    neighbors[edge_from].append(edge_to)
    neighbors[edge_to].append(edge_from)
    receive[edge_to].append(edge_from)
    receive[edge_from].append(edge_to)
    cost_tuple_min = int(line_s[2])
    cost_tuple_max = int(line_s[3])
    min_max[edge_from][edge_to] = (cost_tuple_min, cost_tuple_max)
    min_max[edge_to][edge_from] = (cost_tuple_min, cost_tuple_max)

if(Node_id==0):
    print(neighbors)
    print(receive)
    print(min_max)


def send_receive_hello(router_num):
    global CloseEverything, cost
    while(CloseEverything == False):
        hello_packet = "HELLO : " + bin(router_num)[2:].zfill(8)
        
        for i in range(len(neighbors[router_num])):
            sockets[router_num].sendto(hello_packet.encode(), (clientAddress, clientPort + neighbors[router_num][i]))
            #print("sent {} to {}".format(router_num, clientPort + neighbors[router_num][i]))
        
        for i in range(len(receive[router_num])):
            hello_message = sockets[router_num].recvfrom(bufferSize)[0].decode()

        time.sleep(HELLO_INTERVAL/2)
        
        for i in range(len(receive[router_num])):
            hello_packet_reply = "HELLOREPLY:" + bin(router_num)[2:].zfill(8) + ":" + bin(receive[router_num][i])[2:].zfill(8) + ":" + str(random.randint(min_max[receive[router_num][i]][router_num][0], min_max[receive[router_num][i]][router_num][1]))
            sockets[router_num].sendto(hello_packet_reply.encode(), (clientAddress, clientPort + receive[router_num][i]))

        for i in range(len(neighbors[router_num])):
            cost_message = sockets[router_num].recvfrom(bufferSize)[0].decode()
            if(cost_message[5] != 'R'):
                continue
            #print(cost_message)
            
            cost_to = int(cost_message[11:19], 2)
            cost_from = int(cost_message[20:28], 2)
            actual_cost = int(cost_message[29:])
            print("actual_cost is {}", actual_cost)
            cost[cost_from][str(cost_to)] = actual_cost

        if(router_num == 0):
            print(cost)

        time.sleep(HELLO_INTERVAL/2)

def send_LSA_packet(router_num):

    global seqNo, CloseEverything, do_update, cost
    while(CloseEverything == False):
        time.sleep(LSA_INTERVAL)
        # print("heredsf")
        LSA_packet = "LSA:" + bin(router_num)[2:].zfill(8) + ":" +  bin(seqNo)[2:].zfill(8) + ":" + bin(len(cost[router_num]))[2:].zfill(8)
        for key, value in cost[router_num].items():
            LSA_packet = LSA_packet + ":" + bin(int(key))[2:].zfill(8) + ":" + bin(value)[2:].zfill(8)
        #print("router {} :::    ".format(router_num), LSA_packet)

        for i in range(N):
            if(i != router_num):
                sockets[router_num].sendto(LSA_packet.encode(), (clientAddress, clientPort + i))

            
        for i in range(N):
            if(i != router_num):
                LSA_recv = sockets[router_num].recvfrom(bufferSize)[0].decode()
                if(router_num == 0):
                    print(LSA_recv)
                if(LSA_recv[5] == 'R'):
                    cost_to = int(cost_message[11:19], 2)
                    cost_from = int(cost_message[20:28], 2)
                    actual_cost = int(cost_message[29:])
                    print("actual_cost is {}", actual_cost)
                    cost[cost_from][str(cost_to)] = actual_cost
                    
                #print(LSA_recv)
                got_from = int(LSA_recv[4:12], 2)
                seq = int(LSA_recv[13:21], 2)
                #print(seq)
                if(do_update):
                    item_num = int(LSA_recv[22:30], 2)
                    for i in range(item_num):
                        dest = int(LSA_recv[31 + 18*i : 39 + 18*i], 2)
                        #print(LSA_recv[40 + 18*i : 48 + 18*i])
                        cost_new = int(LSA_recv[40 + 18*i : 48 + 18*i], 2)
                        # cost__ = int(LSA_recv[40 * 18*i : 48 + 18*i], 2)
                        #print("got from {} dest {} cost {}".format(got_from, dest, cost_new))
                        topology[router_num][got_from][str(dest)] = cost_new
                        # print(topology)
        topology[router_num][router_num] = cost[router_num]
        # if(router_num == 0):
        #     print(topology[router_num])
        
    # print("topology for {} ".format(router_num), end = "  ")
    # print(topology[router_num])

def Dijkstra(router_num):
    global start, end, CloseEverything, do_update, cost

    open("Node_{}.output".format(router_num), "w").close()

    while(CloseEverything == False):
        time.sleep(SPF_INTERVAL)

        # if(router_num == 0):
        #     print(topology)
        end = int(time.time() - start)
        time.sleep(1.5)
        current_topo = topology[router_num]
        if(Node_id == 0):
            print(cost)
        RTR_file = open("Node_{}.output".format(router_num ), "a")

        RTR_file.write("Graph now : \n")
        for i in range(N):
            RTR_file.write("Node {}  :  ".format(i))
            for key, value in current_topo[i].items():
                RTR_file.write("'{}' : {},  ".format(key, value))
            RTR_file.write("\n")
        RTR_file.write("\n")
        RTR_file.write("______________________________________________________________\n")
        RTR_file.write("             Routing Table for Node No. {} at time {}\n".format( router_num, end))
        RTR_file.write("______________________________________________________________\n")
        RTR_file.write("   Destination   |            Path            |     Cost      |\n")
        path = [''] * N
        path[router_num] = str(router_num)
        visited = [False] * N
        dist = [1000000] * N
        tent = N
        dist[router_num] = 0
        
        current = -1
        while(True):
            current = -1
            max = 1000000
            for i in range(N):
                if(dist[i] < max and visited[i] == False):
                    max = dist[i]
                    current = i
                    #print("router {} , current{}".format(router_num, current))
            if(current == -1):
                break
            #print("current is {} ", current)
            visited[current] = True        
            for key, value in current_topo[current].items():
                #print(dist[current] + value)
                if(dist[int(key)] > dist[current] + value):
                    dist[int(key)] = value + dist[current]
                    path[int(key)] = path[current] + "-{}".format(int(key))
            flag = 0
            for i in range(N):
                if(visited[i] == False):
                    flag = 1
            if(flag == 0):
                break

        for i in range(N):
            if(path[i] != '' and path[i] != str(router_num)):
                RTR_file.write("{:^{}}|{:^{}}|{:^{}}|\n".format("{}".format(i), 17, "{}".format(path[i]), 28, "{}".format(dist[i]), 15))
        # print("router {} path{}".format(router_num, path))
        RTR_file.write("______________________________________________________________\n")
        RTR_file.write("\n\n\n")
        RTR_file.close()
        time.sleep(2)

        if(time.time() - start > 150):
            CloseEverything = True

def RTR( router_num):
    nn = 10

    time.sleep(1)
    SRH = threading.Thread(target=send_receive_hello, args = (router_num, ))
    SLSA = threading.Thread(target = send_LSA_packet, args = (router_num, ))
    Dijk = threading.Thread(target = Dijkstra, args = (router_num, ))

    Dijk.start()
    SRH.start()
    SLSA.start()

    SRH.join()
    SLSA.join()

    Dijk.join()



print("SSFSLKFLKSNLK")

for i in range(N):
    s = socket.socket(family = socket.AF_INET, type=socket.SOCK_DGRAM)
    s.bind((clientAddress, clientPort + i))
    sockets.append(s)
        

processes = []
for i in range(N):
    p = multiprocessing.Process(target=RTR, args = (i, ))
    p.start()
    processes.append(p)


for p in processes:
    p.join()











