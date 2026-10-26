# MGLMUN'26 sitesi — kurulum (ücretsiz, ~15 dakika)

Klasördekiler:
- `index.html` — site (ana sayfa, komiteler, ekip, program, SSS, başvuru formları)
- `admin.html` — admin paneli (başvuruları görme, durum değiştirme, CSV indirme)
- `config.js` — Supabase bağlantı bilgileri (sen dolduracaksın)
- `schema.sql` — veritabanı tablosu ve güvenlik kuralları
- `logo.jpg`

## 1) Supabase (veritabanı)

1. https://supabase.com → giriş yap → **New project**. Ad: `mglmun26`, bölge: Frankfurt (eu-central-1). Şifreyi bir yere not et.
2. Proje açılınca sol menü **SQL Editor → New query** → `schema.sql` dosyasının tamamını yapıştır.
3. En alttaki satırın başındaki `--` işaretini sil ve kendi e-postanı yaz. Birden fazla admin olacaksa her biri için bir satır ekle:
   ```sql
   insert into public.admins (email) values ('senin@mailin.com');
   insert into public.admins (email) values ('arya@mailin.com');
   ```
   → **Run**. "Success" görmelisin.
4. **Authentication → Users → Add user → Create new user**: aynı e-posta + güçlü bir şifre, **Auto Confirm User** işaretli.
   (Her admin için tekrarla. Herkes farklı ve güçlü şifre kullansın.)
5. **Authentication → Sign In / Providers → Email**: "Allow new users to sign up" seçeneğini **kapat**. (Yabancıların hesap açmasını engeller; panel zaten sadece admins tablosundakilere açık.)
6. **Project Settings → API** (veya Data API): **Project URL** ve **anon / publishable key**'i kopyala.
   `service_role` / `secret` anahtarını **asla** kullanma.

## 2) config.js

`config.js` dosyasını aç, iki değeri yapıştır:
```js
SUPABASE_URL: "https://xxxxxxxx.supabase.co",
SUPABASE_ANON_KEY: "eyJ...  veya  sb_publishable_..."
```

## 3) Cloudflare Pages → mglmun26.pages.dev

1. https://dash.cloudflare.com → ücretsiz hesap aç / giriş yap.
2. Sol menü **Workers & Pages → Create → Pages → Upload assets** (Direct Upload).
3. Proje adı: **mglmun26** → Create project.
4. Bu klasörün **içindekileri** (index.html, admin.html, config.js, logo.jpg) sürükle bırak → **Deploy site**.
5. Site: **https://mglmun26.pages.dev** · Admin: **https://mglmun26.pages.dev/admin.html**

İsim alınmışsa Cloudflare farklı bir ad önerir (ör. mglmun26-abc.pages.dev); proje adını değiştirerek dene.

Güncelleme: dosyayı değiştir → Cloudflare'de projeye gir → **Create deployment** → klasörü tekrar yükle.

## 4) Test

1. Siteden kendi adınla bir delege başvurusu yap → "Application received" ekranı gelmeli.
2. `/admin.html` → giriş yap → başvuru listede görünmeli. Tıklayınca detay açılır, durumu Kabul/Red yapıp kaydedebilirsin.
3. Gerçek başvurular açılmadan önce test başvurusunu Supabase → Table Editor → applications'tan sil.

## Notlar
- Başvuru formu herkese açık ama veriler **sadece admins tablosundaki e-postalarla giriş yapanlara** görünür.
- Supabase ücretsiz projeleri uzun süre hiç kullanılmazsa duraklatılabilir; panelden tek tıkla tekrar açılır.
- Formda T.C. kimlik no istenmiyor; gerekiyorsa ayrıca konuşalım.
