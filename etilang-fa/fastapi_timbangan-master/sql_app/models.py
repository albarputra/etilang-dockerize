from email.policy import default
from .database import Base
from datetime import datetime
from sqlalchemy import String, Boolean, Integer, Column, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    __table_args__ = ({"schema": "api"})

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="guest")
    nama_penanggung_jawab = Column(String)
    NIP = Column(String)
    jabatan = Column(String)
    instansi = Column(String)
    created_date = Column(DateTime)
    updated_date = Column(DateTime)


class LogTransaction(Base):
    __tablename__ = "log_transaction"
    __table_args__ = ({"schema": "api"})

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    access_token = Column(String)
    user_agent = Column(String)
    client_host = Column(String)
    url_req = Column(String)
    response_body = Column(String)
    duration = Column(String)
    http_status = Column(Integer)
    str_time_created = Column(String)

    # def __repr__(self):
    #     return f"<User id={self.id}, username={self.username}>"


class TokenUser(Base):
    __tablename__ = "token_user"
    __table_args__ = ({"schema": "api"})

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    access_token = Column(String, unique=True)
    time_created = Column(String)
    expired = Column(String)
    client_host = Column(String)

# endpoint 1


class ViewTilang(Base):
    __tablename__ = "v_get_tilang"
    __table_args__ = ({"schema": "api"})

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String)
    no_reg_tilang = Column(String)
    no_ranmor = Column(String)
    kode_ins = Column(String)
    no_briva = Column(String)
    denda = Column(Integer)
    bp = Column(Integer)
    pasal = Column(String)
    tgl_sidang = Column(String)

# endpoint 3


class ViewStatusPembayaran(Base):
    __tablename__ = "v_get_status_pembayaran"
    __table_args__ = ({"schema": "api"})

    # id = Column(Integer, primary_key=True, index=True)
    no_reg_tilang = Column(String, primary_key=True)
    kode_billing = Column(String)
    ntpn = Column(String)
    payment_date = Column(String)
    tgl_pembukuan = Column(String)
    channel = Column(String)
    bank_persepsi = Column(String)
    ca_name = Column(String)
    channel_type_name = Column(String)

# endpoint 6


class ViewStatusPengambilanSisaTitipan(Base):
    __tablename__ = "v_get_status_pengambilan_sisa_titipan"
    __table_args__ = ({"schema": "api"})

    # id = Column(Integer, primary_key=True, index=True)
    no_reg_tilang = Column(String, primary_key=True)
    briva = Column(String)
    lokasi = Column(String)
    tgl_ambil = Column(String)
    rekening = Column(String)
    bank = Column(String)
    email = Column(String)

# endpoint 7


class ViewDaftarPerkara(Base):
    __tablename__ = "v_get_daftar_perkara"
    __table_args__ = ({"schema": "api"})

    # id = Column(Integer, primary_key=True, index=True)
    nama = Column(String)
    no_reg_tilang = Column(String, primary_key=True)
    no_ranmor = Column(String)
    kode_ins = Column(String)
    no_briva = Column(String)
    denda = Column(String)
    bp = Column(String)
    pasal = Column(String)
    tgl_sidang = Column(String)
    is_titip = Column(String)
    uang_titipan = Column(Integer)
    tgl_bayar = Column(String)

# endpoint #2
# bulan


class ViewTilangSatkerBulan(Base):
    __tablename__ = "v_get_rekap_satker_bulan"
    __table_args__ = ({"schema": "api"})

    kode_ins = Column(String, primary_key=True)
    jml = Column(Integer)
    denda = Column(Integer)
    bp = Column(Integer)
    bulan = Column(Integer)
    tahun = Column(Integer)


class ViewTilangSatkerTahun(Base):
    __tablename__ = "v_get_rekap_satker_tahun"
    __table_args__ = ({"schema": "api"})

    kode_ins = Column(String, primary_key=True)
    jml = Column(Integer)
    denda = Column(Integer)
    bp = Column(Integer)
    tahun = Column(Integer)


# endpoint 4
class ViewDaftarPerkaraSetor(Base):
    __tablename__ = "v_get_daftar_perkara_setor"
    __table_args__ = ({"schema": "api"})

    kode_ins = Column(String)
    no_reg_tilang = Column(String, primary_key=True)
    nama = Column(String)
    alamat = Column(String)
    no_ranmor = Column(String)
    ntpn = Column(String)
    payment_date = Column(String)
    kode_billing = Column(String)
    tgl_pembukuan = Column(String)
    bulan = Column(Integer)
    tahun = Column(Integer)
    tipe = Column(String)

# emdpoint 5


class ViewRekapDataPutusanTahun(Base):
    __tablename__ = "v_get_rekap_data_putusan_tahun"
    __table_args__ = ({"schema": "api"})

    kode_ins = Column(String, primary_key=True)
    inst_nama = Column(String)
    tahun = Column(Integer)
    jml = Column(Integer)
    denda = Column(Integer)
    bp = Column(Integer)
    jumlah_titipan = Column(Integer)
    biru_denda_dibayar = Column(Integer)
    biru_bp_dibayar = Column(Integer)
    nominal_titipan = Column(Integer)
    biru_disetor = Column(Integer)
    biru_denda_disetor = Column(Integer)
    biru_bp_disetor = Column(Integer)
    merah_disetor = Column(Integer)
    merah_denda_disetor = Column(Integer)
    merah_bp_disetor = Column(Integer)


class ViewRekapDataPutusanTriwulan(Base):
    __tablename__ = "v_get_rekap_data_putusan_triwulan"
    __table_args__ = ({"schema": "api"})

    kode_ins = Column(String, primary_key=True)
    inst_nama = Column(String)
    tahun = Column(Integer)
    triwulan = Column(Integer)
    jml = Column(Integer)
    denda = Column(Integer)
    bp = Column(Integer)
    jumlah_titipan = Column(Integer)
    biru_denda_dibayar = Column(Integer)
    biru_bp_dibayar = Column(Integer)
    nominal_titipan = Column(Integer)
    biru_disetor = Column(Integer)
    biru_denda_disetor = Column(Integer)
    biru_bp_disetor = Column(Integer)
    merah_disetor = Column(Integer)
    merah_denda_disetor = Column(Integer)
    merah_bp_disetor = Column(Integer)


class ViewRekapDataPutusanSemester(Base):
    __tablename__ = "v_get_rekap_data_putusan_semester"
    __table_args__ = ({"schema": "api"})

    kode_ins = Column(String, primary_key=True)
    inst_nama = Column(String)
    tahun = Column(Integer)
    semester = Column(Integer)
    jml = Column(Integer)
    denda = Column(Integer)
    bp = Column(Integer)
    jumlah_titipan = Column(Integer)
    biru_denda_dibayar = Column(Integer)
    biru_bp_dibayar = Column(Integer)
    nominal_titipan = Column(Integer)
    biru_disetor = Column(Integer)
    biru_denda_disetor = Column(Integer)
    biru_bp_disetor = Column(Integer)
    merah_disetor = Column(Integer)
    merah_denda_disetor = Column(Integer)
    merah_bp_disetor = Column(Integer)

# endpoint 8


class ViewBriva(Base):
    __tablename__ = "v_get_briva"
    __table_args__ = ({"schema": "api"})

    id = Column(Integer, primary_key=True)
    price = Column(Integer)
    debitcredit = Column(String)
    description = Column(String)
    transaction_code = Column(String)
    value_timestamp = Column(String)
    entry_timestamp = Column(String)
    created_at = Column(String)
