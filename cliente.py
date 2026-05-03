import socket

def enviar_tarea(descripcion):
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(('localhost', 5000)) # Le pide al Servidor Central
    
    print(f"[CLIENTE] Enviando tarea: {descripcion}")
    cliente.send(descripcion.encode())
    
    resultado = cliente.recv(1024).decode()
    print(f"[CLIENTE] Respuesta recibida: {resultado}")
    cliente.close()

if __name__ == "__main__":
    enviar_tarea("REGISTRAR_GATO: 'Simba', 3 años, Vacunas al día")