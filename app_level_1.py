from flask import Flask, render_template, request
from twilio.rest import Client
import mysql.connector

account_sid = '__AC61__639100b___7374e9__a727b8eeaf32__82533'
auth_token = 'bf54a37c7__f3ad886379__508e2c7a__3af0d'
client = Client(account_sid, auth_token)

app = Flask(__name__)

def createConnection(user_name, database_name, user_password, host, port):
    cnx = mysql.connector.connect(
        user=user_name, database=database_name, password=user_password, host=host, port=port)
    cursor = cnx.cursor()
    return (cnx, cursor)

# solamente recibimos datos del emulador virtual
@app.route('/sensor_data', methods=['POST'])
def receive_sensor_data():

    if request.headers['Content-Type'] == 'application/json':

        data = request.json

        humidity = str(data.get('humidity'))
        temperature = str(data.get('temperature'))
        date_time = data.get('date_time')

        print(humidity)
        print(temperature)
        print(date_time)
        # DB name, User name, password, host,  port
        cnx, cursor = createConnection('sql36___78867', 'sql36___78867___', 'JlY___RKX9QNL', 'sql3.freemys___qlhosting.net', '3306')

        add_data = ("INSERT INTO dht_sensor_data (humidity, temperature, date_time) VALUES ("+temperature+","+humidity+",'"+date_time+"')")
        
        cursor.execute(add_data)
        cnx.commit()
        cursor.close()
        cnx.close()
    
        message = client.messages.create(
        from_='whatsapp:+14155238886',
        body='Humedad: '+humidity+" temperatura:"+temperature,
        to='whatsapp:+5215514200581'
        )
        print(message.sid)

        return 'Data received successfully.', 200
    else:
        return 'Invalid content type. Expected application/json.', 0

# solamente mostramos la Pagina Web
@app.route("/" , methods=['GET'])
def hello_world():
    message = client.messages.create(
    from_='whatsapp:+14155238886',
    body='Servicio activado ',
    to='whatsapp:+5215514200581'
    )
    print(message.sid)
    return render_template('index.html')
