from flask import Flask, render_template, request
from twilio.rest import Client
import mysql.connector
import matplotlib.pyplot as plt
from io import BytesIO
import base64

account_sid = 'AC61639100b7374e9a727b8eeaf3282533'
auth_token = 'bf54a37c7f3ad886379508e2c7a3af0d'
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
        cnx, cursor = createConnection('sql3678867', 'sql3678867', 'JlYRKX9QNL', 'sql3.freemysqlhosting.net', '3306')

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
        # Create a connection to the database
    cnx, cursor = createConnection('sql3678867', 'sql3678867', 'JlYRKX9QNL', 'sql3.freemysqlhosting.net', '3306')

    # Query the database
    query = ("SELECT * FROM dht_sensor_data")

    # Execute the query
    cursor.execute(query)

    # Get the data
    data = cursor.fetchall()

    # Close the connection
    cursor.close()
    cnx.close()

        # Obtener los valores de x e y desde los datos
    x = [item[0] for item in data]
    y1 = [item[1] for item in data]
    y2 = [item[2] for item in data]

    # Crear la gráfica
    plt.figure(figsize=(8, 4))
    plt.plot(x, y1, label='Valor 1')
    plt.plot(x, y2, label='Valor 2')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()

    # Guardar la gráfica en un archivo temporal
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_data = base64.b64encode(img.getvalue()).decode()

    # Renderizar la plantilla HTML con la gráfica
    return render_template('graph.html', img_data=img_data)

    # Return the data
    # return , 200
