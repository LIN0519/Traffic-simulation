import random
from random import choice
import math
import sys
import time
import tkinter as tk
from typing import Text
from typing_extensions import IntVar
import numpy as np
CAR_SPEED = 0.4                                                                 # (0.05km/s)
P_THRESHOLD = 25
ETROPY_THRESHOLD=25
PROBABILITY = (1/12) * math.exp(-1/12)

root = tk.Tk()
root.title('simulation')
mycanvas = tk.Canvas(root,width=520,height=620)
time_label = mycanvas.create_text(20,530,text='',anchor='nw')
num_car_label = mycanvas.create_text(20,550,text='',anchor='nw')
Q1handoff = mycanvas.create_text(20,570,text='',anchor='nw')
Q2handoff = mycanvas.create_text(20,590,text='',anchor='nw')                     # label 
handoff1 = 0
handoff2 = 0
handoff3 = 0
handoff4 = 0
call_handoff1 = 0
call_handoff2 = 0
call_handoff3 = 0
call_handoff4 = 0
              
class BaseStation:
    def __init__(self,x,y,frequency,num):
        self.x_position = x
        self.y_position = y
        self.frequency = frequency
        self.num = num


class cars:
    def __init__(self,x,y,current_direction,next_direction):
        self.x_position = x
        self.y_position = y
        self.current_direction = current_direction
        self.next_direction = next_direction
        
        self.bs_num1 = 0         
        self.bs_num2 = 0
        self.bs_num3 = 0
        self.bs_num4 = 0                      # connected     basestation

        self.call_time = 0
        self.canvas = mycanvas
        self.dot = self.canvas.create_rectangle(7+self.x_position,7+self.y_position,13+self.x_position,13+self.y_position,fill='green')       #car point
              
    def move(self):
        speed = CAR_SPEED                                                          # 車速
        if self.current_direction == 'down':                                 # 從上面進來 往下走
            if self.next_direction == 'left':
                self.x_position = self.x_position + speed
                self.canvas.move(self.dot,speed,0)   
                self.current_direction == 'right'                     
            elif self.next_direction == 'right':
                self.x_position = self.x_position - speed
                self.canvas.move(self.dot,-speed,0)
                self.current_direction == 'left'  
            elif self.next_direction == 'forward':
                self.y_position = self.y_position - speed
                self.canvas.move(self.dot,0,-speed)
            elif self.next_direction == 'back':
                self.y_position = self.y_position + speed
                self.canvas.move(self.dot,0,speed)
                self.current_direction == 'up'  
        elif self.current_direction == 'up':                                # 從下面進來 往上走
            if self.next_direction == 'left':
                self.x_position = self.x_position - speed
                self.canvas.move(self.dot,-speed,0)
                self.current_direction == 'left'
            elif self.next_direction == 'right':
                self.x_position = self.x_position + speed
                self.canvas.move(self.dot,speed,0)
                self.current_direction == 'right'
            elif self.next_direction == 'forward':
                self.y_position = self.y_position + speed
                self.canvas.move(self.dot,0,speed)
                self.current_direction == 'up'
            elif self.next_direction == 'back':
                self.y_position = self.y_position - speed
                self.canvas.move(self.dot,0,-speed)  
                self.current_direction == 'down'  
        elif self.current_direction == 'right':                             # 從左邊進來
            if self.next_direction == 'left':
                self.y_position = self.y_position + speed
                self.canvas.move(self.dot,0,speed)
                self.current_direction == 'up'
            elif self.next_direction == 'right':
                self.y_position = self.y_position - speed
                self.canvas.move(self.dot,0,-speed)
                self.current_direction == 'down'
            elif self.next_direction == 'forward':
                self.x_position = self.x_position + speed
                self.canvas.move(self.dot,speed,0)
                self.current_direction == 'right'
            elif self.next_direction == 'back':
                self.x_position = self.x_position - speed
                self.canvas.move(self.dot,-speed,0)
                self.current_direction == 'left'
        elif self.current_direction == 'left':                             # 從右邊進來
            if self.next_direction == 'left':
                self.y_position = self.y_position - speed
                self.canvas.move(self.dot,0,-speed)
                self.current_direction == 'down'
            elif self.next_direction == 'right':
                self.y_position = self.y_position + speed
                self.canvas.move(self.dot,0,speed)
                self.current_direction == 'up'
            elif self.next_direction == 'forward':
                self.x_position = self.x_position - speed
                self.canvas.move(self.dot,-speed,0)
                self.current_direction == 'left'
            elif self.next_direction == 'back':
                self.x_position = self.x_position + speed
                self.canvas.move(self.dot,speed,0)
                self.current_direction == 'right'        
        if self.x_position < 0 or self.x_position > 500 or self.y_position < 0 or self.y_position > 500:
            self.canvas.delete(self.dot)                                                                                   # delete self.dot
        self.canvas.update()    

enter_point = []
BS_location = []
crossroad = []
BS_freq = [100,200,300,400,500,600,700,800,900,1000]
def enter():
    for up in range(0,9):
        enter_point.append([50+50*up,0])
    for down in range(0,9):
        enter_point.append([50+50*down,500])
    for left in range(0,9):
        enter_point.append([0,50+50*left])
    for right in range(0,9):
        enter_point.append([500,50+50*right])                      #save enter point
def intersection():
    for x in range(0,11):
        for y in range(0,11):
            crossroad.append([50*x,50*y])                          #save intersection point

def set_BS():
    for i in range(0,10):
        for j in range(0,10):
            BS_location.append([25+50*i,25+50*j])                  #save i00 center point
    
def cal_db(car,bs): 
    path_loss = 32.45 + 20 * math.log(bs.frequency,10) + 20 * math.log((((bs.x_position-car.x_position) * 0.05)**2 + ((bs.y_position-car.y_position) * 0.05)**2)**0.5,10)
    power = 120 - path_loss
    return power                                                   # calculate power
                  
def set_call_time(car):
    if car.call_time == 0:
        rand = random.randint(1,1800)
        if rand == 1:
            car.call_time = np.random.normal(300,10)                                      # call  call_time    avg:300  div:10

def sub_call_time(car):
    if(car.call_time!=0):
       car.call_time= car.call_time-1

def set_first_base(car):
    for i in range(len(BS_list)-1):
        if cal_db(car,BS_list[i]) > cal_db(car,BS_list[i+1]):
                car.bs_num1 = BS_list[i].num
                car.bs_num2 = BS_list[i].num
                car.bs_num3 = BS_list[i].num
                car.bs_num4 = BS_list[i].num
        else:
                car.bs_num1 = BS_list[i+1].num
                car.bs_num2 = BS_list[i+1].num 
                car.bs_num3 = BS_list[i+1].num 
                car.bs_num4 = BS_list[i+1].num                                              #choose first basestation            

def Minium(car,BS_list):
    global handoff1
    global call_handoff1                         
    if cal_db(car,BS_list[car.bs_num1]) < P_THRESHOLD:                                       # < Pmin
        nowbs = car.bs_num1
        for i in range(len(BS_list)):
            if cal_db(car,BS_list[i]) > cal_db(car,BS_list[car.bs_num1]) and cal_db(car,BS_list[i]) > P_THRESHOLD:
                car.bs_num1 = BS_list[i].num
        if nowbs != car.bs_num1 :
            handoff1 = handoff1 + 1                                                          # change basestation if new db is greather than P_THRESHOLD
        if nowbs != car.bs_num1 and car.call_time!=0 :
            call_handoff1 = call_handoff1 + 1                                                # change basestation when call if new db is greather than P_THRESHOLD
                                                        
def Best_effort(car,BS_list):
    global call_handoff2
    global handoff2
    nowbs = car.bs_num2
    for i in range(len(BS_list)):
        if cal_db(car,BS_list[i]) > cal_db(car,BS_list[car.bs_num2]):
            car.bs_num2 = BS_list[i].num
    if nowbs != car.bs_num2:
        handoff2 = handoff2 + 1        
    if nowbs != car.bs_num2 and car.call_time !=0:
        call_handoff2 = call_handoff2 + 1

def Entropy(car,BS_list):
    global call_handoff3
    global handoff3
    nowbs = car.bs_num3
    for i in range(len(BS_list)):
        if cal_db(car,BS_list[i])-ETROPY_THRESHOLD > cal_db(car,BS_list[car.bs_num3]) :
            car.bs_num3 = BS_list[i].num
    if nowbs != car.bs_num3 :
        handoff3 = handoff3 + 1        
    if nowbs != car.bs_num3 and car.call_time!=0:
        call_handoff3 = call_handoff3 + 1
                                                           
def My_policy(car,BS_list):
    global call_handoff4
    global handoff4
    nowbs = car.bs_num4
    min =  10000
    for i in range(len(BS_list)):
        distance = math.sqrt(math.pow((BS_list[i].x_position-car.x_position) ,2) + math.pow((BS_list[i].y_position-car.y_position) ,2))
        if min >distance  :
            min = distance
            car.bs_num4 = BS_list[i].num
    if nowbs != car.bs_num4:
        handoff4 = handoff4 + 1
    if nowbs != car.bs_num4 and car.call_time!=0:
        call_handoff4 = call_handoff4 + 1                                                                # change    basestation         (choose nearest basestation)

if __name__ == '__main__':
    mycanvas.create_rectangle(10,10,510,510)
    for i in range(1,10):
        mycanvas.create_line(10,10+50*i,510,10+50*i)
        mycanvas.create_line(10+50*i,10,10+50*i,510)                        # draw  line
    mycanvas.pack()                                                         # save line to graph
    BS_list = []
    car_list = []
    enter()
    intersection()
    set_BS()
    num = 0
    t = 0
    for b in BS_location:                                                    # random基地台
        rand = random.randint(1,10)
        if rand == 1:
            BS = BaseStation(b[0],b[1],choice(BS_freq),num)                  #編號(num)   
            bias = random.randint(1,4)
            if bias == 1:                                                  
                BS.x_position = BS.x_position - 2
            if bias == 2:
                BS.x_position = BS.x_position + 2
            if bias == 3:
                BS.y_position = BS.y_position + 2
            if bias == 4:
                BS.y_position = BS.y_position - 2                                          # 上下左右有1/4機率偏移
            BS_list.append(BS)
            num = num + 1
    for b in BS_list: 
        mycanvas.create_oval(3+b.x_position,3+b.y_position,17+b.x_position,17+b.y_position,fill='blue')       # draw base
                                          
    while(True):                                                             #build car_list
        for e in enter_point:
            rand = random.uniform(0,1)
            if rand <= PROBABILITY:
                if e[1] == 0:                                                 # 從下面進來
                    car = cars(e[0],e[1],'up','')
                elif e[1] == 500:                                             # 從上面進來
                    car = cars(e[0],e[1],'down','')
                elif e[0] == 0:                                               # 從左邊進來
                    car = cars(e[0],e[1],'right','')
                elif e[0] == 500:                                             # 從右邊進來
                    car = cars(e[0],e[1],'left','')
                car_list.append(car)                                          # save every cars
                set_first_base(car)                                           # initialize every policy first connect  basestation
        for car in car_list:
            for cross in crossroad:
                if car.x_position == cross[0] and car.y_position == cross[1]:           # car on intersection
                    rand = random.randint(1,32)
                    if rand <= 16:                                              
                        car.next_direction = 'forward'
                        break
                    if rand >= 17 and rand <= 18:                                
                        car.next_direction = 'back'
                        break
                    if rand >= 19 and rand <= 25:                                
                        car.next_direction = 'left'
                        break
                    if rand >= 26 and rand <= 32:                                
                        car.next_direction = 'right'                                         # dicision
                        break
            car.move()
        
        for car in car_list:
            set_call_time(car)    
            Minium(car,BS_list)
            Best_effort(car,BS_list)
            Entropy(car,BS_list)
            My_policy(car,BS_list)
            sub_call_time(car)
            mycanvas.itemconfig(time_label,text='time: '+str(t))
            mycanvas.itemconfig(num_car_label,text='number of cars: '+str(len(car_list)))
            mycanvas.itemconfig(Q1handoff,text='handoff times: Pmin: '+str(handoff1)+' / best effort: '+str(handoff2)+' / entropy: '+str(handoff3)+' / my policy: '+str(handoff4))
            mycanvas.itemconfig(Q2handoff,text='call handoff times: Pmin: '+str(call_handoff1)+' / best effort: '+str(call_handoff2)+' / entropy: '+str(call_handoff3)+' / my policy: '+str(call_handoff4))
            if car.x_position < 0 or car.x_position > 500 or car.y_position < 0 or car.y_position > 500:     
                car_list.remove(car)                                                                               # remove car 超出
        t = t + 1
        time.sleep(0.01)                                                                                          # sleep 0.01 sec       
    root.mainloop()