import streamlit as st
from datetime import datetime, date

# ==========================
# LINKED LIST NODE & CLASS
# ==========================

class NodeBuku:
    def __init__(self, id_buku, judul, pengarang, status="Tersedia", dipinjam_oleh="-", tgl_kembali="-"):
        self.id_buku = id_buku
        self.judul = judul
        self.pengarang = pengarang
        self.status = status          # "Tersedia" atau "Dipinjam"
        self.dipinjam_oleh = dipinjam_oleh  # ID Anggota
        self.tgl_kembali = tgl_kembali      # Batas tanggal pengembalian
        self.next = None

class NodeAnggota:
    def __init__(self, id_anggota, nama, tipe):
        self.id_anggota = id_anggota
        self.nama = nama
        self.tipe = tipe              # "Siswa", "Mahasiswa", "Dosen"
        self.denda = 0                # Total denda terakumulasi
        self.next = None

class LinkedListPerpustakaanLengkap:
    def __init__(self):
        self.head_buku = None
        self.head_anggota = None

    # --- FITUR MANAJEMEN KOLEKSI ---
    def tambah_buku(self, id_buku, judul, pengarang):
        curr = self.head_buku
        while curr:
            if curr.id_buku == id_buku:
                return f"Gagal: ID Buku {id_buku} sudah terdaftar!"
            curr = curr.next

        buku_baru = NodeBuku(id_buku, judul, pengarang)
        if self.head_buku is None:
            self.head_buku = buku_baru
        else:
            current = self.head_buku
            while current.next:
                current = current.next
            current.next = buku_baru
        return f"Buku '{judul}' berhasil ditambahkan ke rak digital."

    def tampilkan_buku(self):
        hasil = []
        current = self.head_buku
        while current:
            hasil.append({
                "ID": current.id_buku,
                "Judul": current.judul,
                "Pengarang": current.pengarang,
                "Status": current.status,
                "Peminjam": current.dipinjam_oleh,
                "Batas Kembali": current.tgl_kembali
            })
            current = current.next
        return hasil

    def hapus_buku(self, id_buku):
        current = self.head_buku
        prev = None

        while current:
            if current.id_buku == id_buku:
                # Validasi jika buku sedang dipinjam tidak boleh dihapus
                if current.status == "Dipinjam":
                    return f"Gagal: Buku ID {id_buku} ('{current.judul}') tidak bisa dihapus karena sedang dipinjam."

                if prev is None:
                    self.head_buku = current.next
                else:
                    prev.next = current.next

                return f"Sukses: Buku '{current.judul}' dengan ID {id_buku} berhasil dihapus."

            prev = current
            current = current.next

        return "Gagal: ID Buku tidak ditemukan."

    # --- FITUR MANAJEMEN ANGGOTA ---
    def tambah_anggota(self, id_anggota, nama, tipe):
        curr = self.head_anggota
        while curr:
            if curr.id_anggota == id_anggota:
                return f"Gagal: ID Anggota {id_anggota} sudah terdaftar!"
            curr = curr.next

        anggota_baru = NodeAnggota(id_anggota, nama, tipe)
        if self.head_anggota is None:
            self.head_anggota = anggota_baru
        else:
            current = self.head_anggota
            while current.next:
                current = current.next
            current.next = anggota_baru
        return f"Anggota '{nama}' ({tipe}) berhasil didaftarkan."

    def tampilkan_anggota(self):
        hasil = []
        current = self.head_anggota
        while current:
            hasil.append({
                "ID": current.id_anggota,
                "Nama": current.nama,
                "Tipe": current.tipe,
                "Total Denda": f"Rp {current.denda:,}"
            })
            current = current.next
        return hasil

    # --- FITUR SIRKULASI (PINJAM & KEMBALI + DENDA) ---
    def pinjam_buku(self, id_buku, id_anggota, tgl_kembali_target):
        anggota = self.head_anggota
        found_anggota = False
        while anggota:
            if anggota.id_anggota == id_anggota:
                found_anggota = True
                break
            anggota = anggota.next
        if not found_anggota:
            return "Gagal: ID Anggota tidak ditemukan. Silakan daftar dulu."

        buku = self.head_buku
        while buku:
            if buku.id_buku == id_buku:
                if buku.status == "Dipinjam":
                    return f"Gagal: Buku '{buku.judul}' sedang dipinjam orang lain."
                
                buku.status = "Dipinjam"
                buku.dipinjam_oleh = id_anggota
                buku.tgl_kembali = tgl_kembali_target.strftime("%Y-%m-%d")
                return f"Sukses: Buku '{buku.judul}' berhasil dipinjam oleh {anggota.nama}."
            buku = buku.next
        return "Gagal: ID Buku tidak ditemukan."

    def kembalikan_buku(self, id_buku, tgl_dikembalikan):
        buku = self.head_buku
        while buku:
            if buku.id_buku == id_buku:
                if buku.status == "Tersedia":
                    return "Gagal: Buku ini sudah berada di perpustakaan."

                id_anggota = buku.dipinjam_oleh
                tgl_target = datetime.strptime(buku.tgl_kembali, "%Y-%m-%d").date()
                
                pesan_denda = ""
                if tgl_dikembalikan > tgl_target:
                    hari_terlambat = (tgl_dikembalikan - tgl_target).days
                    total_denda = hari_terlambat * 2000
                    
                    anggota = self.head_anggota
                    while anggota:
                        if anggota.id_anggota == id_anggota:
                            anggota.denda += total_denda
                            pesan_denda = f" (Terlambat {hari_terlambat} hari. Denda Rp {total_denda:,} ditambahkan ke akun Anda)"
                            break
                        anggota = anggota.next

                judul_buku = buku.judul
                buku.status = "Tersedia"
                buku.dipinjam_oleh = "-"
                buku.tgl_kembali = "-"
                return f"Sukses: Buku '{judul_buku}' berhasil dikembalikan.{pesan_denda}"
            buku = buku.next
        return "Gagal: ID Buku tidak ditemukan."


# ==========================
# SESSION STATE
# ==========================

if "sistem_perpus" not in st.session_state:
    st.session_state.sistem_perpus = LinkedListPerpustakaanLengkap()

if "inisialisasi" not in st.session_state:
    st.session_state.sistem_perpus.tambah_buku("B0001", "Back Stage", "Grysheis Tyya")
    st.session_state.sistem_perpus.tambah_buku("B0002", "Laut Bercerita", "Leila Salikha Chudori")
    st.session_state.sistem_perpus.tambah_anggota("A0001", "Vegraha", "Mahasiswa")
    st.session_state.inisialisasi = True

perpus = st.session_state.sistem_perpus

# ==========================
# TAMPILAN MENU
# ==========================

st.title("📚 SISTEM MANAJEMEN PERPUSTAKAAN")

menu = [
    "1. Manajemen Koleksi Buku",
    "2. Manajemen Anggota",
    "3. Transaksi Sirkulasi (Pinjam/Kembali)",
    "4. Laporan & Statistik",
    "5. Keluar"
]

pilihan = st.selectbox("Pilih Menu Utama", menu)

# ==========================
# MENU 1: MANAJEMEN BUKU
# ==========================
if pilihan == "1. Manajemen Koleksi Buku":
    st.header("🗂️ Manajemen Koleksi Buku")
    
    # Menambahkan opsi "Hapus Buku" ke dalam radio button
    sub_menu = st.radio("Aksi Buku", ["Tambah Buku Baru", "Lihat Rak Buku", "Hapus Buku"])
    
    if sub_menu == "Tambah Buku Baru":
        id_buku = st.text_input("ID Buku (Contoh: B03)")
        judul = st.text_input("Judul Buku")
        pengarang = st.text_input("Nama Pengarang")
        
        if st.button("Simpan Buku"):
            if id_buku and judul and pengarang:
                pesan = perpus.tambah_buku(id_buku, judul, pengarang)
                st.success(pesan)
            else:
                st.error("Semua field input data buku wajib diisi!")
                
    elif sub_menu == "Lihat Rak Buku":
        data_buku = perpus.tampilkan_buku()
        if not data_buku:
            st.warning("Belum ada koleksi buku.")
        else:
            st.dataframe(data_buku, use_container_width=True)

    elif sub_menu == "Hapus Buku":
        st.subheader("Form Penghapusan Buku")
        id_buku_hapus = st.text_input("Masukkan ID Buku yang akan dihapus")
        
        if st.button("Hapus Permanen"):
            if id_buku_hapus:
                pesan = perpus.hapus_buku(id_buku_hapus)
                if "Sukses" in pesan:
                    st.success(pesan)
                else:
                    st.error(pesan)
            else:
                st.warning("Silakan isi ID Buku terlebih dahulu.")

# ==========================
# MENU 2: MANAJEMEN ANGGOTA
# ==========================
elif pilihan == "2. Manajemen Anggota":
    st.header("👥 Manajemen Keanggotaan")
    
    sub_menu = st.radio("Aksi Anggota", ["Pendaftaran Anggota", "Daftar Anggota Aktif"])
    
    if sub_menu == "Pendaftaran Anggota":
        id_anggota = st.text_input("ID Anggota (Contoh: A02)")
        nama = st.text_input("Nama Lengkap")
        tipe = st.selectbox("Kategori", ["Siswa", "Mahasiswa", "Dosen"])
        
        if st.button("Daftarkan"):
            if id_anggota and nama:
                pesan = perpus.tambah_anggota(id_anggota, nama, tipe)
                st.success(pesan)
            else:
                st.error("ID dan Nama Anggota wajib diisi!")
                
    elif sub_menu == "Daftar Anggota Aktif":
        data_anggota = perpus.tampilkan_anggota()
        if not data_anggota:
            st.warning("Belum ada anggota terdaftar.")
        else:
            st.dataframe(data_anggota, use_container_width=True)

# ==========================
# MENU 3: TRANSAKSI SIRKULASI
# ==========================
elif pilihan == "3. Transaksi Sirkulasi (Pinjam/Kembali)":
    st.header("🔄 Sirkulasi Perpustakaan")
    aksi = st.tabs(["📖 Peminjaman Buku", "📥 Pengembalian Buku"])
    
    with aksi[0]:
        st.subheader("Form Peminjaman")
        id_b = st.text_input("Masukkan ID Buku yang akan Dipinjam")
        id_a = st.text_input("Masukkan ID Anggota Peminjam")
        tgl_kembali = st.date_input("Batas Tanggal Pengembalian (Maks 7 Hari)", date.today())
        
        if st.button("Proses Pinjam"):
            if id_b and id_a:
                pesan = perpus.pinjam_buku(id_b, id_a, tgl_kembali)
            if "Sukses" in pesan:st.success(pesan)
            else:
                st.error(pesan)
        else:
            st.warning("Isi ID Buku dan ID Anggota terlebih dahulu.")

    with aksi[1]:
        st.subheader("Form Pengembalian")
        id_b_kembali = st.text_input("Masukkan ID Buku yang Dikembalikan")
        tgl_kembali_aktual = st.date_input("Tanggal Pengembalian Hari Ini", date.today())

        if st.button("Proses Kembali"):
            if id_b_kembali:
                pesan = perpus.kembalikan_buku(id_b_kembali, tgl_kembali_aktual)
                if "Sukses" in pesan:
                    st.success(pesan)
                else:
                    st.error(pesan)
            else:
                st.warning("Isi ID Buku terlebih dahulu.")

# ==========================
# MENU 4: LAPORAN & STATISTIK
# ==========================
elif pilihan == "4. Laporan & Statistik":
    st.header("📊 Laporan Real-Time")

    buku_list = perpus.tampilkan_buku()
    anggota_list = perpus.tampilkan_anggota()

    total_buku = len(buku_list)
    buku_dipinjam = sum(1 for b in buku_list if b["Status"] == "Dipinjam")
    total_anggota = len(anggota_list)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Koleksi Buku", total_buku)
    col2.metric("Buku Sedang Dipinjam", buku_dipinjam)
    col3.metric("Total Anggota Aktif", total_anggota)

    st.subheader("Buku yang sedang di luar rak (Dipinjam):")
    buku_out = [b for b in buku_list if b["Status"] == "Dipinjam"]
    if not buku_out:
        st.info("Semua koleksi buku aman di dalam rak.")
    else:
        st.table(buku_out)

# ==========================
# MENU 5: KELUAR
# ==========================
elif pilihan == "5. Keluar":
    st.info("Sistem dinonaktifkan. Terima kasih telah menggunakan layanan perpustakaan digital.")