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

def urun_ekle(imlec):
    
    ad = input("Ürün adı giriniz (iptal için q tuşuna basınız): ")
    if ad == "q":
        return    
    fiyat = float(input("Fiyat giriniz: "))
    stok = int(input("Stok giriniz: "))
    
    imlec.execute("SELECT stok FROM urunler WHERE ad = ?", (ad,))
    sonuc = imlec.fetchone()
    
    if sonuc:
        yeni_stok = sonuc[0] + stok
        imlec.execute("UPDATE urunler SET stok = ? WHERE ad = ?", (yeni_stok, ad))
    else:
        kategori = input("Kategori giriniz: ")
        imlec.execute("INSERT INTO urunler (ad, fiyat, stok, kategori) VALUES (?, ?, ?, ?)", (ad, fiyat, stok, kategori)) 

def urun_listele(imlec):
    imlec.execute("""
        SELECT *
        FROM urunler
    """)
    for urun in imlec.fetchall():
        print(f"{urun[1]} | Fiyat: {urun[2]} | Stok: {urun[3]} | Kategori: {urun[4]}")     

def stok_guncelle(imlec):
    ad = input("Hangi ürünü güncellemek istiyosunuz? (iptal için q tuşuna basınız): ")
    if ad == "q":
        return    
    imlec.execute("""
        SELECT stok
        FROM urunler
        WHERE ad = ?
    """, (ad,))
    sonuc = imlec.fetchone()
    
    if sonuc:
        yeni_stok = int(input("Yeni stok: "))
        imlec.execute("""
            UPDATE urunler
            SET stok = ?
            WHERE ad = ?
        """, (yeni_stok, ad))
        print(f"{ad} stoğu güncellendi!")

    else:
        print(f"{ad} ürünü bulunamadı!")

def urun_sil(imlec):
    ad = input("Hangi ürünü silmek istersiniz? (iptal için q tuşuna basınız): ")
    if ad == "q":
        return    
    imlec.execute("""
        SELECT stok
        FROM urunler
        WHERE ad = ?
    """, (ad,))
    sonuc = imlec.fetchone()
    if sonuc:
        imlec.execute("""
            DELETE FROM urunler
            WHERE ad = ?
        """, (ad,))
        print(f"{ad} ürünü başarıyla silindi!")
    else:
        print(f"Silinecek {ad} ürünü bulunamadı!")   

def istatistik_goster(imlec):
    imlec.execute("""
        SELECT COUNT(*) 
        FROM urunler
    """)
    adet = imlec.fetchone()
    print(f"Toplam ürün sayısı: {adet[0]}")
    
    imlec.execute("SELECT AVG(fiyat) FROM urunler")
    ort = imlec.fetchone()
    print(f"Ortalama fiyat: {ort[0]}")
    
    imlec.execute("SELECT SUM(stok) FROM urunler")
    toplam = imlec.fetchone()
    print(f"Toplam stok: {toplam[0]}")

def kategori_raporu(imlec):
    imlec.execute("""
        SELECT kategori, SUM(stok)
        FROM urunler
        GROUP BY kategori
    """)
    print("=== KATEGORİ RAPORU ===")
    for satir in imlec.fetchall():
        print(f"{satir[0]}: {satir[1]} adet")

while True:
    print("=== ENVANTER SİSTEMİ ===")
    print("1. Ürün ekle")
    print("2. Ürünleri listele")
    print("3. Stok güncelle")
    print("4. Ürün sil")
    print("5. İstatistikler")
    print("6. Kategori Raporu")
    print("7. Çıkış")
    secim = input("Seçiminiz: ")
    
    if secim == "1":
        urun_ekle(imlec)
        baglanti.commit()
    elif secim == "2":
        urun_listele(imlec)
    elif secim == "3":
        stok_guncelle(imlec)
        baglanti.commit()
    elif secim == "4":
        urun_sil(imlec)
        baglanti.commit()
    elif secim == "5":
        istatistik_goster(imlec)  
    elif secim == "6":
        kategori_raporu(imlec)      
    elif secim == "7":
        break
    else:
        print("Geçersiz seçim!")
      
    



baglanti.commit()
baglanti.close()
print("İşlem tamamlandı!")        