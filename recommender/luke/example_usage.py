import os

import read_file as rf
import collab_by_item as ci
import collab_by_user as cu

user_entries = [["minigames", '0912696591', 5.0], ["minigames", '0615391206', 5.0], ["minigames", '0689027818', 5.0]]
df, df2, user_ID = rf.read_file(user_entries, os.path.join('..', 'nick', 'output.csv'))
print(cu.collab_by_user(df, df2, user_ID))
print(ci.collab_by_item(df2, user_ID))
