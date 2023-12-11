import smtplib
from decouple import config
import psutil
import time
from memory_profiler import profile
import paho.mqtt.client as mqtt
from pymongo import MongoClient

#Configuracion Mongo

mongo_client = MongoClient("mongodb://localhost:27017/")  # Cambia la URL de conexión según tu configuración
db = mongo_client["rendimiento"]
collection = db["mensajes"]

# Configuración del servidor HiveMQ
host = "broker.hivemq.com"  # Puedes cambiarlo si es necesario
port = 1883
topic = "Bad_boys"  

# Inicialización del cliente MQTT
mqtt_client = mqtt.Client()

# Conexión al servidor MQTT
mqtt_client.connect(host, port, 60)

#funcion que guarda los mensajes en mongo
def guardar_mensaje_en_mongo(mensaje):
    collection.insert_one({"mensaje": mensaje, "timestamp": time.time()})

def obtener_porcentaje_uso_cpu():
    porcentaje = psutil.cpu_percent(interval=1)
    return porcentaje


@profile
def my_function():
    a = [1] * (10 ** 6)
    b = [2] * (2 * 10 ** 7)
    del b
    return a

def monitor_network(interval=1, duration=10):
    print("Monitoring network performance...")
    end_time = time.time() + duration

    while time.time() < end_time:
        net_stats = psutil.net_io_counters()
        mensaje = f"Bytes enviados: {net_stats.bytes_sent} | Bytes recibidos: {net_stats.bytes_recv}"
        print(mensaje)
        mqtt_client.publish(topic, mensaje)
        guardar_mensaje_en_mongo(mensaje)
        #metadatos
        # guardar_mensaje_en_mongo(mensaje, equipo)
        time.sleep(interval)

def monitor_cpu(interval=1, duration=10):
    print("Monitoring CPU performance...")
    end_time = time.time() + duration

    while time.time() < end_time:
        cpu_percent = psutil.cpu_percent(interval=interval)
        mensaje = f"Uso de CPU: {cpu_percent}%"
        print(mensaje)
        mqtt_client.publish(topic, mensaje)
        guardar_mensaje_en_mongo(mensaje)
        #metadatos
        # guardar_mensaje_en_mongo(mensaje, equipo)
        time.sleep(interval)

if __name__ == "__main__":
    # Inicia el cliente MQTT en un hilo separado
    mqtt_client.loop_start()
    #(metadatos) Ejecuta las funciones de recopilación de información para cada equipo
    #equipos = ["Equipo1", "Equipo2"]

    # Ejecuta las funciones de recopilación de información
    #for equipo in equipos:(metadatos)
    porcentaje_uso_cpu = obtener_porcentaje_uso_cpu()
    print(f"Porcentaje de uso de CPU: {porcentaje_uso_cpu}%")
    
    if porcentaje_uso_cpu > 40:
        
     #Se envia al correo la alerta cuando se sobrepase el 40%
     message='el porcentaje del cpu es superior al 40%'
     subject='alerta de rendimiento'
     message='Subject: {}\n\n{}'.format(subject, message)
     server=smtplib.SMTP('smtp.gmail.com',587)
     server.starttls()
     server.login('BryanDaviid333@gmail.com', 'ffco lbue izbz ryeh')
     server.sendmail('BryanDavid333@gmail.com','davidchalan54@gmail.com',message)
     server.quit()
     print('correo enviado de manera exitosa')
    

    my_function()

    monitor_network()

    monitor_cpu()
    #metadatos, reemplaza a las funciones de arriba
    #monitor_network(equipo=equipo)
    #monitor_cpu(equipo=equipo)

    # Espera a que las publicaciones MQTT se completen antes de salir
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
    
    #-------------------codigo para la maquina que recibe------------
    
    import paho.mqtt.client as mqtt

# Configuración del servidor HiveMQ
host = "broker.hivemq.com"  # Puedes cambiarlo si es necesario
port = 1883
topic = "Bad_boys"

# Callback cuando se recibe un mensaje
def on_message(client, userdata, msg):
    print(f"Mensaje recibido: {msg.payload.decode()}")

# Inicialización del cliente MQTT
client = mqtt.Client()
client.on_message = on_message

# Conexión al servidor MQTT
client.connect(host, port, 60)

# Suscripción al topic
client.subscribe(topic)

# Loop principal
client.loop_forever()
    
   