#include <Servo.h>

// Definicion de pines
const int trigA = 2, echoA = 3;
const int trigB = 4, echoB = 5;
const int pinServo = 9;

// Parametros de deteccion (en cm)
const int distanciaActivacion = 10;
const int distanciaMaxima = 20;

Servo barrera;

// Variables de estado
bool anteriorA = false;
bool anteriorB = false;
bool barreraAbierta = false;
int primero = 0; // 0: libre, 1: sentido A->B (Entrada), 2: sentido B->A (Salida)

long medirDistancia(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duracion = pulseIn(echoPin, HIGH, 30000);
  long distancia = duracion * 0.034 / 2;

  if (distancia == 0 || distancia > distanciaMaxima) {
    return 0;
  }
  return distancia;
}

void setup() {
  Serial.begin(9600);

  pinMode(trigA, OUTPUT);
  pinMode(echoA, INPUT);
  pinMode(trigB, OUTPUT);
  pinMode(echoB, INPUT);

  barrera.attach(pinServo);
  barrera.write(0);
}

void loop() {
  // Control manual desde interfaz Python
  if (Serial.available() > 0) {
    String mensaje = Serial.readStringUntil('\n');
    mensaje.trim();

    if (mensaje == "BOTON") {
      barreraAbierta = !barreraAbierta;

      if (barreraAbierta) {
        barrera.write(90);
        Serial.println("BARRERA LEVANTADA");
      } else {
        barrera.write(0);
        primero = 0;
        Serial.println("BARRERA BAJA");
      }
    }
  }

  // Lectura de sensores
  long distA = medirDistancia(trigA, echoA);
  long distB = medirDistancia(trigB, echoB);

  bool detectaA = (distA > 0 && distA <= distanciaActivacion);
  bool detectaB = (distB > 0 && distB <= distanciaActivacion);

  // Control de sentido y accionamiento de barrera
  if (primero == 0) {
    if (detectaA && !anteriorA) {
      primero = 1;
      barreraAbierta = true;
      barrera.write(90);
      Serial.println("BARRERA LEVANTADA");
    } else if (detectaB && !anteriorB) {
      primero = 2;
      barreraAbierta = true;
      barrera.write(90);
      Serial.println("BARRERA LEVANTADA");
    }
  } 
  else if (primero == 1) {
    if (!detectaB && anteriorB) {
      barreraAbierta = false;
      barrera.write(0);
      primero = 0;
      Serial.println("BARRERA BAJA");
      Serial.println("ENTRA");
    }
  } 
  else if (primero == 2) {
    if (!detectaA && anteriorA) {
      barreraAbierta = false;
      barrera.write(0);
      primero = 0;
      Serial.println("BARRERA BAJA");
      Serial.println("SALE");
    }
  }

  anteriorA = detectaA;
  anteriorB = detectaB;

  delay(50);
}