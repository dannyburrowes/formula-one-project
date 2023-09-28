from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
import requests

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///formula.db"
db.init_app(app)

class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    season: Mapped[str] = mapped_column(String)
    round: Mapped[str] = mapped_column(String)
    raceName: Mapped[str] = mapped_column(String)
    circuitId: Mapped[str] = mapped_column(String)
    date: Mapped[str] = mapped_column(String)
    number: Mapped[str] = mapped_column(String)
    position: Mapped[str] = mapped_column(String)
    driverId: Mapped[str] = mapped_column(String)
    permanentNumber: Mapped[str] = mapped_column(String)
    givenName: Mapped[str] = mapped_column(String)
    familyName: Mapped[str] = mapped_column(String)
    nationality: Mapped[str] = mapped_column(String)
    constructorId: Mapped[str] = mapped_column(String)
    Q1: Mapped[str] = mapped_column(String)
    Q2: Mapped[str] = mapped_column(String)
    Q3: Mapped[str] = mapped_column(String)


def AddingData():
    data = requests.get(f"http://ergast.com/api/f1/qualifying.json?limit=10000&offset=9000").json()

    data2 = data['MRData']['RaceTable']['Races']

    for i in range(7, len(data2)):
        formula_data = User(
            season=data['MRData']['RaceTable']['Races'][i]["season"],
            round=data['MRData']['RaceTable']['Races'][i]["round"],
            raceName=data['MRData']['RaceTable']['Races'][i]["raceName"],
            circuitId=data['MRData']['RaceTable']['Races'][i]["Circuit"]["circuitId"],
            date=data['MRData']['RaceTable']['Races'][i]["date"],
            number=data['MRData']['RaceTable']['Races'][i]["QualifyingResults"][0]["number"],
            position=data['MRData']['RaceTable']['Races'][i]["QualifyingResults"][0]["position"],
            driverId=data['MRData']['RaceTable']['Races'][i]["QualifyingResults"][0]["Driver"]["driverId"],
            permanentNumber=data['MRData']['RaceTable']['Races'][i]["QualifyingResults"][0]["Driver"]["permanentNumber"],
            givenName=data['MRData']['RaceTable']['Races'][i]["QualifyingResults"][0]["Driver"]["givenName"],
            familyName=data['MRData']['RaceTable']['Races'][i]["QualifyingResults"][0]["Driver"]["familyName"],
            nationality=data['MRData']['RaceTable']['Races'][i]["QualifyingResults"][0]["Driver"]["nationality"],
            constructorId=data['MRData']['RaceTable']['Races'][i]["QualifyingResults"][0]["Constructor"]["constructorId"],
            Q1=data['MRData']['RaceTable']['Races'][i]["QualifyingResults"][0]["Q1"],
            Q2=data['MRData']['RaceTable']['Races'][i]["QualifyingResults"][0]["Q2"],
            Q3=data['MRData']['RaceTable']['Races'][i]["QualifyingResults"][0]["Q3"],
        )
        db.session.add(formula_data)
        db.session.commit()

@app.route("/")
def hello_world():
    users = User.query.order_by(User.season).all()
    driver = ""
    for i in users:
        driver += "<p>" + i.givenName + " - " + i.constructorId + " - " + i.season + "</p>"
    return driver


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        db.session.query(User).delete()
        AddingData()
    app.run(debug=True)

