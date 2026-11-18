#include <Servo.h>

const int trigA = 2, echoA = 3;
const int trigB = 4, echoB = 5;
const int pinServo = 9;

const int distanciaActivacion = 8;
const int distanciaMaxima = 20;

Servo barrera;

bool anteriorA = false;
bool anteriorB = false;
bool barreraAbierta = false;
int primero = 0;

unsigned long ultimoDisparoA = 0;
unsigned long ultimoDisparoB = 0;
const unsigned long cooldownSensor = 2000;

long medirDistancia(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duracion = pulseIn(echoPin, HIGH, 20000);
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
  
  barrera.write(130);
  delay(1000);
}

void loop() {
  if (Serial.available() > 0) {
    String mensaje = Serial.readStringUntil('\n');
    mensaje.trim();

    if (mensaje == "BOTON") {
      barreraAbierta = !barreraAbierta;

      if (barreraAbierta) {
        barrera.write(25);
        Serial.println("BARRERA LEVANTADA");
      } else {
        barrera.write(130);
        primero = 0;
        Serial.println("BARRERA BAJA");
      }
    }
  }

  long distA = medirDistancia(trigA, echoA);
  delay(15);
  long distB = medirDistancia(trigB, echoB);

  bool detectaA = (distA > 0 && distA <= distanciaActivacion);
  bool detectaB = (distB > 0 && distB <= distanciaActivacion);

  unsigned long tiempoActual = millis();

  if (primero == 0) {
    if (detectaA && !anteriorA && (tiempoActual - ultimoDisparoA > cooldownSensor)) {
      primero = 1;
      barreraAbierta = true;
      barrera.write(25);
      ultimoDisparoA = tiempoActual;
      Serial.println("BARRERA LEVANTADA");
    } 
    else if (detectaB && !anteriorB && (tiempoActual - ultimoDisparoB > cooldownSensor)) {
      primero = 2;
      barreraAbierta = true;
      barrera.write(25);
      ultimoDisparoB = tiempoActual;
      Serial.println("BARRERA LEVANTADA");
    }
  } 
  else if (primero == 1) {
    if (!detectaB && anteriorB) {
      barreraAbierta = false;
      barrera.write(130);
      primero = 0;
      Serial.println("BARRERA BAJA");
      Serial.println("ENTRA");
    }
  } 
  else if (primero == 2) {
    if (!detectaA && anteriorA) {
      barreraAbierta = false;
      barrera.write(130);
      primero = 0;
      Serial.println("BARRERA BAJA");
      Serial.println("SALE");
    }
  }

  anteriorA = detectaA;
  anteriorB = detectaB;

  delay(30);
}