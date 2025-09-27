# Proyecto-2
Documentación de Simulador de Procesos

1. Descripción general
   Reas.me es una aplicación en Python que permite gestionar, planificar y analizar procesos de manera interactiva, incluyendo simulación de algoritmos de planificación (FCFS, SJF, SRTF y Round Robin) con diagramas de Gantt y métricas de rendimiento.

2. Requisitos
   2.1 Software

* Python 3.10+
* Sistema operativo: Windows, macOS o Linux

2.2 Librerías de Python

* tkinter: Interfaz gráfica
* matplotlib: Gráficos y diagramas de Gantt
* pandas: Manejo de datos y métricas
* functools: Uso de partial para botones
* random: Colores aleatorios para procesos

Instalación de librerías:

```
pip install matplotlib pandas
```

(tkinter viene por defecto en Python)

3. Instalación
4. Descargar o clonar el proyecto.
5. Abrir terminal en la carpeta del proyecto.
6. Ejecutar:

```
python main.py
```

4. Se abrirá la ventana de interfaz gráfica para agregar, eliminar y ejecutar procesos.

5. Funcionalidades principales

* Agregar proceso (nombre, llegada, duración)
* Eliminar proceso
* Visualizar lista de procesos
* Simular algoritmos de planificación
* Modificar Quantum para Round Robin
* Visualización de:

  * Diagrama de Gantt
  * CPU en tiempo real
  * Tabla de métricas de procesos

5. Estructura del código

```
Procesos/
├── app.py
├── SCSF.py
├── SJF.py
├── ROUN ROBIN.py
├── SRTF.py
├── README.md
```

5.1 Clase Proceso

```
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
```

5.2 Funciones de planificación

* FCFS, SJF, SRTF, Round Robin.
* Retornan `historial` y `procesos` con métricas actualizadas.

  <img width="297" height="443" alt="image" src="https://github.com/user-attachments/assets/39d2bda9-54f1-4cff-8423-d5dcba4afe37" />

<img width="1900" height="900" alt="image" src="https://github.com/user-attachments/assets/0c6ae617-2c84-409c-ae1f-8769b5f5f4a8" />
<img width="1900" height="900" alt="image" src="https://github.com/user-attachments/assets/0ff9ca3d-9182-45ab-adb9-0fe35c242b72" />
<img width="1900" height="900" alt="image" src="https://github.com/user-attachments/assets/8b90098d-dff1-4ef3-8cf8-c79f673ab1a5" />
<img width="1900" height="900" alt="image" src="https://github.com/user-attachments/assets/f5d2f715-53b8-4963-822b-221854ba2394" />



5.3 Función animar

* Genera diagramas de Gantt, barra de CPU y tabla de métricas usando pandas.

5.4 Interfaz gráfica (Tkinter)

* Lista de procesos (Listbox)
* Botones Agregar/Eliminar (Button + simpledialog)
* Entrada de Quantum (Entry con validación)
* Botones de ejecución de algoritmos

6. Ejemplo de uso

7. Ejecutar `python main.py`

8. Ver procesos de prueba

9. Cambiar quantum si se desea

10. Ejecutar Round Robin

11. Ver animación y tabla de métricas

12. Buenas prácticas

* Nombres únicos para procesos
* No dejar campos vacíos
* Ajustar quantum según número de procesos
* Aumentar intervalo_ms para animaciones grandes
