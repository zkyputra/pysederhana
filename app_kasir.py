import datetime
from datetime import timedelta

pilihan = 0
keluar = False
sudah_login = False
index = -1

pelanggan = [
  {
    "nama":"Zacky",
    "email":"zacky@gmail.com",
    "password":"zacky1234",
    "saldo":100000000,
    "failed_login":0,
    "transaksi":[]
  }
]

barang = [
  {
    "nama":"Samsung Galaxy M11",
    "harga":1949000,
    "type":"Smartphone",
    "merek":"Samsung"
  },
  {
    "nama":"Samsung Galaxy M21",
    "harga":2995000,
    "type":"Smartphone",
    "merek":"Samsung"
  },
  {
    "nama":"Samsung Galaxy A11",
    "harga":1999000,
    "type":"Smartphone",
    "merek":"Samsung"
  },
  {
    "nama":"OPPO A3s",
    "harga":1421000,
    "type":"Smartphone",
    "merek":"OPPO"
  },
]

voucher = [
  {
    "kode":123456,
    "type":"All",
    "merek":"All",
    "diskon":10,
    "dipakai":False,
    "expired":"2025-06-14 17:25:00"
  },
  {
    "kode":654321,
    "type":"Smartphone",
    "merek":"All",
    "diskon":50,
    "dipakai":False,
    "expired":"2025-12-14 23:25:00"
  },
]

batas_pembayaran_transaksi = 5

def inputAngka(message):
  while True:
    try:
      userInput = int(input(message))
    except ValueError:
      print("Silahkan Masukan Nomor Berupa Angka.")
      continue
    else:
      return userInput
    break

def cekPelanggan(email,password):
  i = 0
  for pl in pelanggan:
    if(str(pl['email']) == str(email) and str(pl['password']) == password):
      return i
    i+=1
  return "Tidak Ada"

def failedLogin(email):
  i = 0
  for pl in pelanggan:
    if(str(pl['email']) == str(email)):
      pelanggan[i]['failed_login'] += 1
      return pl['failed_login']
    i += 1
  return 0

def cekVoucher(kode):
  i = 0
  for vc in voucher:
    if vc['kode'] == kode:
      return i
    i+=1
  return "Tidak Ada"

def tampilkanBarang():
  no = 1
  print("")
  print("")
  print("======== DATA BARANG =========")
  for b in barang:
    print("=================")
    print("No :",no)
    print("Nama : ",b['nama'])
    print("Merek : ",b['merek'])
    print("Type : ",b['type'])
    print("Harga : Rp.",b['harga'])
    print("=================")
    no += 1
  print("")
  print("No "+str(no)+" : Keluar")
  print("")
  beliBarang(no)

def beliBarang(no):
  plh_brg = inputAngka("Pilih Nomor Barang : ")
  if(plh_brg == no):
    print("")
  else:
    b = barang[plh_brg-1]
    print("========= Beli Barang ========")
    print("Nama : ",b['nama'])
    print("Merek : ",b['merek'])
    print("Type : ",b['type'])
    print("Harga : Rp.",b['harga'])
    print("==============================")
    print("1.Beli")
    print("2.Masukan Kode Voucher")
    print("3.Kembali")
    plh_mn = inputAngka("Pilih Nomor Barang : ")
    if(plh_mn == 1):
      if(b['harga'] > pelanggan[index]['saldo']):
        print("Saldo Anda Tidak Cukup")
      else:
        trans = {
          "barang":b,
          "total":b['harga'],
          "batas_waktu":datetime.datetime.now()+timedelta(minutes=batas_pembayaran_transaksi),
          "status":"Belum Dibayar"
        }
        pelanggan[index]['saldo'] -= b['harga']
        print("==============================")
        print("Anda Sudah Membeli : ")
        print("Nama : ",b['nama'])
        print("Dengan Harga : Rp.",b['harga'])
        print("Silahkan Bayar Tagihan Sebelum ",trans['batas_waktu'])
        print("==============================")
        pelanggan[index]['transaksi'].append(trans)
    elif(plh_mn == 2):
      kd_vcr = inputAngka("Masukan Kode Vocher : ")
      cek = cekVoucher(kd_vcr)
      if(cek != "Tidak Ada"):
        if(voucher[cek]['dipakai']):
          print("==============================")
          print("Voucher Sudah Tidak Tersedia Atau Sudah Di Gunakan")
          print("==============================")
          print("")
          print("")
        # elif(datetime.datetime.strptime(voucher[cek]['expired'], '%Y-%m-%d %H:%M:%S')):
        #   print("==============================")
        #   print("Masa Berlaku Voucher Sudah Habis")
        #   print("==============================")
        #   print("")
        #   print("")
        elif(voucher[cek]['merek'] != "All" and voucher[cek]['merek'] != b['merek']):
          print("==============================")
          print("Voucher Tidak Bisa Di Gunakan Untuk Barang Ini")
          print("==============================")
          print("")
          print("")
        else:
          potongan = b['harga'] * (voucher[cek]['diskon']/100)
          pelanggan[index]['saldo'] -= (b['harga']-potongan)
          trans = {
          "barang":b,
          "total":(b['harga']-potongan),
          "batas_waktu":datetime.datetime.now()+timedelta(minutes=5),
          "status":"Belum Dibayar"
          }
          print("==============================")
          print("Anda Sudah Membeli : ")
          print("Nama : ",b['nama'])
          print("Dengan Harga : Rp.",b['harga'])
          print("Anda Juga Mendapat Potongan Sebesar "+str(voucher[cek]['diskon']))
          print("Total Harga : Rp.",(b['harga']-potongan))
          print("Silahkan Bayar Tagihan Sebelum ",trans['batas_waktu'])
          print("==============================")
          voucher[cek]['dipakai'] = True
          pelanggan[index]['transaksi'].append(trans)
      else:
        print("Voucher Tidak Di Temukan")
    print("")
    print("")

def tampilkanTransaksi():
  no = 1
  print("")
  print("")
  print("======== DATA TRANSAKSI =========")
  for t in pelanggan[index]['transaksi']:
    print("=================")
    print("No :",no)
    print("Nama : ",t['barang']['nama'])
    print("Merek : ",t['barang']['merek'])
    print("Type : ",t['barang']['type'])
    print("Total : Rp.",t['total'])
    print("Status : ",t['status'])
    print("Batas Waktu : ",t['batas_waktu'])
    print("=================")
    no += 1
  print("")
  print("No "+str(no)+" : Keluar")
  print("")
  bayarTransaksi(no)

def bayarTransaksi(no):
  plh_trans = inputAngka("Pilih Nomor Transaksi : ")
  print("")
  print("")
  if(plh_trans == no):
    print("")
  else:
    trans = pelanggan[index]['transaksi'][(plh_trans - 1)]
    if(trans['batas_waktu'] < datetime.datetime.now()):
      print("")
      print("")
      print("====================")
      print("Transaksi Sudah Melebihi Batas Yang Di Tentukan Maka Transaksi Di Anulir")
      print("====================")
    elif(trans['status'] == "Sudah Dibayar"):
      print("====================")
      print("Transaksi Sudah Di Bayar")
      print("====================")
    else:
      print("====================")
      print("Berhasil Membayar Transaksi Sebesar : ",trans['total'])
      pelanggan[index]['saldo'] -= trans['total']
      print("====================")
  print("")
  print("")

while keluar == False:
  if(sudah_login == False):
    print("======== SELAMAT DATANG DI GOOD-PHONE =======")
    print("1.Login Sebagai Pelanggan")
    print("2.Keluar")
    pilihan = inputAngka("Pilihan : ")
    if(pilihan == 1):
      email = input("Email : ")
      password = input("Password : ")
      if(failedLogin(email) >= 3):
        print("Akun Di Banned")
      cek = cekPelanggan(email,password)
      if(cek == "Tidak Ada"):
        print("Email atau password salah")
        sudah_login = False
      else:
        sudah_login = True
        index = cek
    elif(pilihan == 2):
      keluar = True
      break
    else:
      print("Pilihan Tidak Tersedia")
  elif (sudah_login == True):
    if(pilihan == 1):
      print("======== SELAMAT DATANG DI GOOD-PHONE =======")
      print("=================================")
      print("Selamat Datang : ",pelanggan[index]['nama'])
      print("Saldo Anda : ",pelanggan[index]['saldo'])
      print("=================================")
      print("1.Beli Barang")
      print("2.Lihat Transaksi")
      print("3.Logout")
      print("4.Keluar")
      pilihan_pelanggan = inputAngka("Pilihan : ")
      if(pilihan_pelanggan == 1):
        tampilkanBarang()
      elif(pilihan_pelanggan == 2):
        tampilkanTransaksi()
      elif(pilihan_pelanggan == 3):
        sudah_login = False
      elif(pilihan_pelanggan == 4):
        keluar = False
        break
