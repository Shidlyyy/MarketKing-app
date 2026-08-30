import datetime
import io
import qrcode
import streamlit as st

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="Market King POS",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM CSS UNTUK TAMPILAN MODERN & AESTHETIC ---
st.markdown("""
<style>
    /* Styling Dasar & Background */
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    
    /* Hero Header Banner */
    .hero-container {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #4338ca 100%);
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 10px 25px -5px rgba(67, 56, 202, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }
    .hero-title {
        color: #ffffff;
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        color: #c7d2fe;
        font-size: 0.95rem;
        margin-top: 4px;
    }
    
    /* Card Container UI */
    .custom-card {
        background-color: #1e293b;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #334155;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
        margin-bottom: 16px;
    }
    
    /* Badge Status & Kategori */
    .badge-retail {
        background-color: #3b82f6;
        color: white;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
    }
    
    /* Styling Ringkasan Total */
    .total-box {
        background: linear-gradient(135deg, #065f46 0%, #047857 100%);
        border-radius: 12px;
        padding: 16px;
        color: white;
        text-align: center;
        margin: 15px 0;
        box-shadow: 0 4px 12px rgba(4, 120, 87, 0.3);
    }
    
    /* Override Struk Code Block */
    .stCodeBlock {
        border-radius: 12px !important;
        border: 1px solid #334155 !important;
    }
</style>
""", unsafe_allow_html=True)

# 2. Data Master Produk & Rekening
BARANG = {
    "1": ("Mie Instan Goreng", 3500, "Makanan Instan & Olahan"),
    "2": ("Mie Instan Kuah", 3300, "Makanan Instan & Olahan"),
    "3": ("Bubur Instan Cup", 6000, "Makanan Instan & Olahan"),
    "4": ("Sosis Sapi Ready to Eat", 8000, "Makanan Instan & Olahan"),
    "5": ("Roti Tawar Kupas", 14000, "Makanan Instan & Olahan"),
    "6": ("Roti Cokelat", 6000, "Makanan Instan & Olahan"),
    "7": ("Air Mineral 600ml", 3500, "Minuman"),
    "8": ("Air Mineral 1500ml", 6500, "Minuman"),
    "9": ("Susu UHT 250ml", 7000, "Minuman"),
    "10": ("Susu UHT 1L", 20000, "Minuman"),
    "11": ("Kopi Kemasan Botol", 9500, "Minuman"),
    "12": ("Teh Kemasan Botol", 4500, "Minuman"),
    "13": ("Isotonik Botol", 7500, "Minuman"),
    "14": ("Keripik Kentang", 11500, "Makanan Ringan"),
    "15": ("Keripik Singkong", 9500, "Makanan Ringan"),
    "16": ("Biskuit Kaleng", 32000, "Makanan Ringan"),
    "17": ("Cokelat Batangan", 15000, "Makanan Ringan"),
    "18": ("Kacang Atom 100g", 8500, "Makanan Ringan"),
    "19": ("Beras Pulen 5kg", 72000, "Sembako & Bahan Dapur"),
    "20": ("Minyak Goreng 2L", 36000, "Sembako & Bahan Dapur"),
    "21": ("Gula Pasir 1kg", 17500, "Sembako & Bahan Dapur"),
    "22": ("Telur Ayam (10 butir)", 22000, "Sembako & Bahan Dapur"),
    "23": ("Kecap Manis 520ml", 21000, "Sembako & Bahan Dapur"),
    "24": ("Sabun Mandi Cair 450ml", 26000, "Perawatan Diri"),
    "25": ("Sampo Botol 160ml", 24500, "Perawatan Diri"),
    "26": ("Pasta Gigi 190g", 14000, "Perawatan Diri"),
    "27": ("Sikat Gigi (1 pcs)", 7500, "Perawatan Diri"),
    "28": ("Sabun Cuci Muka 100g", 31000, "Perawatan Diri"),
    "29": ("Deterjen Bubuk 800g", 21500, "Kebutuhan Rumah Tangga"),
    "30": ("Pembersih Lantai 780ml", 13500, "Kebutuhan Rumah Tangga"),
    "31": ("Pencuci Piring 780ml", 15000, "Kebutuhan Rumah Tangga"),
    "32": ("Tisu Wajah 250 sheets", 16500, "Kebutuhan Rumah Tangga"),
}

REKENING_BANK = {
    "BCA": {"no": "138-092-8841", "color": "#38bdf8", "bg": "#0f172a"},
    "Mandiri": {"no": "134-00-1982341-2", "color": "#fbbf24", "bg": "#0f172a"},
    "BRI": {"no": "0182-01-002938-53-4", "color": "#60a5fa", "bg": "#0f172a"},
    "BNI": {"no": "098-765-4321", "color": "#fb923c", "bg": "#0f172a"},
    "Atas Nama": "MARKET KING",
}

def buat_qr_code(data_text):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )
    qr.add_data(data_text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

if "keranjang" not in st.session_state:
    st.session_state.keranjang = []

# --- HEADER HERO BANNER ---
WIB = datetime.timezone(datetime.timedelta(hours=7))
waktu_sekarang_display = datetime.datetime.now(WIB).strftime("%d %B %Y | %H:%M:%S WIB")

st.markdown(f"""
<div class="hero-container">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 class="hero-title">🛍️ MARKET KING POS</h1>
            <p class="hero-subtitle">Sistem Kasir Modern & Smart Retail Enterprise</p>
        </div>
        <div style="text-align: right;">
            <span class="badge-retail">STORE ID: #CRB-01</span>
            <p style="color: #cbd5e1; font-size: 0.85rem; margin-top: 6px; margin-bottom: 0;">📍 Kejaksan, Cirebon</p>
            <p style="color: #94a3b8; font-size: 0.8rem; margin: 0;">🕒 {waktu_sekarang_display}</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- PANEL METRIK UTAMA ---
subtotal_kotor_temp = sum(item["subtotal"] for item in st.session_state.keranjang)
total_item_temp = sum(item["jumlah"] for item in st.session_state.keranjang)

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric(label="🛒 Item di Keranjang", value=f"{len(st.session_state.keranjang)} Jenis")
with m2:
    st.metric(label="📦 Total Qty", value=f"{total_item_temp} Pcs")
with m3:
    st.metric(label="💰 Subtotal Sementara", value=f"Rp{subtotal_kotor_temp:,}")
with m4:
    if st.button("🔄 Reset Transaksi", use_container_width=True):
        st.session_state.keranjang = []
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# --- INPUT KASIR ---
with st.container():
    col_k1, col_k2 = st.columns([2, 1])
    with col_k1:
        nama_kasir = st.text_input(
            "👤 Petugas Kasir / Operator:",
            value="Kasir 1",
            help="Nama kasir yang bertanggung jawab pada sesi ini"
        )

st.markdown("---")

# --- TATA LETAK UTAMA (DUA KOLOM) ---
col_kiri, col_kanan = st.columns([1.1, 1])

# --- KOLOM KIRI: INPUT BARANG & KATALOG ---
with col_kiri:
    st.subheader("📦 Input Produk Belanja")

    opsi_barang = {f"[{k}] {v[0]} - Rp{v[1]:,} ({v[2]})": k for k, v in BARANG.items()}
    pilihan_label = st.selectbox(
        "🔍 Cari / Pilih Produk:", list(opsi_barang.keys())
    )
    kode_terpilih = opsi_barang[pilihan_label]
    nama_item, harga_item, kategori_item = BARANG[kode_terpilih]

    c_qty, c_btn = st.columns([1, 1])
    with c_qty:
        jumlah = st.number_input(
            f"Jumlah (Qty):", min_value=1, value=1, step=1
        )
    with c_btn:
        st.write("")
        st.write("")
        if st.button("➕ Tambahkan Produk", use_container_width=True, type="primary"):
            subtotal = harga_item * jumlah
            st.session_state.keranjang.append(
                {
                    "kode": kode_terpilih,
                    "nama": nama_item,
                    "harga": harga_item,
                    "jumlah": jumlah,
                    "subtotal": subtotal,
                }
            )
            st.toast(f"Berhasil menambahkan {nama_item}!", icon="✅")
            st.rerun()

    with st.expander("📊 Katalog & Stok Master Produk"):
        st.dataframe(
            [
                {
                    "Kode": k,
                    "Nama Produk": v[0],
                    "Kategori": v[2],
                    "Harga Unit": f"Rp{v[1]:,}",
                }
                for k, v in BARANG.items()
            ],
            use_container_width=True,
            hide_index=True
        )

# --- KOLOM KANAN: KERANJANG & PEMBAYARAN ---
with col_kanan:
    st.subheader("📋 Ringkasan Belanja")

    if not st.session_state.keranjang:
        st.info("🛒 Keranjang belanja masih kosong.")
    else:
        st.dataframe(
            st.session_state.keranjang,
            column_config={
                "kode": "Kode",
                "nama": "Nama Produk",
                "harga": st.column_config.NumberColumn(
                    "Harga", format="Rp %d"
                ),
                "jumlah": "Qty",
                "subtotal": st.column_config.NumberColumn(
                    "Subtotal", format="Rp %d"
                ),
            },
            hide_index=True,
            use_container_width=True,
        )

        subtotal_kotor = sum(
            item["subtotal"] for item in st.session_state.keranjang
        )

        persen_diskon = 0
        if subtotal_kotor >= 500000:
            persen_diskon = 15
        elif subtotal_kotor >= 200000:
            persen_diskon = 10
        elif subtotal_kotor >= 100000:
            persen_diskon = 5

        nominal_diskon = int(subtotal_kotor * (persen_diskon / 100))
        total_akhir = subtotal_kotor - nominal_diskon

        # Display Total Tagihan Aestetik
        st.markdown(f"""
        <div class="total-box">
            <span style="font-size: 0.9rem; letter-spacing: 1px; text-transform: uppercase;">Total Tagihan</span>
            <h2 style="margin: 0; font-size: 2.2rem; font-weight: 800;">Rp{total_akhir:,}</h2>
            {"<p style='margin: 4px 0 0 0; font-size: 0.85rem; color: #a7f3d0;'>🎉 Diskon Member Applied: " + str(persen_diskon) + "% (-Rp" + f"{nominal_diskon:,}" + ")</p>" if persen_diskon > 0 else ""}
        </div>
        """, unsafe_allow_html=True)

        st.subheader("💳 Metode Pembayaran")

        opsi_bayar = st.radio(
            "Pilih Metode Pembayaran:",
            ["Tunai", "QRIS Instant", "Transfer Bank / EDC"],
            horizontal=True,
        )

        metode_pembayaran = opsi_bayar
        bayar = 0
        kembalian = 0
        siap_bayar = False

        if opsi_bayar == "Tunai":
            bayar = st.number_input(
                "Nominal Uang diterima (Rp):",
                min_value=0,
                value=int(total_akhir),
                step=1000,
            )

            if bayar < total_akhir:
                st.error(f"⚠️ Pembayaran kurang Rp{total_akhir - bayar:,}")
            else:
                kembalian = bayar - total_akhir
                st.success(f"💵 Kembalian Pelanggan: **Rp{kembalian:,}**")
                siap_bayar = True

        elif opsi_bayar == "QRIS Instant":
            st.markdown(
                """
                <div style="background-color: #0f172a; padding: 16px; border-radius: 12px; text-align: center; border: 1px solid #334155;">
                    <h4 style="margin:0; color: #38bdf8;">📲 QRIS NATIONAL STANDARD</h4>
                    <p style="margin: 4px 0 0 0; font-size: 12px; color: #94a3b8;">Merchant: <b>MARKET KING STORE</b></p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            payload_qris = f"00020101021226680016ID.MARKETKING.WWW0118936009180000000000520458125303360540{total_akhir}5802ID5911MARKET KING6007CIREBON6304"
            gambar_qr = buat_qr_code(payload_qris)

            c1, c2, c3 = st.columns([1, 2, 1])
            with c2:
                st.image(
                    gambar_qr,
                    caption=f"Scan & Bayar: Rp{total_akhir:,}",
                    use_container_width=True,
                )

            st.caption("✅ Mendukung BCA Mobile, Livin, GoPay, OVO, DANA, ShopeePay & QRIS Lainnya.")
            bayar = total_akhir
            siap_bayar = True

        elif opsi_bayar == "Transfer Bank / EDC":
            sub_metode = st.radio(
                "Pilih Jalur Transaksi:",
                ["Transfer Bank (Virtual Account)", "Mesin EDC (Debit/Kredit)"],
                horizontal=True,
            )

            if sub_metode == "Transfer Bank (Virtual Account)":
                pilihan_bank = st.selectbox("Pilih Bank Tujuan:", ["BCA", "Mandiri", "BRI", "BNI"])
                bank_info = REKENING_BANK[pilihan_bank]

                st.markdown(
                    f"""
                    <div style="background: {bank_info['bg']}; padding: 16px; border-radius: 12px; border-left: 6px solid {bank_info['color']}; border-top: 1px solid #334155; border-right: 1px solid #334155; border-bottom: 1px solid #334155;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-size: 18px; font-weight: bold; color: {bank_info['color']};">{pilihan_bank} DIRECT</span>
                            <span style="font-size: 10px; background: #334155; padding: 2px 8px; border-radius: 4px; color: #fff;">AUTOMATED</span>
                        </div>
                        <p style="margin: 8px 0 2px 0; font-size: 12px; color: #94a3b8;">Nomor Rekening / VA:</p>
                        <h3 style="margin: 0; font-family: monospace; color: #f8fafc; letter-spacing: 1.5px;">{bank_info['no']}</h3>
                        <p style="margin: 6px 0 0 0; font-size: 12px; color: #cbd5e1;">Atas Nama: <b>{REKENING_BANK['Atas Nama']}</b></p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    """
                    <div style="background: #1e293b; padding: 18px; border-radius: 12px; border: 1px dashed #475569; text-align: center;">
                        <h4 style="margin: 0; color: #38bdf8;">💳 TERMINAL EDC READY</h4>
                        <p style="margin: 6px 0 0 0; color: #cbd5e1; font-size: 13px;">Silakan <b>Tap / Gesek / Dip</b> Kartu Debit/Kredit pada mesin EDC.</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            bayar = total_akhir
            siap_bayar = True

        st.markdown("<br>", unsafe_allow_html=True)

        # CETAK STRUK
        if siap_bayar:
            if st.button(
                "🖨️ Selesaikan Transaksi & Cetak Struk",
                type="primary",
                use_container_width=True,
            ):
                waktu_transaksi = datetime.datetime.now(WIB).strftime("%Y-%m-%d %H:%M:%S")

                lines_struk = [
                    "========================================",
                    "            MARKET KING POS             ",
                    "     Jl. Kartini No. 45, Kejaksan       ",
                    "              Kota Cirebon              ",
                    "========================================",
                    f"Kasir   : {nama_kasir}",
                    f"Waktu   : {waktu_transaksi} WIB",
                    "----------------------------------------",
                ]
                for item in st.session_state.keranjang:
                    lines_struk.append(f"{item['nama']}")
                    lines_struk.append(
                        f"  {item['jumlah']} x Rp{item['harga']:,} = Rp{item['subtotal']:,}"
                    )
                lines_struk.extend(
                    [
                        "----------------------------------------",
                        f"Subtotal      : Rp{subtotal_kotor:,}",
                    ]
                )
                if persen_diskon > 0:
                    lines_struk.append(
                        f"Diskon ({persen_diskon}%)  : -Rp{nominal_diskon:,}"
                    )
                lines_struk.extend(
                    [
                        f"Total Akhir   : Rp{total_akhir:,}",
                        f"Metode Bayar  : {opsi_bayar}",
                        f"Jumlah Bayar  : Rp{bayar:,}",
                        f"Kembalian     : Rp{kembalian:,}",
                        "========================================",
                        "    TERIMA KASIH ATAS KUNJUNGAN ANDA    ",
                        "      HARAP SIMPAN STRUK INI            ",
                        "========================================",
                    ]
                )

                isi_struk = "\n".join(lines_struk)

                st.balloons()
                st.success(f"✅ Transaksi Berhasil Diproses oleh **{nama_kasir}**!")
                st.code(isi_struk, language="text")

                nama_file = f"struk_{datetime.datetime.now(WIB).strftime('%Y%m%d_%H%M%S')}.txt"
                st.download_button(
                    label="📥 Unduh Struk Digital (.txt)",
                    data=isi_struk,
                    file_name=nama_file,
                    mime="text/plain",
                    use_container_width=True
                )