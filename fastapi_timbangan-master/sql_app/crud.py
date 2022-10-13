from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, funcfilter
from . import models, schemas
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def view_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ViewUser).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    argonhaspwd = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        hashed_password=argonhaspwd)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_token(db: Session, username: str, access_token: str,  time_created: str, expired: str, client_host: str):
    db_token = models.TokenUser(username=username, access_token=access_token,
                                time_created=time_created, expired=expired, client_host=client_host)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token


def create_log(db: Session, username: str, access_token: str,  user_agent: str, client_host: str, url_req: str, response_body: str, duration: str, http_status: str, str_time_created: str):
    db_log = models.LogTransaction(
        username=username, access_token=access_token, user_agent=user_agent, client_host=client_host, url_req=url_req, response_body=response_body, duration=duration, http_status=http_status, str_time_created=str_time_created)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def is_superuser(db: Session, username: str):
    return db.query(models.User.role).filter(models.User.username == username).first()


def get_password_hash(password):
    return pwd_context.hash(password)


# def get_user_dict(db: Session, username: str):
#     if username in db:
#         user_dict = db[username]
#         return schemas.UserInDB(**user_dict)


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def get_cities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.City).offset(skip).limit(limit).all()


# endpoint 1
def get_no_reg_tilang(db: Session, no_reg_tilang: str):
    return db.query(models.ViewTilang).filter(models.ViewTilang.no_reg_tilang == no_reg_tilang).first()

    # def get_user_by_username(db: Session, username: str):
    # return db.query(models.User).filter(models.User.username == username).first()


# endpoint 2
def get_status_pembayaran(db: Session, no_reg_tilang: str):
    return db.query(models.ViewStatusPembayaran).filter(models.ViewStatusPembayaran.no_reg_tilang == no_reg_tilang).first()

# endpoint 6


def get_status_pengambilan_sisa_titipan(db: Session, no_reg_tilang: str):
    return db.query(models.ViewStatusPengambilanSisaTitipan).filter(models.ViewStatusPengambilanSisaTitipan.no_reg_tilang == no_reg_tilang).first()

# endpoint 7


def get_daftar_perkara(db: Session, kode_ins: str, tgl_sidang: str, skip: int, limit: int):
    getgroup = db.query(models.ViewDaftarPerkara).filter(
        and_(
            models.ViewDaftarPerkara.kode_ins == kode_ins,
            models.ViewDaftarPerkara.tgl_sidang == tgl_sidang
        )
    ).offset(skip).limit(limit).all()
    return getgroup


# endpoint 2
# bulan
def get_tilang_satker_bulan(db: Session, kode_ins: str, bulan: int, tahun: int):
    data_req = db.query(models.ViewTilangSatkerBulan).filter(
        and_(models.ViewTilangSatkerBulan.kode_ins == kode_ins,
             models.ViewTilangSatkerBulan.bulan == bulan,
             models.ViewTilangSatkerBulan.tahun == tahun)
    ).first()
    return data_req

# tahun


def get_tilang_satker_tahun(db: Session, kode_ins: str, tahun: int):
    data_req = db.query(models.ViewTilangSatkerTahun).filter(
        and_(models.ViewTilangSatkerTahun.kode_ins == kode_ins,
             models.ViewTilangSatkerTahun.tahun == tahun)
    ).first()

    return data_req

# endpoint 4


def get_daftar_perkara_setor(
        db: Session,
        kode_ins: str,
        bulan: int,
        tahun: int,
        payment_date: str,
        tipe: str,
        skip: int,
        limit: int
):
    data_req = db.query(models.ViewDaftarPerkaraSetor).filter(
        and_(
            models.ViewDaftarPerkaraSetor.kode_ins == kode_ins,
            models.ViewDaftarPerkaraSetor.bulan == bulan,
            models.ViewDaftarPerkaraSetor.tahun == tahun,
            models.ViewDaftarPerkaraSetor.payment_date == payment_date,
            models.ViewDaftarPerkaraSetor.tipe == tipe,
        )).offset(skip).limit(limit).all()

    return data_req

# endpoint 5


def get_rekap_data_putusan_tahun(db: Session, kode_ins: str, tahun: int):
    get_rekap_th = db.query(models.ViewRekapDataPutusanTahun).filter(
        and_(models.ViewRekapDataPutusanTahun.kode_ins == kode_ins,
             models.ViewRekapDataPutusanTahun.tahun == tahun)
    ).first()

    return get_rekap_th


def get_rekap_data_putusan_triwulan(db: Session, kode_ins: str, tahun: int, triwulan: int):
    get_rekap_tri = db.query(models.ViewRekapDataPutusanTriwulan).filter(
        and_(models.ViewRekapDataPutusanTriwulan.kode_ins == kode_ins,
             models.ViewRekapDataPutusanTriwulan.tahun == tahun,
             models.ViewRekapDataPutusanTriwulan.triwulan == triwulan)
    ).first()

    return get_rekap_tri


def get_rekap_data_putusan_semester(db: Session, kode_ins: str, tahun: int, semester: int):
    get_rekap_s = db.query(models.ViewRekapDataPutusanSemester).filter(
        and_(models.ViewRekapDataPutusanSemester.kode_ins == kode_ins,
             models.ViewRekapDataPutusanSemester.tahun == tahun,
             models.ViewRekapDataPutusanSemester.semester == semester)
    ).first()

    return get_rekap_s


def get_briva(db: Session, kode: str):
    get_kode = db.query(models.ViewBriva).filter(
        models.ViewBriva.description.like("%"+kode+"%")).offset(0).limit(1).all()
    return get_kode
