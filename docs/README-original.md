# Pasaparola Arena

Türkçe / English kelime oyunu. Vanilla oyun arayüzü `web/index.html` ve `public/game.js` içinde; Vinext kök route HTML döndürür. Günlük mücadele `/api/daily` ve D1 kullanır.

- Soru kaynağı: content TSV dosyaları; `python scripts/build-content.py` iki soru çıktısını günceller.
- Testler: `node scripts/test-game.cjs` ve `node scripts/test-daily.mjs`.
- Şema: db/schema.ts. Değişikliklerde `npm run db:generate`; DDL istek sırasında çalıştırılmaz.
- Yerel oyun kayıtları, cüzdan ve yıldızlar localStorage içindedir. Tarayıcı verilerini temizlemek bu kayıtları siler. Yerel çok oyunculu oyun cihazın ortak cüzdanını kullanır.
- Günlük tur: İstanbul günü, 26 karma İngilizce soru, 300 saniye, cihaz çerezi başına tek deneme. Başlanan turun süresi sayfa kapalıyken de akar. Ortak sıralamaya katılım sonuçta açık yayımla düğmesiyledir. Cihaz çerezini silmeye karşı hesap tabanlı kimlik doğrulaması yoktur; rekabet arkadaşça kullanım içindir.
- Cümle ipucu İngilizce modundadır, 150 cüzdan puanı harcar; günlük turda yalnız o turda kazanılan cüzdan kullanılır. Diğer ipuçları soru puanını bir kez yarıya indirir.
- Otomatik kontroller DOM simülasyonu ve SQLite API testleridir. Gerçek iPhone Safari üzerinde test yapılmadı.

## Arena 5

Ana menü dört giriş içerir. Oyun kurulumu kişi → dil → mod adımlarını izler; süre/seviye/insaflı mod Ayarlar bölümünde saklanır. Can seçimi yalnız Survival'da görünür.

Kelime varlıkları `content/enrichment/*-output.json` dosyalarındadır. Derleyici aynı kelimenin eski seviye üyeliklerini `levels` dizisinde korur ve her dilde benzersiz kelimeleri sayar. Hedef: Türkçe 1500, İngilizce 2500. Türkçe örnek ve İngilizce karşılıkları da desteklenir. Eş/yakın anlamlı ipucu 200, cümle ipucu 150 puandır; uygun eş anlamlı yoksa ücret alınmaz.

`arena4_totals_v5` eski kayıtları bir kez içe aktarır ve yerel/çevrim içi toplamları ayrı biriktirir. Eski boş sorularda pas ayrımı bulunmadığından bu rakamlar pas sayısına uydurularak eklenmez. Yeni kayıtlar pas ve cevaplanmamış soruları ayrı tutar. Maksimum puan ve doğru rekoru oyuncu turu başınadır. Tekrar turları puan, cüzdan ve istatistiğe dahil değildir. Günlük tur tamamlanınca sunucu cevap incelemesini gönderir; devam eden tur için cevap anahtarı gönderilmez.
