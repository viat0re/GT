import numpy as np
import pandas as pd


# create raw data
raw_data={}
rng = np.random.default_rng()

df = pd.DataFrame(columns=['windows', 'clients', 'intervals','area_before','area_after'])




for num_of_wins in range(1,6):
    for num_of_clients in range(5,51,5):
        for rep in range(1000):
            windows = []
            points = []

            # create windows for each client
            for client in range(num_of_clients):

                a = rng.uniform(low=0, high=100, size=2*num_of_wins)
                b = sorted(a)
                c = [(b[i],b[i+1]) for i in range(len(b)) if i%8==0]
                windows.append(c)

                points += [(x,'left') for (x,y) in c]
                points += [(y,'right') for (x,y) in c]


            # join the windows
            windows_new = []
            points.sort(key=lambda x: x[0])
            counter = 0
            a=points[0]
            for p in points:

                if p[1] == 'left':
                    counter += 1
                    if counter == num_of_clients:  a = p

                if p[1] == 'right':
                    if counter == num_of_clients:
                        b = p
                        windows_new.append((a,b))
                    counter -= 1

            # fill database
            if len(windows_new)>0:
                df.loc[len(df)] = [num_of_wins,
                                   num_of_clients,
                                   len(windows_new),
                                   round(sum([b-a for (a,b) in windows[0]]), 2),
                                   round(sum([b[0]-a[0] for (a,b) in windows_new]), 2)]


# print(df.groupby(['windows', 'clients']).mean())
# print(df.groupby(['windows', 'clients']).size())

df1 = df.groupby(['windows', 'clients']).agg(count=('intervals', 'size'),
                                             mean=('intervals', 'mean'),
                                             stdev=('intervals', 'std'),
                                             area_perc_before=('area_before','mean'),
                                             area_perc_after=('area_after','mean'))

print(df1[df1['count'] >= 10])