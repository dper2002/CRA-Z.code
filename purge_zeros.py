import pandas as pd

deco = pd.read_csv("WildfireData.csv",
                   usecols=["roll", "pitch", "yaw", "event_id"], dtype=int)

#deco = deco.query("roll != 0 or pitch != 0 or yaw != 0")