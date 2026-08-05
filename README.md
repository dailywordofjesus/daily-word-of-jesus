# Daily Word Of Jesus (static site)

## Struktur folder
```
index.html            → halaman utama (grid, 4 cerita terbaru)
all-articles.html      → galeri semua cerita
styles.css             → semua styling
articles/
  article-template.html   → TEMPLATE kosong, duplikasi ini tiap buat cerita baru
  be-still-and-know.html  → contoh cerita
  the-lost-sheep.html     → contoh cerita
  a-cup-of-water.html     → contoh cerita
  the-lamp-on-the-stand.html → contoh cerita
```

## Cara menambah cerita baru (manual)
1. Di folder `articles/`, copy `article-template.html`, rename sesuai judul,
   misalnya `the-good-samaritan.html`.
2. Buka file barunya, ganti semua teks berikut:
   - `ARTICLE TITLE` → judul cerita
   - `ONE-SENTENCE SUMMARY OF THE STORY.` → ringkasan 1 kalimat (dipakai untuk preview link)
   - `DAY 0XX · MONTH DAY` → nomor hari & tanggal
   - Isi paragraf cerita di bagian `<article class="article-body">`
   - `REPLACE-WITH-YOUR-USERNAME` dan `REPLACE-FILENAME` di URL `og:image`, `og:url`,
     dan link share Facebook → ganti dengan username GitHub & nama file kamu
3. Siapkan 1 gambar preview (ukuran disarankan 1200x630px) untuk cerita itu,
   simpan di folder `assets/` (buat foldernya kalau belum ada), lalu isi
   `og:image` dengan link ke gambar itu. Ini supaya tiap cerita punya gambar
   preview sendiri saat dibagikan ke Facebook/WhatsApp.
4. Buka `index.html` dan `all-articles.html`, copy salah satu blok kartu
   `<a class="card">...</a>`, taruh paling atas di dalam `<div class="grid">`,
   lalu edit tanggal / judul / ringkasan / `href` supaya mengarah ke file
   cerita barumu.
5. Upload semua file (index.html, all-articles.html, styles.css, dan folder
   articles/ + assets/) ke repo GitHub Pages kamu.

## Iklan
Setiap halaman cerita sudah punya slot iklan siap pakai:
```html
<div class="ad-slot"><div class="box">Ad space</div></div>
```
Kalau nanti mau pasang Adsterra, tinggal ganti isi `<div class="box">...</div>`
dengan kode iklannya.

## Tentang desain
- Latar "langit malam" gelap (`--ink`) di header/hero, kartu cerita berwarna
  parchment (kertas krem) supaya terasa seperti membaca sebuah lembar renungan.
- Huruf pertama tiap ringkasan & paragraf pertama cerita dibuat besar berwarna
  emas (drop cap ala manuskrip lama) — elemen ciri khas situs ini.
- Grid otomatis menyesuaikan: 4 kolom di desktop, 2 di tablet, 1 di mobile.
