import socket
import json

def enviar_tarea(accion, datos_tarea):
    payload = {
        "accion": accion,
        "datos": datos_tarea
    }
    
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(('localhost', 5000)) # Se conecta al servidor
    
    print(f"[CLIENTE] Enviando tarea técnica (JSON): {payload}")
    
    mensaje_codificado = (json.dumps(payload) + "\n").encode()
    cliente.send(mensaje_codificado)
    
    respuesta_raw = cliente.recv(4096).decode()
    try:
        respuesta_json = json.loads(respuesta_raw)
        print(f"[CLIENTE] Respuesta del Servidor: {respuesta_json['mensaje']}")
        if "worker" in respuesta_json:
            print(f"[CLIENTE] Operario a cargo: {respuesta_json['worker']}")
    except json.JSONDecodeError:
        print(f"[CLIENTE] Respuesta sin formato recibida: {respuesta_raw}")
        
    cliente.close()

if __name__ == "__main__":
    nueva_tarea_ti = {
        "titulo": "Configurar servidor de producción",
        "prioridad": "Alta",
        "id_usuario": 142
    }

    enviar_tarea("REGISTRAR_TAREA", nueva_tarea_ti)