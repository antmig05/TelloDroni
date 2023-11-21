from djitellopy import TelloSwarm
import threading
import time

# Carica gli indirizzi IP da file
swarm1 = TelloSwarm.fromFile("ips1.txt")
swarm2 = TelloSwarm.fromFile("ips2.txt")

# Creare una barriera per sincronizzare i due thread
barrier = threading.Barrier(2)

def controllo_tello(tello, nome):
    try:
        tello.connect()
        tello.query_battery()
        print(f"[INFO] Connessione riuscita per {nome}")
    except Exception as e:
        print(f"[ERRORE] Connessione fallita per {nome}: {e}")
        return False

    return True

def takeoff_and_fly(tello, nome):
    try:
        print(f"[INFO] {nome}: In attesa della sincronizzazione...")
        # Aspetta che entrambi i droni siano pronti prima di continuare
        barrier.wait()

        print(f"[INFO] {nome}: Decollo in corso...")
        tello.takeoff()
        tello.move_up(200)
        tello.move_right(300)
        tello.move_up(100)
        tello.move_forward(45)
        tello.move_forward(200)
        tello.move_back(200)
        tello.move_left(300)
        tello.move_forward(200)
        tello.move_left(200)
        tello.land()
        tello.end()
        print(f"[INFO] {nome}: Volare completato.")
    except Exception as e:
        print(f"[ERRORE] {nome}: Errore durante il volo: {e}")
def takeoff_and_fly2(tello, nome):
    try:
        print(f"[INFO] {nome}: In attesa della sincronizzazione...")
        # Aspetta che entrambi i droni siano pronti prima di continuare
        barrier.wait()

        print(f"[INFO] {nome}: Decollo in corso...")
        tello.takeoff()
        tello.move_up(200)
        tello.move_left(300)
        tello.move_down(100)
        tello.move_back(45)
        tello.move_forward(200)
        tello.move_back(200)
        tello.move_right(300)
        tello.move_forward(100)
        tello.move_right(200)
        tello.land()
        tello.end()
     
        print(f"[INFO] {nome}: Volare completato.")
    except Exception as e:
        print(f"[ERRORE] {nome}: Errore durante il volo: {e}")
# Creare i thread di controllo
thread_controllo_1 = threading.Thread(target=controllo_tello, args=(swarm1, "Swarm1"))
thread_controllo_2 = threading.Thread(target=controllo_tello, args=(swarm2, "Swarm2"))

# Avvia i thread di controllo
thread_controllo_1.start()
thread_controllo_2.start()

# Attendi la fine dei thread di controllo
thread_controllo_1.join()
thread_controllo_2.join()

# Se entrambi i droni sono pronti, procedi con il volo
if thread_controllo_1.is_alive() or thread_controllo_2.is_alive():
    print("[ERRORE] Almeno uno dei droni non è pronto. Interrompiamo.")
else:
    # Creare i thread di volo
    thread_volo_1 = threading.Thread(target=takeoff_and_fly, args=(swarm1, "Swarm1"))
    thread_volo_2 = threading.Thread(target=takeoff_and_fly2, args=(swarm2, "Swarm2"))

    # Avvia i thread di volo
    thread_volo_1.start()
    thread_volo_2.start()

    # Attendi la fine dei thread di volo
    thread_volo_1.join()
    thread_volo_2.join()

print("Programma completato.")