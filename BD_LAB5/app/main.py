from app import models
from datetime import datetime
from sqlalchemy.orm import selectin_polymorphic
from sqlalchemy import  exists, select
from fastapi import FastAPI, Depends, HTTPException, status, Response, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, SessionLocal
from .models import Transaction, VoteTransaction, ResultTransaction
from . import models
import zipfile
import csv
import io
from datetime import datetime
from pydantic import BaseModel

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


session = SessionLocal()
session.commit()


@app.post("/load_data_from_archive")
async def load_data_from_archive(archive_path: str):
    with zipfile.ZipFile(archive_path, 'r') as zip_ref:
        for file_name in zip_ref.namelist():
            with zip_ref.open(file_name) as file:
                if file_name.endswith('.csv'):
                    csv_reader = csv.reader(io.TextIOWrapper(file, encoding='utf-8'))
                    next(csv_reader)  # Пропустить первую строку с заголовками столбцов
                    for row in csv_reader:
                        transaction = Transaction(
                            signature=row[0],
                            datetime=datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S'),  # Замените формат на соответствующий вашим данным
                            type=row[2]
                        )
                        session.add(transaction)
        session.commit()
    return {"message": "Data loaded from archive successfully"}

@app.post('/bulletin')
def add_bulletin(signature: str):
    bulletin_transaction = Transaction(signature=signature, datetime=datetime.now())
    session.add(bulletin_transaction)
    session.commit()
    return {'message': 'Bulletin added successfully'}


@app.post('/bulletin/{bulletin_id}/vote')
def add_vote(bulletin_id: int, candidate_number: int):
    bulletin_transaction = session.query(Transaction).get(bulletin_id)
    if not bulletin_transaction:
        return {'message': 'Bulletin transaction not found'}
    if bulletin_transaction.type == 'vote' or bulletin_transaction.type == 'res':
        return {'message': 'Error'}
    vote_exists = session.query(exists().where(VoteTransaction.bulletin_id == bulletin_id)).scalar()
    if vote_exists:
        return {'message': 'You have already voted'}
    cand_res_exists = session.query(exists().where(ResultTransaction.candidate_number == candidate_number)).scalar()
    if cand_res_exists:
        return {'message': 'Results have finished'}
    vote_transaction = VoteTransaction(signature=bulletin_transaction.signature, datetime=datetime.now(),
                                       candidate_number=candidate_number, bulletin_id=bulletin_id)
    session.add(vote_transaction)
    session.commit()
    return {'message': 'Vote added successfully'}


@app.post('/votes/count/{candidate_number}')
def count_votes(signature: str, candidate_number: int):
    vote_count = session.query(VoteTransaction).filter_by(candidate_number=candidate_number).count()
    if vote_count==0:
        return {'message': 'Candidate does not exists!'}
    cand_exists = session.query(exists().where(ResultTransaction.candidate_number == candidate_number)).scalar()
    if cand_exists:
        return {'message': 'Results for cand have finished'}
    res = ResultTransaction(signature=signature, datetime=datetime.now(), candidate_number=candidate_number,
                            vote_count=vote_count)
    session.add(res)
    session.commit()
    return {'candidate_number': candidate_number, 'vote_count': vote_count}

from sqlalchemy.orm import subqueryload

from sqlalchemy.orm import subqueryload

@app.get('/transactions')
def get_transactions():
    loader_opt = selectin_polymorphic(Transaction, [VoteTransaction, ResultTransaction])
    stmt = select(Transaction).options(loader_opt)
    objects = session.scalars(stmt).all()
    return objects


@app.get('/results')
def get_results():
    results = session.query(ResultTransaction).all()
    if results == None:
        return {'message': 'no data'}
    result_list = []
    max_vote_count = 0
    winner = None
    for result in results:
        result_dict = result.as_dict()
        result_list.append(result_dict)
        if result.vote_count > max_vote_count:
            max_vote_count = result.vote_count
            winner = result.candidate_number

    draw = False
    for result in results:
        if result.vote_count == max_vote_count and result.candidate_number != winner:
            draw = True
            break
    return {'results': result_list, 'winner': winner, 'draw': draw}


from datetime import date

@app.get('/transactions/count')
def count_transactions(start_date: date, end_date: date):
    start_time = datetime.combine(start_date, datetime.min.time())
    end_time = datetime.combine(end_date, datetime.max.time())

    transactions = session.query(Transaction).filter(Transaction.datetime >= start_time,
                                                     Transaction.datetime <= end_time).all()
    transaction_count = len(transactions)

    return {'transaction_count': transaction_count}