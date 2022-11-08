import re
import secrets
from fastapi import FastAPI, status, HTTPException, Form, Query, Depends,  Request, Response, Body, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Union
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from dotenv import load_dotenv
import os

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
import datetime
import time
from typing import Callable
from fastapi.routing import APIRoute
import json

# models.Base.metadata.create_all(bind=engine)
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ACCESS_TOKEN_EXPIRE_DAY = 1

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# route


class TimedRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            time_created = datetime.datetime.now()
            str_time_created = time_created.strftime("%d-%m-%Y %H:%M:%S")
            before = time.time()
            response: Response = await original_route_handler(request)
            dur = time.time() - before
            duration = str(dur)
            http_status = response.status_code
            response_body = response.body
            url_req = request.url._url
            a = request.method
            client_host = request.client.host

            user_agent = request.headers["user-agent"]
            rbod = json.loads(response_body)
            rb = json.dumps(rbod, indent=4, sort_keys=True)
            username = None
            if a == 'POST':
                username = "Not Authentication"
                access_token = "-"
                db = request.state.db
                db_log = models.LogTransaction(
                    username=username, access_token=access_token, user_agent=user_agent, client_host=client_host, url_req=url_req, response_body=rb, duration=duration, http_status=http_status, str_time_created=str_time_created)
                db.add(db_log)
                db.commit()
                db.refresh(db_log)
            else:
                user = request.headers["authorization"].lstrip("Bearer")
                access_token = user.strip()
                payload = jwt.decode(access_token, SECRET_KEY,
                                     algorithms=[ALGORITHM])
                username = payload["sub"]
                db = request.state.db
                db_log = models.LogTransaction(
                    username=username, access_token=access_token, user_agent=user_agent, client_host=client_host, url_req=url_req, response_body=rb, duration=duration, http_status=http_status, str_time_created=str_time_created)
                db.add(db_log)
                db.commit()
                db.refresh(db_log)

            return response

        return custom_route_handler


load_dotenv()

app = FastAPI(title="e-tilang",
              description="E-TILANG KEJAKSAAN",
              version="0.0.1",
              redoc_url="/",
              openapi_url="/api/v1/openapi.json",
              contact={
                  "name": "Info Pengaduan",
                  "url": "https://tilang.kejaksaan.go.id/info/pengaduan"
              }
              )

router = APIRouter(route_class=TimedRoute)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error",
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

# Dependency


def get_db(request: Request):
    return request.state.db


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    if expires_delta:
        # expire = datetime.utcnow() + expires_delta
        expire = datetime.datetime.now()
    else:
        # expire = datetime.utcnow() + timedelta(minutes=15)
        expire = datetime.datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = crud.get_user_by_username(db, username=token_data.username)
    #user = get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: models.User = Depends(get_current_user)):
    if current_user.is_active:
        return current_user
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")


# deactivated
# @app.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme), current_user: models.User = Depends(get_current_user)):
#     db_user = crud.get_user_by_username(db, username=user.username)

#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = schemas.TokenData(username=username)
#         userToken = crud.get_user_by_username(db, username=token_data.username)
#     except JWTError:
#         raise credentials_exception

#     if userToken is None:
#         raise credentials_exception

#     if db_user:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
#                             detail="Username already registered")

#     if current_user.role == "admin":
#         return crud.create_user(db=db, user=user)
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, detail="You're not admin")

    # return crud.create_user(db=db, user=user)


# @app.get("/users/", response_model=List[schemas.User], status_code=status.HTTP_200_OK)
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users


# @app.get("/users/{user_id}", response_model=schemas.User, status_code=status.HTTP_200_OK)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
#     return db_user
# @app.get("/")
# def read_root(request: Request):
#     client_host = request.client.host
#     return {"client_host": client_host}


@router.post("/token", response_model=schemas.Token, status_code=status.HTTP_200_OK, tags=[schemas.Tags.token])
async def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAY)
    time_created = datetime.datetime.now()
    str_time_created = time_created.strftime("%d-%m-%Y %H:%M:%S")
    expired = datetime.datetime.now() + access_token_expires
    str_expired = expired.strftime("%d-%m-%Y %H:%M:%S")
    client_host = request.client.host
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    insert_token = crud.create_token(
        db, form_data.username, access_token, str_time_created, str_expired, client_host)
    if not insert_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed Create Token")

    return {"access_token": access_token, "token_type": "bearer", "time_created": str_time_created, "expired": str_expired}


# @app.get("/users/me/", response_model=schemas.User)
# async def read_users_me(current_user: models.User = Depends(get_current_active_user)):
#     return current_user


# @app.get("/view-users/", response_model=List[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.view_users(db, skip=skip, limit=limit)
#     return users

# endpoint 1


@router.get("/etilang/{no_reg_tilang}", response_model=schemas.ViewTilang, status_code=status.HTTP_200_OK, tags=[schemas.Tags.etilang])
async def get_no_reg_tilang(no_reg_tilang: str, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"})
    no_reg_tilang = crud.get_no_reg_tilang(db, no_reg_tilang)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
        user = crud.get_user_by_username(db, username=token_data.username)
    except JWTError:
        raise credentials_exception
    if user is None:
        raise credentials_exception
    elif no_reg_tilang is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No Reg tilang tidak ditemui")

    return no_reg_tilang

# endpoint 3


@router.get("/etilang/statuspembayaran/{no_reg_tilang}", response_model=schemas.ViewStatusPembayaran, status_code=status.HTTP_200_OK, tags=[schemas.Tags.etilang])
async def get_status_pembayaran(no_reg_tilang: str, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"})
    no_reg_tilang = crud.get_status_pembayaran(db, no_reg_tilang)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
        user = crud.get_user_by_username(db, username=token_data.username)
    except JWTError:
        raise credentials_exception
    if user is None:
        raise credentials_exception
    elif no_reg_tilang is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No Reg tilang tidak ditemui")

    return no_reg_tilang

# endpoint 6


@router.get("/etilang/statuspengambilan/{no_reg_tilang}", response_model=schemas.ViewStatusPengambilanSisaTitipan, status_code=status.HTTP_200_OK, tags=[schemas.Tags.etilang])
async def get_status_pengambilan(no_reg_tilang: str, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"})
    no_reg_tilang = crud.get_status_pengambilan_sisa_titipan(db, no_reg_tilang)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
        user = crud.get_user_by_username(db, username=token_data.username)
    except JWTError:
        raise credentials_exception
    if user is None:
        raise credentials_exception
    elif no_reg_tilang is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No Reg tilang tidak ditemui")

    return no_reg_tilang

# endpoint 7


@router.get("/daftarperkara/{kode_ins}/{tgl_sidang}/", response_model=List[schemas.ViewDaftarPerkara], status_code=status.HTTP_200_OK, tags=[schemas.Tags.daftarperkara])
async def get_daftar_perkara(
        kode_ins: str,
        tgl_sidang: str,
        # skip: int = 0,
        # limit: int = 100,
        limit: int = Query(default=5000),

        db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"})

    daftar_perkara = crud.get_daftar_perkara(
        db, kode_ins=kode_ins, tgl_sidang=tgl_sidang, limit=limit)

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
        user = crud.get_user_by_username(db, username=token_data.username)
    except JWTError:
        raise credentials_exception
    if user is None:
        raise credentials_exception
    elif len(daftar_perkara) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="perkara tidak di temukan")

    return daftar_perkara


# endpoint 2
@router.get("/rekap/satker/{kode_ins}/{tahun}/", response_model=schemas.ViewTilangSatker, status_code=status.HTTP_200_OK, tags=[schemas.Tags.rekap])
async def get_tilang_satker(
        kode_ins: str,
        tahun: int,
        bulan: int = Query(default=None),
        db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
        user = crud.get_user_by_username(db, username=token_data.username)
    except JWTError:
        raise credentials_exception

    tilang_satker = None
    if bulan is None:
        tilang_satker = crud.get_tilang_satker_tahun(
            db, kode_ins=kode_ins, tahun=tahun)
    elif bulan >= 1 and bulan <= 12:
        tilang_satker = crud.get_tilang_satker_bulan(
            db, kode_ins=kode_ins, bulan=bulan, tahun=tahun)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="invalid param")

    if tilang_satker is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="rekap tidak di temukan!")
    elif user is None:
        raise credentials_exception
    else:
        return tilang_satker

# endpoint 4


@router.get("/daftarperkara/setor/{kode_ins}/{payment_date}/{tipe}/{tahun}/{bulan}", response_model=List[schemas.ViewDaftarPerkaraSetor], status_code=status.HTTP_200_OK, tags=[schemas.Tags.daftarperkara])
async def get_daftar_perkara_setor(
        kode_ins: str,
        bulan: int,
        tahun: int,
        payment_date: str,
        tipe: str,
        # skip: int = 0,
        # limit: int = 100,
        limit: int = Query(default=5000),
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
        user = crud.get_user_by_username(db, username=token_data.username)
    except JWTError:
        raise credentials_exception

    daftar_perkara_setor = crud.get_daftar_perkara_setor(
        db,
        kode_ins=kode_ins,
        bulan=bulan,
        tahun=tahun,
        payment_date=payment_date,
        tipe=tipe,
        # skip=skip,
        limit=limit
    )

    if len(daftar_perkara_setor) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="perkara tidak di temukan")

    return daftar_perkara_setor


# endpoint 5


@router.get("/rekap/dataputusan/{kode_ins}/{tahun}/", response_model=schemas.ViewRekapDataPutusan, status_code=status.HTTP_200_OK, tags=[schemas.Tags.rekap])
async def get_rekap_data_putusan(
        kode_ins: str,
        tahun: int,
        triwulan: int = Query(default=0),
        semester: int = Query(default=0),
        db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
        user = crud.get_user_by_username(db, username=token_data.username)
    except JWTError:
        raise credentials_exception

    getdatarekap = None
    if tahun >= 2000 and triwulan == 0 and semester == 0:
        getdatarekap = crud.get_rekap_data_putusan_tahun(
            db, kode_ins=kode_ins, tahun=tahun)
    elif triwulan > 0 and triwulan <= 4 and tahun >= 2000 and semester == 0:
        getdatarekap = crud.get_rekap_data_putusan_triwulan(
            db, kode_ins=kode_ins, tahun=tahun, triwulan=triwulan)
    elif semester > 0 and semester <= 2 and tahun >= 2000 and triwulan == 0:
        getdatarekap = crud.get_rekap_data_putusan_semester(
            db, kode_ins=kode_ins, tahun=tahun, semester=semester)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="invalid param")
    if getdatarekap is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="rekap tidak di temukan!")
    elif user is None:
        raise credentials_exception
    else:
        return getdatarekap

# endpoint 8


@router.get("/briva/{kode}", response_model=List[schemas.ViewBriva], status_code=status.HTTP_200_OK, tags=[schemas.Tags.briva])
async def get_briva(kode: str, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):

    if len(kode) == 15 and re.match(r'^([\s\d]+)$', kode):

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"})

        getkode = crud.get_briva(db, kode=kode)
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = schemas.TokenData(username=username)
            user = crud.get_user_by_username(db, username=token_data.username)
        except JWTError:
            raise credentials_exception
        if user is None:
            raise credentials_exception
        elif getkode is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="kode tidak ditemui")

        return getkode
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="invalid param")


app.include_router(router)
