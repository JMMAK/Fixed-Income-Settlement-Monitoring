from flask import Flask, render_template, request, send_from_directory, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, select

app = Flask(__name__)
# API CORS
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.sqlite3"
# create the DB extension
db = SQLAlchemy()
db.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


# Static files
@app.route("/assets/<path:filename>")
def assets(filename):
    return send_from_directory("templates/assets", filename)


# API
@app.route("/api/V1/deals", methods=["GET"])
def dealsAPI():
    entity = request.args.get("Entity")
    pta = request.args.get("PTA")
    isin = request.args.get("ISIN")
    sender_BIC = request.args.get("sender_BIC")
    settelment_Data = request.args.get("settelment_Data")
    matching_status = request.args.get("matching_status")

    page = request.args.get("page")
    pageSize = request.args.get("pageSize")
    dealCount = request.args.get("count")

    # SQL script
    if dealCount:
        stmt = select(func.count(Deals.PTA))
    else:
        stmt = select(Deals)
    # where
    if entity:
        stmt = stmt.where(Deals.Entity == entity)
    if pta:
        stmt = stmt.where(Deals.PTA == pta)
    if isin:
        stmt = stmt.where(Deals.ISIN == isin)
    if sender_BIC:
        stmt = stmt.where(Deals.sender_BIC == sender_BIC)
    if settelment_Data:
        stmt = stmt.where(Deals.settelment_Data == settelment_Data)
    if matching_status:
        stmt = stmt.where(Deals.matching_status == matching_status)

    if dealCount:
        count = db.session.execute(stmt).scalar()

        return jsonify({"dealCount": count})

    elif page and pageSize:
        returnJson = []
        offsetRecord = (int(page)-1) * int(pageSize)
        stmt = stmt.offset(offsetRecord).limit(int(pageSize))
        deals = db.session.execute(stmt).scalars().all()
        for deal in deals:
            deal = deal.__dict__
            deal.pop("_sa_instance_state")
            returnJson.append(deal)

        return jsonify(returnJson)


    return ''



# data Model
class Deals(db.Model):
    Entity = db.Column(db.String)
    PTA = db.Column(db.String, primary_key=True)
    ISIN = db.Column(db.String, unique=True)
    to_BIC = db.Column(db.String)
    sender_BIC = db.Column(db.String)
    settelment_Data = db.Column(db.String)
    matching_status = db.Column(db.String)


def insertDeals():
    deal = Deals(
        Entity="HK",
        PTA="123456789000",
        ISIN="123456789000",
        to_BIC="BICxxx",
        sender_BIC="BICxxx",
        settelment_Data="2016-00-00",
        matching_status="FLP",
    )

    for i in range(200):
        dealTemp = Deals(
            Entity=deal.Entity,
            PTA=str(int(deal.PTA) + i),
            ISIN=str(int(deal.ISIN) + i),
            to_BIC=deal.to_BIC,
            sender_BIC=deal.sender_BIC,
            settelment_Data=deal.settelment_Data,
            matching_status=deal.matching_status,
        )
        db.session.add(dealTemp)

    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
        insertDeals()

    app.run()
