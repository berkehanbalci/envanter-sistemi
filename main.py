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
        imlec.execute("INSERT INTO urunler (ad, fiyat, stok) VALUES (?, ?, ?)", (ad, fiyat, stok)) 

def urun_listele(imlec):
    imlec.execute("""
    SELECT *
    FROM urunler
    """)
    for urun in imlec.fetchall():
        print(f"{urun[1]} | Fiyat: {urun[2]} | Stok: {urun[3]}")     

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
    

while True:
    print("=== ENVANTER SİSTEMİ ===")
    print("1. Ürün ekle")
    print("2. Ürünleri listele")
    print("3. Stok güncelle")
    print("4. Ürün sil")
    print("5. Çıkış")
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
        break
    else:
        print("Geçersiz seçim!")
    



baglanti.commit()
baglanti.close()
print("İşlem tamamlandı!")        