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
imlec.execute("""
    CREATE TABLE IF NOT EXISTS kategoriler(
        id INTEGER PRIMARY KEY,
        ad TEXT UNIQUE
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
        kategori_adi = input("Kategori giriniz: ")
        imlec.execute("""
            SELECT id
            FROM kategoriler
            WHERE ad = ?
        """, (kategori_adi,))
        kategori_sonuc = imlec.fetchone()
        
        if kategori_sonuc:
            kategori_id = kategori_sonuc[0]
            imlec.execute("INSERT INTO urunler (ad, fiyat, stok, kategori_id) VALUES (?, ?, ?, ?)",(ad, fiyat, stok, kategori_id))
        else:
            print(f"{kategori_adi} kategorisi bulunamadı! Önce kategoriler tablosuna eklenmeli.")

def urun_listele(imlec):
    imlec.execute("""
        SELECT urunler.ad, urunler.fiyat, urunler.stok, kategoriler.ad
        FROM urunler
        JOIN kategoriler ON urunler.kategori_id = kategoriler.id
    """)
    for urun in imlec.fetchall():
        print(f"{urun[0]} | Fiyat: {urun[1]} | Stok: {urun[2]} | Kategori: {urun[3]}")     

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
        SELECT kategoriler.ad, SUM(urunler.stok)
        FROM urunler
        JOIN kategoriler ON urunler.kategori_id = kategoriler.id
        GROUP BY kategoriler.ad
        ORDER BY SUM(urunler.stok) DESC
    """)
    print("=== KATEGORİ RAPORU ===")
    for satir in imlec.fetchall():
        print(f"{satir[0]}: {satir[1]} adet")

def kategori_ekle(imlec):
    ad = input("Yeni kategori adı girininiz (iptal için q tuşuna basınız): ")
    if ad == "q":
        return

    imlec.execute("""
        SELECT id
        FROM kategoriler
        WHERE ad = ?
    """, (ad,))
    sonuc = imlec.fetchone()    

    if sonuc:
        print(f"{ad} kategorisi zaten var!")
    else:
        imlec.execute("INSERT INTO kategoriler (ad) VALUES (?)", (ad,))
        print(f"{ad} kategorisi eklendi")

while True:
    print("=== ENVANTER SİSTEMİ ===")
    print("1. Kategori ekle")
    print("2. Ürün ekle")
    print("3. Ürünleri listele")
    print("4. Stok güncelle")
    print("5. Ürün sil")
    print("6. İstatistikler")
    print("7. Kategori Raporu")
    print("8. Çıkış")
    secim = input("Seçiminiz: ")
    
    if secim == "1":
        kategori_ekle(imlec)
        baglanti.commit()
    elif secim == "2":
        urun_ekle(imlec)
        baglanti.commit()
    elif secim == "3":
        urun_listele(imlec)
    elif secim == "4":
        stok_guncelle(imlec)
        baglanti.commit()
    elif secim == "5":
        urun_sil(imlec)
        baglanti.commit()
    elif secim == "6":
        istatistik_goster(imlec)
    elif secim == "7":
        kategori_raporu(imlec)      
    elif secim == "8":
        break
    else:
        print("Geçersiz seçim!")
      
    
baglanti.commit()
baglanti.close()
print("İşlem tamamlandı!")        