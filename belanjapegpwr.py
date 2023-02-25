import pandas as pd

# membaca file CSV ke dalam DataFrame
df = pd.read_csv('.\datavisualitation\pwr2011-2023.csv')

df.columns = ["tahun", 'akun','anggaran','realisasi', 'persen']

df['akun'] = df['akun'].replace(['Belanja','Pendapatan','Belanja Pegawai Tidak Langsung','Belanja Pegawai Langsung'],['Belanja Daerah','Pendapatan Daerah','Belanja Pegawai', 'Belanja Pegawai'])

df['realisasi'] = df['realisasi'].str.replace('.', '', regex=False)\
                                 .str.replace(',','.', regex=False)\
                                 .str.replace(' M', '', regex=False)

df['realisasi'] = df['realisasi'].astype(float) * 1000
# Filtering dengan kondisi yang lebih kompleks
df = df.loc[(df['akun'] == 'Belanja Daerah') | (df['akun'] == 'Belanja Pegawai') ]

df = df.drop_duplicates()

df = df.drop(['anggaran', 'persen'], axis=1)

df = df.pivot_table(values='realisasi', index='tahun', columns='akun', aggfunc='sum').reset_index()

df['persentage'] = round(df['Belanja Pegawai'] / df['Belanja Daerah'] * 100 , 2)
# menampilkan DataFrame
print(df)