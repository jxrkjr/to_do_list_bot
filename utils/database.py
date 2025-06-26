from sqlalchemy import (create_engine, Column, Integer,
                        String, BigInteger, Boolean, DateTime, func, ForeignKey)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from data.config import PG_USER, PG_PASS, PG_HOST, PG_PORT, PG_DB

engine = create_engine(f'postgresql+psycopg2://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DB}')

Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

class Users(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    fullname = Column(String)
    chat_id = Column(BigInteger, unique=True, index=True)
    phone_number = Column(String)
    password = Column(String)
    tasks = relationship('Tasks', back_populates='user')
    def save(self , session):
        session.add(self)
        session.commit()

    @classmethod
    def check_register(cls, session, id_):
        obj = session.query(cls).filter(id_ == cls.chat_id).first()
        if not obj:
            return False
        return True
    def __repr__(self):
        return f'<User {self.fullname} , {self.chat_id} , {self.phone_number} , {self.password}>'
class Tasks(Base):
    __tablename__ = 'tasks'
    id = Column(BigInteger, primary_key=True)
    chat_id = Column(BigInteger , ForeignKey('users.chat_id'))
    task_text = Column(String)
    is_done = Column(Boolean)
    user = relationship('Users', back_populates='tasks')
    def save(self , session):
        session.add(self)
        session.commit()
    def __repr__(self):
        status = "✅" if self.is_done else "❌"
        return f"<Task(id={self.id}, user={self.chat_id}, status={status})>"

    @classmethod
    def get_user_tasks(cls, session, chat_id: int):
        return session.query(cls).filter_by(chat_id=chat_id).all()

    @classmethod
    def mark_done(cls, session, task_id: int):
        task = session.query(cls).get(task_id)
        if task:
            task.is_done = True
            session.commit()