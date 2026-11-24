"""Program Inventaris & Kasir Toko Kecil (versi GUI Tkinter).

Letakkan file ini satu folder dengan inventaris_toko.py,
karena fungsi logikanya dipakai ulang dari file tersebut.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from inventaris_toko import (
    format_rupiah, tambah_barang, ubah_barang, hapus_barang,
    jual_barang, hitung_total,
)


class AplikasiToko:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventaris & Kasir Toko")
        self.inventaris = {
            "B001": {"nama": "Beras 5kg", "harga": 68000, "stok": 20},
            "B002": {"nama": "Minyak Goreng 1L", "harga": 18000, "stok": 30},
            "B003": {"nama": "Gula 1kg", "harga": 16000, "stok": 25},
        }
        self.keranjang = []
        self.buat_tampilan()
        self.refresh_tabel()

    def buat_tampilan(self):
        form = ttk.LabelFrame(self.root, text="Data Barang", padding=10)
        form.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.entries = {}
        for i, label in enumerate(["Kode", "Nama", "Harga", "Stok"]):
            ttk.Label(form, text=label).grid(row=i, column=0, sticky="w", pady=2)
            entry = ttk.Entry(form, width=25)
            entry.grid(row=i, column=1, pady=2, padx=5)
            self.entries[label] = entry

        tombol = ttk.Frame(form)
        tombol.grid(row=4, column=0, columnspan=2, pady=8)
        ttk.Button(tombol, text="Tambah", command=self.aksi_tambah).grid(row=0, column=0, padx=2)
        ttk.Button(tombol, text="Ubah", command=self.aksi_ubah).grid(row=0, column=1, padx=2)
        ttk.Button(tombol, text="Hapus", command=self.aksi_hapus).grid(row=0, column=2, padx=2)
        ttk.Button(tombol, text="Bersihkan", command=self.bersihkan_form).grid(row=0, column=3, padx=2)

        # Tabel barang
        self.tabel = ttk.Treeview(
            self.root, columns=("kode", "nama", "harga", "stok"),
            show="headings", height=8,
        )
        for kolom, judul, lebar in [("kode", "Kode", 70), ("nama", "Nama", 170),
                                    ("harga", "Harga", 100), ("stok", "Stok", 60)]:
            self.tabel.heading(kolom, text=judul)
            self.tabel.column(kolom, width=lebar)
        self.tabel.grid(row=0, column=1, padx=10, pady=10)
        self.tabel.bind("<<TreeviewSelect>>", self.isi_form_dari_tabel)

        # Keranjang
        kasir = ttk.LabelFrame(self.root, text="Kasir", padding=10)
        kasir.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.list_keranjang = tk.Listbox(kasir, height=5, width=60)
        self.list_keranjang.grid(row=0, column=0, columnspan=3, pady=5)
        ttk.Button(kasir, text="Jual Barang Terpilih",
                   command=self.aksi_jual).grid(row=1, column=0, padx=2)
        ttk.Button(kasir, text="Bayar", command=self.aksi_bayar).grid(row=1, column=1, padx=2)
        self.label_total = ttk.Label(kasir, text="Total: Rp0")
        self.label_total.grid(row=1, column=2, padx=10)

    # Helper
    def refresh_tabel(self):
        self.tabel.delete(*self.tabel.get_children())
        for kode, d in self.inventaris.items():
            self.tabel.insert("", "end", values=(kode, d["nama"],
                              format_rupiah(d["harga"]), d["stok"]))

    def bersihkan_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def isi_form_dari_tabel(self, _event):
        terpilih = self.tabel.selection()
        if not terpilih:
            return
        kode = self.tabel.item(terpilih[0])["values"][0]
        d = self.inventaris[kode]
        self.bersihkan_form()
        self.entries["Kode"].insert(0, kode)
        self.entries["Nama"].insert(0, d["nama"])
        self.entries["Harga"].insert(0, d["harga"])
        self.entries["Stok"].insert(0, d["stok"])

    def baca_form_angka(self, label):
        """Membaca angka dari form; ValueError jika bukan angka bulat."""
        try:
            return int(self.entries[label].get())
        except ValueError:
            raise ValueError(f"{label} harus berupa angka bulat.")

    def kode_terpilih(self):
        terpilih = self.tabel.selection()
        if not terpilih:
            raise ValueError("Pilih barang di tabel terlebih dahulu.")
        return self.tabel.item(terpilih[0])["values"][0]

    # Helper
    def aksi_tambah(self):
        try:
            tambah_barang(self.inventaris, self.entries["Kode"].get(),
                          self.entries["Nama"].get(),
                          self.baca_form_angka("Harga"),
                          self.baca_form_angka("Stok"))
            self.refresh_tabel()
            self.bersihkan_form()
        except ValueError as e:
            messagebox.showerror("Gagal", str(e))

    def aksi_ubah(self):
        try:
            ubah_barang(self.inventaris, self.entries["Kode"].get(),
                        self.baca_form_angka("Harga"),
                        self.baca_form_angka("Stok"))
            self.refresh_tabel()
        except ValueError as e:
            messagebox.showerror("Gagal", str(e))

    def aksi_hapus(self):
        try:
            hapus_barang(self.inventaris, self.entries["Kode"].get())
            self.refresh_tabel()
            self.bersihkan_form()
        except ValueError as e:
            messagebox.showerror("Gagal", str(e))

    def aksi_jual(self):
        try:
            kode = self.kode_terpilih()
            jumlah = simpledialog.askinteger("Jumlah", "Jumlah yang dibeli:",
                                             parent=self.root)
            if jumlah is None:  # dialog dibatalkan
                return
            jual_barang(self.inventaris, self.keranjang, kode, jumlah)
            nama, jml, subtotal = self.keranjang[-1]
            self.list_keranjang.insert(tk.END, f"{nama} x{jml} = {format_rupiah(subtotal)}")
            total, _, _ = hitung_total(self.keranjang)
            self.label_total.config(text=f"Total: {format_rupiah(total)}")
            self.refresh_tabel()
        except ValueError as e:
            messagebox.showerror("Gagal", str(e))

    def aksi_bayar(self):
        if not self.keranjang:
            messagebox.showwarning("Kasir", "Keranjang masih kosong.")
            return
        total, diskon, bayar = hitung_total(self.keranjang)
        messagebox.showinfo(
            "Struk",
            f"Total       : {format_rupiah(total)}\n"
            f"Diskon      : {format_rupiah(diskon)}\n"
            f"Total bayar : {format_rupiah(bayar)}",
        )
        self.keranjang.clear()
        self.list_keranjang.delete(0, tk.END)
        self.label_total.config(text="Total: Rp0")


if __name__ == "__main__":
    root = tk.Tk()
    AplikasiToko(root)
    root.mainloop()
