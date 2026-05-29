import socket

PUERTOS_WORKERS = [6000, 6001]
contador_peticiones = 0

def distribuir_a_worker(payload_json):
    global contador_peticiones
    
    indice_worker = contador_peticiones % len(PUERTOS_WORKERS)
    puerto_elegido = PUERTOS_WORKERS[indice_worker]
    
    contador_peticiones += 1
    
    try:
        s_worker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_worker.connect(('localhost', puerto_elegido))
        
        print(f"[SERVIDOR CENTRAL] Derivando tarea técnica al Worker del puerto {puerto_elegido}...")
        s_worker.send(payload_json.encode())
        respuesta = s_worker.recv(4096).decode()
        s_worker.close()
        return respuesta
    except ConnectionRefusedError:
        return f'{{"status": "error", "mensaje": "Error: El Worker del puerto {puerto_elegido} no está activo."}}'

def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind(('localhost', 5000))
    servidor.listen(5)
    print("Servidor Central (Recepción) activo en puerto 5000. Esperando tareas...")

    while True:
        conn, addr = servidor.accept()
        payload_raw = conn.recv(4096).decode()
        
        if payload_raw:
            print("[SERVIDOR CENTRAL] Llegó una solicitud técnica desde un cliente...")
            resultado = distribuir_a_worker(payload_raw)
            conn.send(resultado.encode())
            
        conn.close()

if __name__ == "__main__":
    iniciar_servidor()