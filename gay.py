from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from pymongo import MongoClient
from argparse import ArgumentParser
import sys
import click

client = MongoClient('localhost:5000')

members = client['member-db']

app = Flask(__name__)


@app.cli.command()
def test():
    click.echo('I am test')


@app.cli.command()
@click.argument('name')
def setpass(name):
    app.config['passcode'] = name


@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    resp = MessagingResponse()
    if request.method == 'POST':
        user = members['NetID']
        body = request.form['Body']
        date = request.form['date_sent']
        split_date = date.split()
        date = " ".join(split_date[1:4])
        netId = body.split[0]
        valid = app.config['passcode'] == body.split[1]
        loginUser = user.find_one({'NetID': netId})
        if valid and loginUser is None:
            usr = {
                "NetID": netId,
                "Meetings": 1,
                "Dates": [date]
            }
            members.insert_one(usr)
        elif valid:
            resp = MessagingResponse()
            user = client.members.find_one({'NetID': netId})
            dates = user["Dates"]
            if date in dates:
                newMeet = client.members.find({'NetID': netId}, {'Meetings': 1, "_id": 0}) + 1
                client.members.update_one({'NetID': netId}, {'Meetings': newMeet}, {'upsert': True})
                members.update_one({'NetID': netId}, {'$push': {'Meetings': date}})
            resp.message("Your response has been recorded, thank you!")

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
