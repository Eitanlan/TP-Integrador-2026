Nombre del Proyecto: Parking Barrier and car counter

Integrantes del Proyecto: Lisandro Cabrera; Daniel Zilberberg; Eitan Landenberg

De que se trata: Este proyecto consiste en que mediante dos sensores ultrasonicos y un servo se simule un estacionamiento donde segun el orden en el que los autos son detectados por los sensores, el arduino determina si entra o sale y se lo comunica a python. En python se muestra en una interfaz grafica la diferencia de autos entre el comienzo del programa y ese momento, los movimientos y el estado de la barrera. En la interfaz hay un boton que abre o cierra la barrera segun su estado actual

Componentes usados: Usamos dos sensores ultrasonicos de 4 pines en el primer sensor conectamos el trig a 2 y el echo 3 y en el otro calculamos el trig a 4 y el echo a 5. Tambien usamos un servomotor donde conectamos el pin de senal a 9

Como funciona la comunicacion: Lo que le manda Arduino a Python: "BARRERA LEVANTADA" cuando un sensor detecta a un auto; "BARRERA BAJA" cuando el auto termino de cruzar y lo detecto el otro sensor; "ENTRA" cuando el auto fue detectado primero por el sensor A y despues por el B; "SALE" cuando el auto fue detectado primero por el sensor B y despues por el A
			       Lo que le manda Python a Arduion: "BOTON" cuando haces click en el boton de la interfaz para levantar o bajar la barrera segun el estado actual

Como ejecutarlo: Para correr el proyecto desde WSL, primero conectamos el Arduino Uno por USB y desde el Arduino IDE de Windows subimos el codigo a la placa y cerramos el Monitor Serie. Despues abrimos PowerShell como administrador en Windows, ejecutamos usbipd list para ver el BUSID del Arduino y lo pasamos a Linux usando usbipd bind --busid [ID] y usbipd attach --wsl --busid [ID]. Ya en la terminal de WSL instalamos las librerias necesarias corriendo sudo apt update && sudo apt install python3-pip python3-tk -y y pip3 install pyserial, le damos permisos al puerto serie con sudo chmod 666 /dev/ttyACM0 (verificando en el codigo de Python que coincida el nombre del puerto) y por ultimo ejecutamos python3 archivo_python_interfaz.py para abrir la interfaz grafica

Capturas:
<img width="1382" height="1176" alt="Screenshot 2026-11-18 120311" src="https://github.com/user-attachments/assets/3bfc819e-9d81-473d-b01f-8668882751ed" />
<img width="1390" height="1186" alt="Screenshot 2026-11-18 120231" src="https://github.com/user-attachments/assets/040ccc7c-da21-43a3-947e-b1b541d6650f" />
<img width="1388" height="1176" alt="Screenshot 2026-11-18 120216" src="https://github.com/user-attachments/assets/b35b845f-28fa-4cb3-bfe5-8618bfd11553" />
<img width="1374" height="1178" alt="Screenshot 2026-11-18 120157" src="https://github.com/user-attachments/assets/cd709d16-e88b-4334-bf3a-1e5290602296" />
<img width="1376" height="1174" alt="Screenshot 2026-11-18 120140" src="https://github.com/user-attachments/assets/7ea155fa-741c-4f00-bad8-9615acf3386c" />
<img width="1388" height="1178" alt="Screenshot 2026-11-18 120128" src="https://github.com/user-attachments/assets/c6326849-14e7-40f3-ba08-4ee2ec813e5a" />
<img width="1356" height="1154" alt="Screenshot 2026-11-18 120959" src="https://github.com/user-attachments/assets/4bc1a113-d802-4e98-ad47-ab0c0fd68cc1" />

Cambios: En la interfaz grafica de python con tkinter se agrego un boton que envia "BOTON" al arduino y el arduino segun el estado de la barrera, la baja o la levanta. "BOTON" es el unico mensaje que envia python al arduino


