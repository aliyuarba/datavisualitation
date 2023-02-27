import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# membaca file CSV ke dalam DataFrame
df = pd.read_csv('.\datavisualitation\jateng22.csv')

# mengubah nama kolom
df.columns = ["wil", 'akun','anggaran','realisasi', 'persen']

# mengubah nama-nama akun tertentu
df['akun'] = df['akun'].replace(['Belanja','Pendapatan','Belanja Pegawai Tidak Langsung','Belanja Pegawai Langsung'],['Belanja Daerah','Pendapatan Daerah','Belanja Pegawai', 'Belanja Pegawai'])

# find and replace
df['realisasi'] = df['realisasi'].str.replace('.', '', regex=False)\
                                 .str.replace(',','.', regex=False)\
                                 .str.replace(' M', '', regex=False)

# membuat data menjadi float dan mengalikannya dengan 1000
df['realisasi'] = df['realisasi'].astype(float) * 1000000000

# Filtering dengan kondisi yang lebih kompleks
df = df.loc[(df['akun'] == 'PAD') | (df['akun'] == 'Pendapatan Daerah') ]

df = df.drop_duplicates()

df = df.drop(['anggaran', 'persen'], axis=1)

df = df.pivot_table(values='realisasi', index='wil', columns='akun', aggfunc='sum').reset_index()

df['persentage'] = round(df['PAD'] / df['Pendapatan Daerah'] * 100 , 2)

df = df.sort_values('Pendapatan Daerah')

# menampilkan DataFrame
print(df)

########################################################
########################################################
########################################################

# membuat dataset dari dataframe yang telah dibuat
wil = np.array(df['wil'])
x = np.arange(0,len(wil),1)
y1 = np.array(df['PAD'])
y2 = np.array(df['Pendapatan Daerah'])
y3 = np.array(df['persentage'])

# membuat figure dan ax1
fig, ax1 = plt.subplots()

# membuat ax2
ax2 = ax1.twinx()

# membuat bar dan plot
ax1.bar(x, y2,label='Pendapatan Daerah',color='#7DB9B6')
ax1.bar(x, y1,label='PAD',color='#E96479')
ax2.plot(x,y3,'.',label='Persentase',linewidth=1,linestyle='dotted',color='#4D455D')

# membuat anotasi
for x, y in enumerate(y1):
    ax1.annotate('{} T'.format(round(y/1000000000000,2)), xy=(x,y), xytext=(x-0.175,y+50000000000),rotation=90,fontsize=6)

for x, y in enumerate(y2):
    ax1.annotate('{} T'.format(round(y/1000000000000,2)), xy=(x,y), xytext=(x-0.175,y+50000000000),rotation=90,fontsize=6)

# for x, y in enumerate(y3[2:]):
#     ax2.annotate('{} %'.format(round(y)), xy=(x,y), xytext=(x+2+0.125,y),rotation=90,fontsize=8)
# for x, y in enumerate(y3[:2]):
#     ax2.annotate('{} %'.format(round(y)), xy=(x,y), xytext=(x+0.125,y-15),rotation=90,fontsize=8)


# membuat array untuk mengatur jarak titik-titik sumbu
xstep = np.arange(0,len(wil),1)
ax1step = np.arange(0,6000000000000,600000000000)
ax2step = np.arange(0,100,10)

# membuat array untuk mengatur label titik-titik sumbu
xlabel = wil
ax1label = list(map(lambda x: '{} T'.format(round(x/1000000000000,2)), ax1step))
ax2label = list(map(lambda x: '{} %'.format(x), ax2step))

# mengatur jarak titik-titik sumbu axis 1 dan axis 2 menggunakan array yg sudah dibuat
ax1.set_xticks(xstep)
ax1.set_yticks(ax1step)
ax2.set_yticks(ax2step)

# mengatur label titik-titik sumbu axis 1 dan axis 2 menggunakan array yg sudah dibuat
ax1.set_xticklabels(xlabel, rotation=90, fontsize=8)
ax1.set_yticklabels(ax1label, fontsize=8)
ax2.set_yticklabels(ax2label, fontsize=8)

# membuat legends
handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()
handles = handles1 + handles2
labels = labels1 + labels2

plt.legend(handles, labels, loc='upper left', fontsize=8)
plt.title("Kontribusi PAD thd Pendapatan Daerah \n di Kab/Kota seJateng Tahun 2022")
plt.subplots_adjust(left=0.1,right=0.9,top=0.9,bottom=0.25)

# # menampilkan grafik
plt.show()