#include <Arduino.h>
#include <Servo.h>
// #include <HardwareSerial.h>

Servo myservo;
int incomingByte = 0;  // Serial'den gelecek olan veri
int old_angle = 0; // Son hedef açısı

void setup() {
  myservo.attach(9);  // Servo motorun bağlı olduğu pin
  Serial.begin(9600); // Seri haberleşmeyi başlat
  myservo.write(90);   // Servoyu başlangıç pozisyonuna getir
}

void loop() {
  if (Serial.available() > 0) {
    incomingByte = Serial.read(); // Seriden gelen veriyi oku
    Serial.print("--------------------\n");
    // incomingByte'ı yazdır ve ardından açıklamayı yazdır
    myservo.write(incomingByte);
    Serial.print("Incoming Byte: ");
    Serial.println(incomingByte);
    delay(50);
    
    // if (incomingByte == old_angle) {
    //   myservo.write(incomingByte);
    //   delay(50);
    //   Serial.print("Incoming Byte: ");
    //   Serial.println(incomingByte);
    // }

    // else if (incomingByte > old_angle) {
    //   for (int i = old_angle; i < incomingByte; i+=3) {
    //     myservo.write(i);
    //     delay(50);
    //     Serial.print("i: ");
    //     Serial.println(i);
    //   }
    // }

    // else if (incomingByte < old_angle) {
    //   for (int i = old_angle; i > incomingByte; i-=3) {
    //     myservo.write(i);
    //     delay(50);
    //     Serial.print("i: ");
    //     Serial.println(i);
    //   }
    // }
    // old_angle = incomingByte; // Hedef açıyı güncelle
  }
}
