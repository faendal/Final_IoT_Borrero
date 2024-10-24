#include <Arduino.h>
#include <ClosedCube_HDC1080.h>

#define SOIL_MOISTURE_PIN A0

int estado = 0;
double temperatura = 0;
double humedad_aire = 0;
double medicion_humedad_tierra = 0;
double humedad_tierra = 0;

ClosedCube_HDC1080 sensorHT;

void setup() 
{
    Serial.begin(115200);
    sensorHT.begin(0x40);

    Serial.println("");

    estado = 1;
}

void loop()
{
    switch (estado)
    {
        case 1:
            for (int i = 0; i < 5; i++)
            { 
                temperatura += sensorHT.readTemperature();
                delay(100);
            }
            temperatura = temperatura / 5.0;
            estado = 2;
            break;

        case 2:
            for (int i = 0; i < 5; i++)
            { 
                humedad_aire += sensorHT.readHumidity();
                delay(100);
            }
            humedad_aire = humedad_aire / 5.0;
            estado = 3;
            break;
        
        case 3:
            for (int i = 0; i < 5; i++)
            { 
                medicion_humedad_tierra = analogRead(SOIL_MOISTURE_PIN);
                humedad_tierra += map(medicion_humedad_tierra, 0, 1023, 0, 100);
                delay(100);
            }
            humedad_tierra = humedad_tierra / 5.0;
            estado = 4;
            break;

        
        case 4:
            Serial.println("Variables medidas:");
            Serial.println("Temperatura: " + String(temperatura) + "°C");
            Serial.println("Humedad del aire: " + String(humedad_aire) + "%");
            Serial.println("Humedad de la tierra: " + String(humedad_tierra) + "%");
            delay(500);
            estado = 5;
            break;
        
        case 5:
            temperatura = 0;
            humedad_aire = 0;
            humedad_tierra = 0;
            delay(500);
            estado = 1;
            break;
    }
}