import socket
from concurrent.futures import ThreadPoolExecutor

# Configuración del Worker
def procesar_mision(tarea):
    print(f"[TRABAJANDO] Procesando: {tarea}")
    # Aquí simularíamos guardar en PostgreSQL o S3 
    return f"Resultado exitoso de: {tarea}"

def iniciar_worker(puerto):
    worker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    worker.bind(('localhost', puerto))
    worker.listen(1)
    print(f"Worker listo en el puerto {puerto}...")

    # Pool de hilos para manejar múltiples tareas 
    pool = ThreadPoolExecutor(max_workers=3)

    while True:
        conn, addr = worker.accept()
        tarea = conn.recv(1024).decode()
        # El pool de hilos se encarga del trabajo
        futuro = pool.submit(procesar_mision, tarea)
        respuesta = futuro.result() 
        conn.send(respuesta.encode())
        conn.close()

if __name__ == "__main__":
    iniciar_worker(6000) # El worker escucha en el 6000