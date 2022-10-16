import string
from enum import Enum
from typing import List, Union

from pydantic import BaseModel


class User(BaseModel):
    username: str

    class Config:
        orm_mode = True


class UserCreate(User):
    password: str


class LogTransaction(BaseModel):
    username = str
    access_token = str
    user_agent = str
    client_host = str
    url_req = str
    response_body = str
    duration = str
    http_status = str
    str_time_created = str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
    time_created: str
    expired: str


class TokenData(BaseModel):
    username: Union[str, None] = None


# endpoint 1


class ViewTilang(BaseModel):

    nama: Union[str, None] = None
    no_reg_tilang: str
    no_ranmor: Union[str, None] = None
    kode_ins: Union[str, None] = None
    no_briva: Union[str, None] = None
    denda: Union[int, None] = None
    bp: Union[int, None] = None
    pasal: Union[str, None] = None
    tgl_sidang: Union[str, None] = None

    class Config:
        orm_mode = True

# endpoint 3


class ViewStatusPembayaran(BaseModel):

    no_reg_tilang: str
    kode_billing: Union[str, None] = None
    ntpn: Union[str, None] = None
    payment_date: Union[str, None] = None
    tgl_pembukuan: Union[str, None] = None
    channel: Union[str, None] = None
    bank_persepsi: Union[str, None] = None
    ca_name: Union[str, None] = None
    channel_type_name: Union[str, None] = None

    class Config:
        orm_mode = True

# endpoint 6


class ViewStatusPengambilanSisaTitipan(BaseModel):

    no_reg_tilang: str
    briva: Union[str, None] = None
    lokasi: Union[str, None] = None
    tgl_ambil: Union[str, None] = None
    rekening: Union[str, None] = None
    bank: Union[str, None] = None
    email: Union[str, None] = None

    class Config:
        orm_mode = True

# endpoint 7


class ViewDaftarPerkara(BaseModel):

    nama:  Union[str, None] = None
    no_reg_tilang: str
    no_ranmor: Union[str, None] = None
    kode_ins:  Union[str, None] = None
    no_briva: Union[str, None] = None
    denda:  Union[str, None] = None
    bp:  Union[str, None] = None
    pasal: Union[str, None] = None
    tgl_sidang:  Union[str, None] = None
    is_titip:  Union[str, None] = None
    uang_titipan: Union[int, None] = None
    tgl_bayar: Union[str, None] = None

    class Config:
        orm_mode = True

# endpoint 2


class ViewTilangSatker(BaseModel):

    kode_ins: str
    jml: Union[int, None] = None
    denda: Union[int, None] = None
    bp: Union[int, None] = None

    class Config:
        orm_mode = True

# endpoint 4


class ViewDaftarPerkaraSetor(BaseModel):

    # kode_ins : str
    no_reg_tilang: str
    nama: Union[str, None] = None
    alamat: Union[str, None] = None
    no_ranmor: Union[str, None] = None
    ntpn: Union[str, None] = None
    payment_date: Union[str, None] = None
    kode_billing: Union[str, None] = None
    tgl_pembukuan: Union[str, None] = None
    # bulan : int
    # tahun : int
    # tipe : str

    class Config:
        orm_mode = True


# endpoint 5
class ViewRekapDataPutusan(BaseModel):
    kode_ins: str
    inst_nama: str
    jml: Union[int, None] = None
    denda: Union[int, None] = None
    bp: Union[int, None] = None
    jumlah_titipan: Union[int, None] = None
    biru_denda_dibayar: Union[int, None] = None
    biru_bp_dibayar: Union[int, None] = None
    nominal_titipan: Union[int, None] = None
    biru_disetor: Union[int, None] = None
    biru_denda_disetor: Union[int, None] = None
    biru_bp_disetor: Union[int, None] = None
    merah_disetor: Union[int, None] = None
    merah_denda_disetor: Union[int, None] = None
    merah_bp_disetor: Union[int, None] = None

    class Config:
        orm_mode = True


class Tags(Enum):
    token = "TOKEN"
    etilang = "E-TILANG"
    rekap = "REKAP"
    daftarperkara = "DAFTAR PERKARA"
    briva = "BRIVA"

# endpoint 8


class ViewBriva(BaseModel):
    id: int
    price: Union[int, None] = None
    debitcredit: Union[str, None] = None
    description: Union[str, None] = None
    transaction_code: Union[str, None] = None
    value_timestamp: Union[str, None] = None
    entry_timestamp: Union[str, None] = None

    class Config:
        orm_mode = True
