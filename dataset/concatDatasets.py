import pandas as pd

# Read the CSV file into a DataFrame
dodungnhabep = pd.read_csv('dodungnhabep.csv')
dodungphongngu = pd.read_csv('dodungphongngu.csv')
trangtrinhacua = pd.read_csv('trangtrinhacua.csv')
ngoaitroi = pd.read_csv('ngoaitroi.csv')
noithat = pd.read_csv('noithat.csv')

result = pd.concat([dodungnhabep, dodungphongngu, ngoaitroi, trangtrinhacua, ngoaitroi])

# Resetting index for the concatenated DataFrame
result.to_csv('tiki1.csv', index=False)  