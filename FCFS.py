import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import pandas as pd

# === Clase Proceso ===
class Proceso:
    contador_pid = 1
    def __init__(self, nombre, llegada, duracion, quantum=None):
        self.pid = Proceso.contador_pid
        Proceso.contador_pid += 1
        self.nombre = nombre
        self.llegada = llegada
        self.duracion = duracion
        self.restante = duracion
        self.quantum = quantum
        self.finalizacion = 0
        self.retorno = 0
        self.espera = 0
        self.inicio = None

# === FCFS tick-a-tick (cola correcta y esperas por segundo) ===
def fcfs_tick(procesos):
    for p in procesos:
        p.restante = p.duracion
        p.espera = 0
        p.inicio = None
        p.finalizacion = 0
        p.retorno = 0

    tiempo = 0
    historial = []  # lista de (t, en_cpu_nombre|None, [(nombre_wait, pos)])
    cola = []
    current = None
    pendientes = sorted(procesos, key=lambda x: x.llegada)

    while pendientes or cola or current:
        # 1) llegan procesos
        while pendientes and pendientes[0].llegada == tiempo:
            cola.append(pendientes.pop(0))

        # 2) si CPU libre, tomar primero de la cola
        if current is None and cola:
            current = cola.pop(0)
            if current.inicio is None:
                current.inicio = tiempo

        # 3) sumar espera a los que siguen en cola
        for q in cola:
            q.espera += 1

        # 4) snapshot para animación
        esperas_con_pos = [(q.nombre, i+1) for i, q in enumerate(cola)]
        en_cpu_nombre = current.nombre if current else None
        historial.append((tiempo, en_cpu_nombre, esperas_con_pos))

        # 5) consumir CPU
        if current:
            current.restante -= 1

            # marcar finalización solo si terminó y el tick ya pasó
            if current.restante == 0:
                # fijar el tiempo de finalización como el tiempo actual
                current.finalizacion = tiempo +2
                current.retorno = current.finalizacion - current.llegada
                current = None


        # ⬇ Esto estaba mal indentado en tu código
        tiempo += 1
        
    return historial, procesos

# === Animación ===
def animar(procesos, intervalo_ms=1000, guardar=False):
    historial, resultados = fcfs_tick(procesos)
    colores = {p.nombre: (random.random(), random.random(), random.random()) for p in procesos}
    procesos_unicos = [p.nombre for p in procesos]
    tiempo_total = historial[-1][0] + 1 if historial else 0

    fig = plt.figure(figsize=(12, 8))
    gs = fig.add_gridspec(3, 1, height_ratios=[2, 1, 1.6])

    ax1 = fig.add_subplot(gs[0])  # Gantt
    ax2 = fig.add_subplot(gs[1])  # CPU
    ax3 = fig.add_subplot(gs[2])  # Tabla

    # Gantt
    ax1.set_yticks(range(len(procesos_unicos)))
    ax1.set_yticklabels(procesos_unicos)
    ax1.set_title("Diagrama de Gantt (gris = espera con posición, color = ejecución)")
    ax1.set_ylabel("Procesos")
    ax1.set_xlim(0, tiempo_total)
    ax1.grid(axis="x", linestyle="--", alpha=0.6)

    # CPU timeline
    ax2.set_yticks([])
    ax2.set_title("CPU en tiempo real")
    ax2.set_xlabel("Tiempo")
    ax2.set_xlim(0, tiempo_total)
    ax2.grid(axis="x", linestyle="--", alpha=0.6)

    # Tabla métricas
    data = {
        "PID": [p.pid for p in resultados],
        "Proceso": [p.nombre for p in resultados],
        "Llegada": [p.llegada for p in resultados],
        "Duración": [p.duracion for p in resultados],
        "Inicio": [p.inicio for p in resultados],
        "Espera": [p.espera for p in resultados],
        "Finalización": [p.finalizacion for p in resultados],
        "Retorno": [p.retorno for p in resultados],
    }
    df = pd.DataFrame(data)
    ax3.axis("off")
    tabla = ax3.table(cellText=df.values, colLabels=df.columns,
                      loc="center", cellLoc="center")
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(9)
    tabla.scale(1.2, 1.2)
    ax3.set_title("Métricas de Procesos", pad=8)

    # === Función de actualización ===
    def update(frame):
        t, en_cpu, esperas = historial[frame]
        for nombre, pos in esperas:
            idx = procesos_unicos.index(nombre)
            ax1.barh(idx, 1, left=t, color="lightgray", edgecolor="black")
            ax1.text(t + 0.5, idx, str(pos), ha="center", va="center", fontsize=8, color="black")

        if en_cpu:
            idx = procesos_unicos.index(en_cpu)
            ax1.barh(idx, 1, left=t, color=colores[en_cpu], edgecolor="black")
            ax2.barh(0, 1, left=t, color=colores[en_cpu], edgecolor="black")
            ax2.text(t + 0.5, 0, en_cpu, ha="center", va="center", fontsize=9, color="white")
        return []

    ani = animation.FuncAnimation(
        fig, update,
        frames=len(historial),
        interval=intervalo_ms,
        blit=False,
        repeat=False
    )

    # Guardar en archivo si se pide
    if guardar:
        ani.save("simulacion.mp4", writer="ffmpeg")  # necesitas ffmpeg instalado
        # ani.save("simulacion.gif", writer="pillow")

    plt.tight_layout()
    plt.show()

# === Ejemplo ===
if __name__ == "__main__":
    procesos = [
        Proceso("A", 1, 4),
        Proceso("B", 0, 2),
        Proceso("C", 3, 3),
        Proceso("D", 3, 1),
        Proceso("E", 3, 8),
        Proceso("F", 8, 2),
        Proceso("G", 6, 4),
    ]
    animar(procesos, intervalo_ms=800, guardar=False)
