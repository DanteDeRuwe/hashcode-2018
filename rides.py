input_file = open('d_metropolis.in', 'r')

splitted_arr = []

for l in input_file:
    arr = l.strip().split(' ')
    arr = [int(t) for t in arr]
    splitted_arr.append(arr)

def distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def get_rides(arr):
    rides_dict = {}
    i = 0
    for ride in arr[1:]:
        rides_dict[str(i)] = {
            'start' : [ride[0], ride[1]] ,
            'finish': [ride[2], ride[3]] ,
            'early': ride[4],
            'late': ride[5],
            'distance': distance((ride[0], ride[1]), (ride[2], ride[3]))
        }
        i += 1

    return rides_dict



class Car():
    def __init__(self, arr, f):
        self.carnumber = f
        self.rides = arr[0][3]
        self.max_steps = arr[0][5]
        self.pos = [0,0]
        self.timer = 0
        self.idle = True
        self.assigned_rides = []


T = splitted_arr[0][5]
F = splitted_arr[0][2]
R = splitted_arr[0][0]
C = splitted_arr[0][1]


cars = [Car(splitted_arr, f) for f in range(F)]
rides = get_rides(splitted_arr)
#print(rides)

for t in range(T):
    for i,car in enumerate(cars):
        if car.timer == 0:
            car.idle = True
        if car.idle:
            ride_scores = {}
            for j,ride in rides.items():
                A_part = 1-(((-distance(car.pos, ride['start']) - t + ride['early'])) / T)
                if (-distance(car.pos, ride['start']) - t + ride['early']) <0:
                    A_part = 0
                B_part = (ride['distance'] / (R+C) )
                C_part =  1- ((distance(car.pos, ride['start'])) / (R+C))
                A,B,C = (1,0.05,1)

                score = A*A_part + B*B_part + C*C_part
                ride_scores[str(j)] =  score
                #print('car :' + str(car.carnumber) + '\n  ride: ' + str(j) + '\n A,B,C: ' + str(A_part) + ',' + str(B_part) + ',' + str(C_part) + ',\n\n SCORE: ' + str(A*A_part + B*B_part + C*C_part) + '\n\n\n')
            s = [(k, ride_scores[k]) for k in sorted(ride_scores, key=ride_scores.get, reverse=True)]
            if len(s) == 0:
                break
            #print(s)
            best_ride_number = s[0][0]
            best_ride = rides[best_ride_number]
            cars[i].assigned_rides.append(best_ride_number)
            del rides[best_ride_number] #ride got removed
            if rides == {}:
                break
            waitingtime = (-distance(car.pos, best_ride['start']) - t + best_ride['early'])
            if waitingtime < 0:
                waitingtime = 0

            cars[i].timer += distance(car.pos, best_ride['start']) + best_ride['distance'] + waitingtime
            cars[i].pos = best_ride['finish']
            cars[i].idle = False
        if cars[i].timer >0:
            cars[i].timer -= 1

    if t%100 == 0:
        print(t)

print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n')

for i,_ in enumerate(cars):
    list = cars[i].assigned_rides
    outputfile = open('testje3.txt', 'w')
    line = str(len(list)) + ' ' + ' '.join(list)
    # outputfile.write(line)
    print(line)