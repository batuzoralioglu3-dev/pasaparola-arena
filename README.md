# Pasaparola Arena — kaynak kod arşivi

Son yayımlanan çalışan sürümün tam kaynaklarıdır. Kaynak commit: `9931c328e0508ea2bd0be4443b96968f7cc80775`. Bu arşiv hazırlanırken oyunun kodu ve canlı site değiştirilmedi.

## Kurulum ve yerel çalıştırma

Node.js 24, pnpm 11.25.0 kullanın. Kelime derleyicisi için Python 3 gereklidir. Paketlerin ilk kurulumu internet gerektirir.

```sh
corepack enable
corepack prepare pnpm@11.25.0 --activate
pnpm install --frozen-lockfile
pnpm build
```

Tam uygulama günlük mücadele için yerel D1 veritabanına ihtiyaç duyar. İlk kurulumda, proje kökünde aşağıdaki komutu bir kez çalıştırın:

```sh
pnpm exec wrangler d1 execute DB --local --config dist/server/wrangler.json --persist-to .wrangler/state --file drizzle/0000_previous_mongu.sql
pnpm start
```

Terminalde yazılan yerel adresi tarayıcıda açın. Migration SQL komutunu aynı veritabanında tekrar çalıştırmayın; tablolar zaten oluşturulmuş olur. `pnpm start` derlenmiş uygulamayı yerel Workers ortamında çalıştırır. Hot reload geliştirmesi için `pnpm dev` kullanılabilir; varsayılan port 5173'tür. Günlük mücadele API'sini denemek için yukarıdaki build + veritabanı + start akışını kullanın.

## Dosyalar

- `web/index.html`: HTML, oyun CSS'i ve gömülü ikonlar.
- `public/game.js`: oyun, ekran geçişleri, yerel kayıtlar ve istatistikler.
- `content/questions.json` ve `public/questions.js`: tam 4.000 kelime (1.500 benzersiz Türkçe, 2.500 benzersiz İngilizce).
- `content/base.json`, TSV dosyaları ve `content/enrichment/`: kelime üretiminde kullanılan kaynaklar; eski sürüm kopyaları değildir. Seviye üyelikleri `levels` alanında korunur.
- `scripts/build-content.py`: kaynaklardan iki soru çıktısını üretir. Çalıştırma: `python3 scripts/build-content.py`.
- `app/`, `lib/`, `db/`, `drizzle/`: sayfa sunumu, günlük mücadele API'si, kurallar, veritabanı şeması ve migration.
- `public/*.svg`: görseller. HTML içindeki base64 PNG ve SVG ikonlar da kaynakta korunmuştur. Ayrı ses efekti veya özel font dosyası yoktur; sistem fontları kullanılır.
- `build/`, `vendor/`, yapılandırma dosyaları, paket kilidi ve yardımcı scriptler: derleme ve çalışma altyapısı; silmeyin. Üçüncü taraf lisans dosyaları korunmuştur.

## Kontroller

Proje kökünden, bağımlılıkları yükledikten sonra:

```sh
node scripts/test-content-export.cjs
node scripts/test-game.cjs
node scripts/test-daily.mjs
pnpm build
```

İçerik testi benzersiz sayıları, açıklama/çeviri alanlarını, eski kelime ve seviye üyeliklerinin korunmasını, boşluklu ipucunda cevabın gizlenmesini denetler. Oyun testi 1.497 akış kontrolü içerir. Günlük mücadele testi SQLite üzerinde API yaşam döngüsünü, skorları ve ipuçlarını doğrular. Bunlar otomatik kod ve DOM simülasyonu testleridir; gerçek iPhone Safari cihaz testi yerine geçmez.

Özgün `scripts/test-content.cjs`, önceki Git commit'ine başvurur. ZIP Git geçmişi taşımadığından, arşiv için aynı kontrolleri `tests/fixtures/preserved-word-levels.json` içindeki yalnızca kelime/seviye referanslarıyla yapan `test-content-export.cjs` eklenmiştir. Eski oyun sürümü arşive dahil edilmemiştir.

## Harici servisler ve başka bir sunucuya taşıma

Uygulama Vinext/Vite, React ve Cloudflare Workers araç zincirini kullanır; sürümler `package.json` ve `pnpm-lock.yaml` içindedir. Günlük mücadele ve ortak skor tablosu sunucuda Cloudflare D1'in `DB` binding'ine ihtiyaç duyar. Yerel çalıştırmada Wrangler D1'i taklit eder; Cloudflare hesabı veya API anahtarı gerekmez. Gerçek sunucuda kendi D1 veritabanınızı oluşturup şemayı uygulamalı ve hosting yapılandırmasını uyarlamalısınız.

GitHub kaynak saklama ve geliştirme için uygundur. GitHub Pages tek başına bu sunucu API'sini/D1'i çalıştırmaz. Başka altyapıya taşırken `vite.config.ts`, `build/` ve `db/` içindeki Workers/Sites bağlantılarını hedefinize uyarlayın. `.openai/hosting.json` mevcut projenin gizli olmayan kimlik bilgisini ve binding adını korur; yeni proje yayımlamak için mevcut site kimliğini kullanmayın. Bu arşiv yayımlama işlemi yapmaz.

Sites bağlayıcı/kimlik doğrulama yardımcıları altyapı kaynaklarının parçası olarak korunmuştur. Kelime oyunu bir yapay zekâ API'si veya OpenAI API anahtarı gerektirmez. Kelimeler arşiv içinde yereldir; oyun sırasında bir sözlük servisine bağımlı değildir.

## Veriler ve güvenlik

Oyun geçmişi, yıldızlanan kelimeler, ayarlar ve yerel istatistikler oyuncunun tarayıcısındaki localStorage'da tutulur; kaynak kodun parçası değildir. Yeni alan adına kendiliğinden taşınmazlar. Canlı D1 kayıtları/oyuncu skorları da bu kaynak arşivine dahil değildir; şema ve migration dahildir.

Arşivde `.git`, `node_modules`, derlenmiş çıktılar, yerel veritabanı, önbellek, ortam değişkeni dosyaları veya kimlik bilgileri bulunmaz. Bağımlılıklar kilit dosyasıyla yeniden yüklenir. Gerçek hesap anahtarlarını GitHub'a göndermeyin; `.gitignore` ortam dosyalarını dışlar.

`docs/README-original.md` yayımlanan sürümün özgün notlarını korur; bu belgedeki kurulum ve ipucu kapsamı daha günceldir. Cümle ipucu iki dilde de desteklenir. `SOURCE-MANIFEST.sha256` arşivdeki dosyaların bütünlük listesidir.
