import sqlite3
baglanti = sqlite3.connect("envanter.db")
imlec = baglanti.cursor()


imlec.execute("""
    CREATE TABLE IF NOT EXISTS urunler(
        id INTEGER PRIMARY KEY,
        ad TEXT UNIQUE,
        fiyat REAL,
        stok INTEGER
    )
""")

while True:
    ad = input("Ürün adı giriniz(çıkmak için q): ")
    if ad == "q":
        break
    fiyat = float(input("Fiyat giriniz: "))
    stok = int(input("Stok giriniz: "))
    
    imlec.execute("SELECT stok FROM urunler WHERE ad = ?", (ad,))
    sonuc = imlec.fetchone()
    
    if sonuc:
        yeni_stok = sonuc[0] + stok
        imlec.execute("UPDATE urunler SET stok = ? WHERE ad = ?", (yeni_stok, ad))
    else:
        imlec.execute("INSERT INTO urunler (ad, fiyat, stok) VALUES (?, ?, ?)", (ad, fiyat, stok))

imlec.execute("""
SELECT *
FROM urunler
""")

for urun in imlec.fetchall():
    print(urun)

baglanti.commit()
baglanti.close()
print("İşlem tamamlandı!")        