import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# membaca file CSV ke dalam DataFrame
df = pd.read_csv('.\datavisualitation\pwr2011-2023.csv')


# mengubah nama kolom
df.columns = ["tahun", 'akun','anggaran','realisasi', 'persen']

# mengubah nama-nama akun tertentu
df['akun'] = df['akun'].replace(['Belanja','Pendapatan','Belanja Pegawai Tidak Langsung','Belanja Pegawai Langsung'],['Belanja Daerah','Pendapatan Daerah','Belanja Pegawai', 'Belanja Pegawai'])

# find and replace
df['realisasi'] = df['realisasi'].str.replace('.', '', regex=False)\
                                 .str.replace(',','.', regex=False)\
                                 .str.replace(' M', '', regex=False)

# membuat data menjadi float dan mengalikannya dengan 1000
df['realisasi'] = df['realisasi'].astype(float) * 1000000000

# Filtering dengan kondisi yang lebih kompleks
df = df.loc[(df['akun'] == 'Belanja Daerah') | (df['akun'] == 'Belanja Pegawai') ]


df = df.drop_duplicates()

df = df.drop(['anggaran', 'persen'], axis=1)

df = df.pivot_table(values='realisasi', index='tahun', columns='akun', aggfunc='sum').reset_index()

df['persentage'] = round(df['Belanja Pegawai'] / df['Belanja Daerah'] * 100 , 2)

# menampilkan DataFrame
# print(df)

########################################################
########################################################
########################################################

# membuat dataset dari dataframe yang telah dibuat
tahun = np.array(df['tahun']).astype(str)
x = np.arange(0,len(tahun),1)
y1 = np.array(df['Belanja Daerah'])
y2 = np.array(df['Belanja Pegawai'])
y3 = np.array(df['persentage'])

# membuat figure dan ax1
fig, ax1 = plt.subplots()

# membuat ax2
ax2 = ax1.twinx()

# membuat bar dan plot
ax1.bar(x - 0.2, y1,0.4)
ax1.bar(x + 0.2,y2,0.4)
ax2.plot(x,y3)

# membuat array untuk titik-titik sumbu
xstep = x
ax1step = np.arange(0,2500000000000,300000000000)
ax2step = np.arange(30,200,20)

# membuat array untuk label titik-titik sumbu
xlabel = tahun
ax1label = list(map(lambda x: '{} T'.format(round(x/1000000000000,2)), ax1step))
ax2label = list(map(lambda x: '{} %'.format(x), ax2step))

# mengatur jarak titik-titik sumbu axis 1 dan axis 2
ax1.set_yticks(ax1step)
ax2.set_yticks(ax2step)

# mengatur label titik-titik sumbu axis 1 dan axis 2
ax1.set_yticklabels(ax1label)
ax2.set_yticklabels(ax2label)

# mengatur ukuran ticklabel
ax1.tick_params(axis='x',labelsize=8)
ax1.tick_params(axis='y',labelsize=8)
ax2.tick_params(axis='y',labelsize=8)

# mengatur jarak titik-titik sumbu x beserta label di setiap titik-titiknya
plt.xticks(xstep, xlabel)

# menampilkan grafik
plt.show()