from sqlalchemy import create_engine
from model import Base
from app import App

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base.metadata.create_all(engine)

app = App(engine)
app.run()
