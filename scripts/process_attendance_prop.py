import pandas as pd

df = pd.read_csv('../data/inputs/RIJAAL Camp June 2024 (Points System) - Sheet1.csv')
new_df = pd.DataFrame(columns=['fname', 'lname', 'code'])

# make fname and lname columns from the split of the 'NAME:' column
new_df['fname'] = df['NAME:'].apply(lambda x: x.split(' ')[0])
new_df['lname'] = df['NAME:'].apply(lambda x: x.split(' ')[1])

def generate_rand_code():
    import random
    return random.randint(1000, 9999)

# make code column with random 4-digit numbers
new_df['code'] = new_df['fname'].apply(lambda x: generate_rand_code())

new_df.to_csv('../data/outputs/campers.csv', index=False)
