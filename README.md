# UAS-PBO-Semester2
UAS-PBO, Kelompok 4, anggota kelompok:
1. Natasya Salsabilla   (G1A022023)
2. Alif Nurhidayat      (G1A022073)
3. Saniyyah Zhafirah    (G1A022081)

## Tampilan Program (Menu Utama)
![](https://github.com/KillerKing93/UAS-PBO-Semester2/blob/main/Gambar%20Program/Menu%20Utama.png)

Pada menu ini, pengguna dapat memilih antara 2 pilihan, yaitu menuju ke laman pengguna biasa, dimana pengguna dapat membeli barang, atau menuju ke lama pengguna admin, dimana pengguna dapat mengakses alat - alat yang hanya dimiliki oleh pengguna admin.
## Tampilan Menu Pengguna Biasa
![](https://github.com/KillerKing93/UAS-PBO-Semester2/blob/main/Gambar%20Program/Menu%20Pengguna%20Biasa.png)

Pada menu ini, pengguna dapat memilih barang yang ingin dibeli kemudian pengguna dapat memfinalisasikan pembelian dengan menekan tombol Finalkan Pembelian dan pembeli pun akan diperlihatkan dengan widget yang akan menampilkan informasi barang yang dibeli oleh pembeli
## Widget Ketika Pembeli Memfinalisasikan Pembelian.
![](https://github.com/KillerKing93/UAS-PBO-Semester2/blob/main/Gambar%20Program/Menu%20Beli%20Pengguna%20Biasa.png)

Widget akan muncul ketika tombol finalkan pembelian ditekan. Pengguna dapat melihat informasi terkait dengan barang yang dibeli oleh pengguna dari widget ini
## Tampilan Menu Login.
![](https://github.com/KillerKing93/UAS-PBO-Semester2/blob/main/Gambar%20Program/Menu%20Login.png)

Menu yang berfungsi untuk membatasi akses antara pengguna biasa sehingga pengguna biasa tidak dapat mengakses menu pengguna administrasi (admin)
## Tampilan Menu Admin.
![](https://github.com/KillerKing93/UAS-PBO-Semester2/blob/main/Gambar%20Program/Menu%20Admin.png)

Menu admin berfungsi sebagai media interaksi antara pengguna admin dengan data - data dan informasi yang ada di dalam program. Pengguna admin dapat mengubah sandi admin file program, menambahkan barang ke dalam program, mengubah barang di dalam program, dan menghapus barang dari dalam program.
## Tampilan Menu Ganti Sandi Pengguna Admin.
![](https://github.com/KillerKing93/UAS-PBO-Semester2/blob/main/Gambar%20Program/Menu%20Ganti%20Kata%20Sandi%20Pengguna%20Admin.png)

Menu yang berfungsi untuk mengganti sandi pengguna admin. Jika sandi pengguna admin saat ini yang dimasukkan salah, maka pengguna tidak dapat mengganti sandi pengguna admin, jika sandi baru yang dimasukkan berbeda dengan sandi baru yang dimasukkan kembali, maka pengguna tidak dapat mengganti sandi pengguna admin. Jika semua kategori ini tidak terpenuhi, maka pengguna akan dengan sukses mengganti sandi pengguna admin.
## Tampilan Menu Tambah Barang
![](https://github.com/KillerKing93/UAS-PBO-Semester2/blob/main/Gambar%20Program/Menu%20Menambah%20Barang.png)

Menu yang berfungsi sebagai media interaksi pengguna admin agar dapat menambah barang baru ke dalam program
## Tampilan Menu Mengganti Detail Barang
![](https://github.com/KillerKing93/UAS-PBO-Semester2/blob/main/Gambar%20Program/Menu%20Mengganti%20Detail%20Barang.png)

Menu yang berfungsi sebagai media interaksi pengguna admin sehingga pengguna admin dapat mengganti detail barang yang ada di dalam program
## Tampilan Menu Menghapus Barang
![](https://github.com/KillerKing93/UAS-PBO-Semester2/blob/main/Gambar%20Program/Menu%20Untuk%20Menghapus%20Barang.png)

Menu yang berfungsi sebagai media interaksi pengguna admin agar pengguna admin dapat menghapus barang yang ada di dalam program
## Widget ketika Pengguna Admin Memfinalisasikan Pembelian
![](https://github.com/KillerKing93/UAS-PBO-Semester2/blob/main/Gambar%20Program/Menu%20Beli%20Pengguna%20Admin.png)

Widget akan muncul ketika pengguna admin menekan tombol Finalisasikan Pembelian, dan pengguna admin dapat melihat informasi yang terkait dengan barang yang dibeli olehnya.
## Gambar Cetak Nota Pembelian
![](https://github.com/KillerKing93/UAS-PBO-Semester2/blob/main/Gambar%20Program/Nota%20Pembelian.png)

Bentuk nota yang akan dihasilkan jika pengguna user maupun pengguna admin menyimpan nota barang yang mereka beli

## Penjelasan Penerapan Object-Oriented Programming pada Program yang Dibuat
Pada program ini, Object-Oriented Programming sangat berperan dalam pembuatan program, sehingga banyak objek dapat dibuat dari sebuah kelas. Contohnya:
| Nama Kelas | Objek yang dihasilkan | Kegunaannya |
| --- | --- | --- |
| Kelas PrintText() | order | Berfungsi untuk mencetak barang yang dibeli oleh pengguna |
| Kelas ItemNodes() | objek yang disimpan ke dalam kelas ItemsCore() | Berfungsi untuk menyimpan data - data barang ke dalam media penyimpanan yang mudah diolah |
| Kelas ItemsCore() | self.IC | Berfungsi sebagai pengolah utama data - data dan informasi barang yang ada di dalam program. Objek ini sangat kritikal bagi kerja program ini karena tanpa kelas ini, program tidak akan tahu bagaimana cara menyimpan serta mengolah data - data dan informasi barang yang ada. |
