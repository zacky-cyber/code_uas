"""
Materi yang diterapkan:
1. Struktur data  : dictionary (inventaris), list (keranjang), tuple (item keranjang)
2. Fungsi         : tambah, ubah, hapus, jual, hitung diskon, dst.
3. Pengkondisian  : validasi input, cek stok, penentuan diskon
4. Perulangan     : menu utama dan menampilkan data
5. Error handling : try-except untuk input tidak valid
"""

DISKON_BESAR = 500_000   # belanja >= 500 ribu -> diskon 10%
DISKON_SEDANG = 200_000  # belanja >= 200 ribu -> diskon 5%


# ---------------------------------------------------------------------------
# Fungsi-fungsi logika (dipakai juga oleh versi GUI)
# ---------------------------------------------------------------------------
def format_rupiah(angka):
    """Mengubah angka menjadi format rupiah, contoh: Rp15.000"""
    return "Rp" + f"{angka:,.0f}".replace(",", ".")


def tambah_barang(inventaris, kode, nama, harga, stok):
    """Menambahkan barang baru. Melempar ValueError jika data tidak valid."""
    kode = kode.strip().upper()
    nama = nama.strip()
    if not kode or not nama:
        raise ValueError("Kode dan nama barang tidak boleh kosong.")
    if kode in inventaris:
        raise ValueError(f"Kode {kode} sudah terdaftar.")
    if harga <= 0:
        raise ValueError("Harga harus lebih dari 0.")
    if stok < 0:
        raise ValueError("Stok tidak boleh negatif.")
    inventaris[kode] = {"nama": nama, "harga": harga, "stok": stok}


def ubah_barang(inventaris, kode, harga=None, stok=None):
    """Mengubah harga dan/atau stok barang yang sudah ada."""
    kode = kode.strip().upper()
    if kode not in inventaris:
        raise ValueError(f"Kode {kode} tidak ditemukan.")
    if harga is not None:
        if harga <= 0:
            raise ValueError("Harga harus lebih dari 0.")
        inventaris[kode]["harga"] = harga
    if stok is not None:
        if stok < 0:
            raise ValueError("Stok tidak boleh negatif.")
        inventaris[kode]["stok"] = stok


def hapus_barang(inventaris, kode):
    """Menghapus barang dari inventaris."""
    kode = kode.strip().upper()
    if kode not in inventaris:
        raise ValueError(f"Kode {kode} tidak ditemukan.")
    del inventaris[kode]


def jual_barang(inventaris, keranjang, kode, jumlah):
    """Memasukkan barang ke keranjang dan mengurangi stok.

    Setiap item keranjang berupa tuple: (nama, jumlah, subtotal).
    """
    kode = kode.strip().upper()
    if kode not in inventaris:
        raise ValueError(f"Kode {kode} tidak ditemukan.")
    if jumlah <= 0:
        raise ValueError("Jumlah harus lebih dari 0.")
    barang = inventaris[kode]
    if jumlah > barang["stok"]:
        raise ValueError(f"Stok tidak cukup. Sisa stok: {barang['stok']}.")
    barang["stok"] -= jumlah
    keranjang.append((barang["nama"], jumlah, barang["harga"] * jumlah))


def hitung_diskon(total):
    """Menghitung diskon berdasarkan total belanja."""
    if total >= DISKON_BESAR:
        return total * 0.10
    elif total >= DISKON_SEDANG:
        return total * 0.05
    return 0


def hitung_total(keranjang):
    """Menghitung total, diskon, dan total bayar. Mengembalikan tuple."""
    total = sum(subtotal for _, _, subtotal in keranjang)
    diskon = hitung_diskon(total)
    return total, diskon, total - diskon


# ---------------------------------------------------------------------------
# Fungsi tampilan & input (khusus terminal)
# ---------------------------------------------------------------------------
def baca_angka(pesan):
    """Meminta input angka bulat sampai pengguna memasukkan nilai yang valid."""
    while True:
        try:
            return int(input(pesan))
        except ValueError:
            print("Input tidak valid, masukkan angka bulat.")


def tampilkan_barang(inventaris):
    """Menampilkan seluruh barang dalam bentuk tabel."""
    if not inventaris:
        print("Inventaris masih kosong.")
        return
    print(f"\n{'Kode':<8}{'Nama':<22}{'Harga':>12}{'Stok':>8}")
    print("-" * 50)
    for kode, data in inventaris.items():
        print(f"{kode:<8}{data['nama']:<22}"
              f"{format_rupiah(data['harga']):>12}{data['stok']:>8}")


def menu_tambah(inventaris):
    kode = input("Kode barang : ")
    nama = input("Nama barang : ")
    harga = baca_angka("Harga       : ")
    stok = baca_angka("Stok        : ")
    tambah_barang(inventaris, kode, nama, harga, stok)
    print("Barang berhasil ditambahkan.")


def menu_ubah(inventaris):
    kode = input("Kode barang yang diubah : ")
    harga = baca_angka("Harga baru : ")
    stok = baca_angka("Stok baru  : ")
    ubah_barang(inventaris, kode, harga, stok)
    print("Data barang berhasil diubah.")


def menu_hapus(inventaris):
    kode = input("Kode barang yang dihapus : ")
    hapus_barang(inventaris, kode)
    print("Barang berhasil dihapus.")


def menu_transaksi(inventaris):
    keranjang = []
    while True:
        tampilkan_barang(inventaris)
        kode = input("\nKode barang (kosongkan untuk bayar): ")
        if kode.strip() == "":
            break
        jumlah = baca_angka("Jumlah : ")
        try:
            jual_barang(inventaris, keranjang, kode, jumlah)
            print("Masuk keranjang.")
        except ValueError as e:
            print(f"Gagal: {e}")

    if not keranjang:
        print("Keranjang kosong, transaksi dibatalkan.")
        return

    print("\n===== STRUK =====")
    for nama, jumlah, subtotal in keranjang:
        print(f"{nama:<22} x{jumlah:<4}{format_rupiah(subtotal):>12}")
    total, diskon, bayar = hitung_total(keranjang)
    print("-" * 40)
    print(f"{'Total':<28}{format_rupiah(total):>12}")
    print(f"{'Diskon':<28}{format_rupiah(diskon):>12}")
    print(f"{'Total bayar':<28}{format_rupiah(bayar):>12}")


def main():
    inventaris = {
        "B001": {"nama": "Beras 5kg", "harga": 68000, "stok": 20},
        "B002": {"nama": "Minyak Goreng 1L", "harga": 18000, "stok": 30},
        "B003": {"nama": "Gula 1kg", "harga": 16000, "stok": 25},
    }
    aksi = {
        "1": tampilkan_barang,
        "2": menu_tambah,
        "3": menu_ubah,
        "4": menu_hapus,
        "5": menu_transaksi,
    }

    while True:
        print("\n=== INVENTARIS & KASIR TOKO ===")
        print("1. Lihat barang")
        print("2. Tambah barang")
        print("3. Ubah harga/stok")
        print("4. Hapus barang")
        print("5. Transaksi penjualan")
        print("0. Keluar")
        pilihan = input("Pilih menu: ").strip()

        if pilihan == "0":
            print("Terima kasih!")
            break
        elif pilihan in aksi:
            try:
                aksi[pilihan](inventaris)
            except ValueError as e:
                print(f"Gagal: {e}")
        else:
            print("Menu tidak tersedia.")


if __name__ == "__main__":
    main()
