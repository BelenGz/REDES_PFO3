import socket
import json
from concurrent.futures import ThreadPoolExecutor

BASE_DE_DATOS_TAREAS = []

def procesar_mision(payload_raw):
    try:
        data_parsed = json.loads(payload_raw)
        accion = data_parsed.get("accion")
        datos = data_parsed.get("datos")
        
        if accion == "REGISTRAR_TAREA":
            print("[WORKER - HILO ACTIVO] Leyendo datos de la tarea técnica...")
            print(f" -> Tarea: {datos.get('titulo')}")
            print(f" -> Prioridad: {datos.get('prioridad')}")
            print(f" -> ID Técnico: {datos.get('id_usuario')}")
            
            BASE_DE_DATOS_TAREAS.append(datos)
            print(f"[ALMACENAMIENTO] Tarea guardada. Total en el sistema de TI: {len(BASE_DE_DATOS_TAREAS)}")

            respuesta_servidor = {
                "status": "success",
                "mensaje": f"¡Tarea '{datos.get('titulo')}' registrada con éxito en el sistema distribuido!",
                "worker": "Worker_Puerto_6000_Threaded"
            }
            return json.dumps(respuesta_servidor)
        else:
            return json.dumps({"status": "error", "mensaje": "Acción no reconocida por el sistema"})
            
    except Exception as e:
        return json.dumps({"status": "error", "mensaje": f"Error en el procesamiento interno: {str(e)}"})

def iniciar_worker(puerto):
    worker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    worker.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    worker.bind(('localhost', puerto))
    worker.listen(5)
    print(f"Worker (Sector de Procesamiento) operativo en el puerto {puerto}...")

    pool = ThreadPoolExecutor(max_workers=5)

    while True:
        conn, addr = worker.accept()
        payload_raw = conn.recv(4096).decode()
        
        if payload_raw:
            futuro = pool.submit(procesar_mision, payload_raw)
            respuesta = futuro.result() 
            conn.send(respuesta.encode())
            
        conn.close()

if __name__ == "__main__":
    iniciar_worker(6000)