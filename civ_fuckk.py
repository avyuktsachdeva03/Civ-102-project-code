import matplotlib.pyplot as plt
from scipy import integrate
import math
#%%
'''we put up the calculated values of the I, y_bar etc which are
put in functions later. we also have the four train cases and point loads
case.'''

p = 1

#train on left end
train_case_1 = {"a":[0,0,"sp"],"b":[52,-1,"l"],"c":[228,-1,"l"],"d":[392,-1,"l"],"e":[568,-1,"l"],"f":[732,-1,"l"],"g":[908,-1,"l"],"h":[1060,0,"sr"],"i":[1250,0,"l"]}
#train on right end
train_case_2 = {"a":[0,0,"sp"],"b":[342,-1,"l"],"c":[518,-1,"l"],"d":[682,-1,"l"],"e":[858,-1,"l"],"f":[1022,-1,"l"],"g":[1060,0,"sr"],"h":[1198,-1,"l"],"i":[1250,0,"l"]}
#train in the centre of the bridge
train_case_3 = {"a":[0,0,"sp"],"b":[197,-1,"l"],"c":[373,-1,"l"],"d":[537,-1,"l"],"e":[713,-1,"l"],"f":[877,-1,"l"],"g":[1053,-1,"l"],"h":[1060,0,"sr"],"i":[1250,0,"l"]}
#train in the centre of the supports
train_case_4 = {"a":[0,0,"sp"],"b":[102,-1,"l"],"c":[278,-1,"l"],"d":[442,-1,"l"],"e":[618,-1,"l"],"f":[782,-1,"l"],"g":[958,-1,"l"],"h":[1060,0,"sr"],"i":[1250,0,"l"]}
#point loads
point_load = {"a":[0,0,"sp"],"b":[550,-1,"l"],"c":[1060,-1,"sr"],"d":[1250,-1,"l"]}
length = 1280
members = point_load

y_bar = 41.6
Q_mat = 6292
Q_glue = 3901
I = 413741
b_mat = 1.27*2
b_glue = 20
h = 75
E = 4000
nu = 0.2
t = 1.27
'''here the function calculates the reaction forces on the supports 
in terms of p'''
for i in range(len(members)):
    temporary_list = sorted(members.keys())
    if members[temporary_list[i]][2] == "sp":
        j = 0
        
        while members[temporary_list[i+j]][2] != "sr":
            j += 1
            
            if members[temporary_list[i+j]][2] == "sr":

                if i-1 >= 0:
                    
                    before = members[temporary_list[i+j]][1]*members[temporary_list[i+j]][0]

                else:
                    temporary_answer = 0
                    for k in range(len(members)):
                        temporary_answer += members[temporary_list[i+k]][1]*members[temporary_list[i+k]][0]
                    members[temporary_list[i+j]][1] = -temporary_answer/members[temporary_list[i+j]][0]
                    another_temporary_answer = 0
                    for ijk in range(len(members)):
                        another_temporary_answer += members[temporary_list[ijk]][1]
                    members[temporary_list[i]][1] = -another_temporary_answer
    else:
        continue
print(members)
#%%
'''this function calculates and plots the sfd and the bmd along with the
manually inputed values of the lowest force breaking the bridge 
(most likely shear force of matboard)'''
def sfd_bmd():
    global bmd_temp
    x_values = []
    for distances in range(len(temporary_list)):
        x_values.append(members[temporary_list[distances]][0])
        x_values.append(members[temporary_list[distances]][0])    
    #x_values = [0,0,342,342,518,518,682,682,858,858,1022,1022,1060,1060,1198,1198,1250,1250]
    y_values = []
    members_x_and_load = []
    
    for load in members:
        members_x_and_load.append((members[load][0], members[load][1]))
    
    members_x_and_load = sorted(members_x_and_load)
    print(members_x_and_load)
    
    y_values=[0]
    for i in range(0, len(members_x_and_load)):
        last=y_values[-1]
        y_values.append(last+members_x_and_load[i][1])
        y_values.append(last+members_x_and_load[i][1])
    print(x_values)   
    y_values.pop(-1)  
    y_values = [jkjk*p for jkjk in y_values]
    if members == point_load:
        y_values[1] = -y_values[1]
        y_values[2] = -y_values[2]
    bmd_temp = integrate.cumtrapz(y_values,x_values,initial=0)
    print(y_values)
    print(max(y_values),min(y_values))
    plt.plot(x_values,y_values)
    plt.axhline(y=0,color='r',linestyle='-')
    plt.axhline(y=191)
    plt.axhline(y=-191)
    plt.title('SFD Point Load with Least Force Required to Break Bridge')
    sfd = plt.show()
    plt.plot(x_values,bmd_temp)
    plt.axhline(y=0,color='r',linestyle='-')
    plt.title('BMD Train Case 2')
    bmd = plt.show()
    return sfd,bmd


    
sfd_bmd()
#%%
'''the functions here take in the previously inputed values of physical 
properties and the max force experienced in the train case which was in 
train case 2 over the roller support'''
highest_force = abs(-223.89934867924524)
def matboard_shear_failure():
    v=(4*I*b_mat)/Q_mat
    return v

def glue_shear_failure():
    v=(2*I*b_glue)/Q_glue
    return v
def flexural_failure_compression_a():
    return (6*I)/(max(bmd_temp)*(y_bar-h/2))

def flexural_failure_compression_b():
    return (6*I)/(max(bmd_temp)*y_bar)

def flexural_failure_tension_a():
    return (30*I)/(max(bmd_temp)*y_bar)

def flexural_failure_tension_b():
    return (30*I)/(max(bmd_temp)*(y_bar-h/2))
def fos():
    return plate_buckling(b5,m5,y5)/highest_force
#the values are calculated manually and then put into thius function to find mid point deflection
def midpoint_deflection(ca,mid_a):
    mid = (ca*530)/1060 - mid_a
    return mid
#%%
'''here are the values for design zero '''
b1 = 77.46
m1 = 4
y1 = 33.4
b2 = 10
m2 = 0.425
y2 = 33.4
b3 = 32.13
m3 = 6
y3 = 32.13 
b4 = y_bar
m4 = 6
y4 = y_bar
b5 = 77.46
m5 = 4
y5 = y_bar
def plate_buckling(b,M,y):
    crit_n = (M*math.pi*math.pi*E*t*t)
    crit_d = (12*(1-nu**2))*(b**2)
    return (crit_n*I)/(crit_d*max(bmd_temp)*y)
#%%
'''these are the printed values of the failure forces'''
print(plate_buckling(b1,m1,y1)) 
print(plate_buckling(b2,m2,y2))
print(plate_buckling(b3,m3,y3))
print(plate_buckling(b4,m4,y4))
print(plate_buckling(b5,m5,y5))   
print(fos())
print(midpoint_deflection(4.57,0.906))
print(matboard_shear_failure(),glue_shear_failure(),flexural_failure_tension_b(),flexural_failure_compression_a())