#%%
from pathlib import Path

base_log_folder = 'logs/dag_id=marketvol'

#%%
file_list = Path(base_log_folder).rglob('*.log')
totalerrors = []
totalcount = 0

def analyze_file(file):
    errors = []
    count = 0

    # first_line = file.readline().strip()
    # print(f"First Line: {first_line}")

    for line in file:
         if 'ERROR' in line:
              count+=1
              errors.append(line.strip())
    return count,errors

def printinfo(count, errors):
     print(f'Total number of errors: {count}')
     print(f'Here are all the errors:')
     for item in errors:
          print(item)

for filepath in file_list:
    with open(filepath, 'r') as f:
            count, errors = analyze_file(f)
            totalcount += count
            if errors:
                totalerrors.extend(errors)
            
            
printinfo(totalcount, totalerrors)


# %%
