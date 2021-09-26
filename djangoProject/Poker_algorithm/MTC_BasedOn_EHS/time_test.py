from MTC_BasedOn_EHS import Winning_p_forecast as wpf
import time

a = [52,100,1000,5000,7500,10000,30000,50000,100000,500000]
with open("../visualization/time.txt", 'w') as f:
    for _ in a:
        start = time.perf_counter()
        b=wpf.Forecaster([50,41],[39,9,7],_)
        end=time.perf_counter()
        f.write(str(_)+':'+str(end-start)+'\n')