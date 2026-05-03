import socket

def distribuir_a_worker(tarea):
    # El servidor central se conecta al worker para pasarle la posta 
    try:
        s_worker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_worker.connect(('localhost', 6000))
        s_worker.send(tarea.encode())
        respuesta = s_worker.recv(1024).decode()
        s_worker.close()
        return respuesta
    except ConnectionRefusedError:
        return "Error: No hay workers disponibles."

def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('localhost', 5000)) # El cliente le pega al 5000
    servidor.listen(5)
    print("Servidor Central (Balanceador) activo en puerto 5000...")

    while True:
        conn, addr = servidor.accept()
        tarea = conn.recv(1024).decode()
        print(f"[RECEPTOR] Tarea recibida de cliente: {tarea}")
        
        # Distribuye la tarea 
        resultado = distribuir_a_worker(tarea)
        
        conn.send(resultado.encode())
        conn.close()

if __name__ == "__main__":
    iniciar_servidor()