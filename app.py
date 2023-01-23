from flask import Flask, render_template, request, redirect
from sqlalchemy import Column, INTEGER, String, select
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import random

Base = declarative_base()
engine = create_engine("sqlite:///url_data.db", echo=True)


app = Flask(__name__)

class URLData(Base):
    __tablename__ = "urls"

    id = Column(INTEGER, primary_key=True)
    url = Column(String)
    url_id = Column(String)

    def __repr__(self):
        return f"URL(id={self.id}, url={self.url}, url_id={self.url_id})"

def create_url_code():
    lowercase_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    uppercase_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    characters = lowercase_letters + uppercase_letters + numbers
    url_index = ""
    for i in range(10):
        url_index += random.choice(characters)
    if url_index in list_of_url_codes():
        create_url_code()
    else:
        return url_index

def list_of_url_codes():
    listofcodes = []
    with Session(engine) as session:
        all_query = session.query(URLData).all()
        for query in all_query:
            listofcodes.append(query.url_id)
    return listofcodes



@app.route('/', methods=["GET", 'POST'])
def home():
    if request.method == "POST":
        url = request.form.get('url')
        url_code = create_url_code()
        with Session(engine) as session:
            new_url = URLData(url=url, url_id=url_code)
            session.add(new_url)
            session.commit()
        return f"/{url_code}"
    return render_template('index.html')

@app.route('/r/<id>')
def redirect_id(id):
    print(id)
    with Session(engine) as session:
        data = select(URLData).where(URLData.url_id == id)
        datas = session.scalars(data).one()
        url = datas.url   
    return redirect(url)

if __name__ == "__main__":
    app.run()