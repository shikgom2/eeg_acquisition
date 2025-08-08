import numpy as np
import mne

# https://physionet.org/content/eegmmidb/1.0.0/#files-panel

#All run : Event 0 corresponds to rest

#3,4,7,8,11,12 run : Event 1 corresponds left fist 
#5,6,9,10,13,14 run : Event 1 corresponds both fists

#3,4,7,8,11 run : Event 2 corresponds right fist 
#5,6,9,10,13 run : Event 2 corresponds both feet

#first event 672 => 672/160hz = 4.2sec events

run1 = [3,4,7,8,11,12]
run2 = [5,6,9,10,13,14]

hz = 160
channel = 64
sec = 4

left_fist_li = []
right_fist_li = []
both_fist_li = []
both_feet_li = []

for i in range(1, 110):
    
    subject = ""

    if(i>=100):
        subject = "S" + str(i)
    elif(i>=10):
        subject = "S0" + str(i)
    else:
        subject = "S00" + str(i)
    
    for j in range(3, 15):

        run = ""
        if(j<10):
            run = "R0" + str(j)
        else:
            run = "R" + str(j)

        url = '../Datasets/physio_mi/' + subject + '/' + subject + run + '.edf'
        
        #load
        raw = mne.io.read_raw_edf(url)
        data = raw.get_data()
        events, event_id = mne.events_from_annotations(raw)
        #print(events)
        #print(type(data), data.shape)
        
        #epoching

        for k in range(len(events)):
            
            tmp = data[:, events[k][0] : events[k][0] + (hz*sec)]

            if(np.shape(tmp)[0] != channel or np.shape(tmp)[1] != (hz * sec)): #(64, 640)
                continue

            #left fist
            if(j in run1 and events[k][-1] == 2):
                left_fist_li.append(tmp)
            elif(j in run1 and events[k][-1] == 3):
                right_fist_li.append(tmp)
            elif(j in run2 and events[k][-1] == 2):
                both_fist_li.append(tmp)
            elif(j in run2 and events[k][-1] == 3):
                both_feet_li.append(tmp)

left_fist = np.stack(left_fist_li, axis=0)
right_fist = np.stack(right_fist_li, axis=0)
both_fist = np.stack(both_fist_li, axis=0)
both_feet = np.stack(both_feet_li, axis=0)

sources = np.concatenate([left_fist, right_fist, both_fist, both_feet], axis=0)


target = [0] * 4950 + [1] * 4894 + [2] * 4905 + [3] * 4924

np.save('../Datasets/physio_mi/sources.npy', sources)
np.save('../Datasets/physio_mi/target.npy', target)

print("Done!")