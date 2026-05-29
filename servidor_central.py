import socket

def distribuir_a_worker(payload_json):
    try:
        s_worker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_worker.connect(('localhost', 6000)) # Conexión con el worker

        s_worker.send(payload_json.encode())
        respuesta = s_worker.recv(4096).decode()
        s_worker.close()
        return respuesta
    except ConnectionRefusedError:
        return "{\"status\": \"error\", \"mensaje\": \"Error: El sector de procesamiento no está activo.\"}"

def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind(('localhost', 5000)) # Recepción en el puerto 5000
    servidor.listen(5)
    print("Servidor Central (Recepción) activo en puerto 5000. Esperando tareas...")

    while True:
        conn, addr = servidor.accept()
        payload_raw = conn.recv(4096).decode()
        
        if payload_raw:
            print("[SERVIDOR CENTRAL] Llegó una solicitud técnica. Derivando al sector interno...")
            resultado = distribuir_a_worker(payload_raw)
            conn.send(resultado.encode())
            
        conn.close()

if __name__ == "__main__":
    iniciar_servidor()