from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, exists, select
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from .database import SessionLocal, Base, engine

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    signature = Column(String(255), nullable=False)
    datetime = Column(DateTime, nullable=False)
    type = Column(String(50))
    __mapper_args__ = {
        'polymorphic_identity': 'bulletin',
        'polymorphic_on': type
    }
    def as_dict(self):
        return {
            'id': self.id,
            'signature': self.signature,
            'datetime': self.datetime,
            'type': self.type
        }



class VoteTransaction(Transaction):
    __tablename__ = 'vote_transactions'
    id = Column(Integer, ForeignKey('transactions.id', ondelete='CASCADE'), primary_key=True)
    bulletin_id = Column(Integer, unique=True)
    candidate_number = Column(Integer)
    __mapper_args__ = {
        'polymorphic_identity': 'vote'
    }

    def as_dict(self):
        transaction_dict = super().as_dict()
        transaction_dict['bulletin_id'] = self.bulletin_id
        transaction_dict['candidate_number'] = self.candidate_number
        return transaction_dict



class ResultTransaction(Transaction):
    __tablename__ = 'result_transactions'
    id = Column(Integer, ForeignKey('transactions.id', ondelete='CASCADE'), primary_key=True)
    vote_count = Column(Integer)
    candidate_number = Column(Integer,unique = True)
    __mapper_args__ = {
        'polymorphic_identity': 'res'
    }

    def as_dict(self):
        result_dict = super().as_dict()
        result_dict['vote_count'] = self.vote_count
        result_dict['candidate_number'] = self.candidate_number
        return result_dict