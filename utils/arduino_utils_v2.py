import serial
import time

def write_read(x):
    try:
        arduino.write(bytes([x]))  # Tek bayt olarak veri gönder
        time.sleep(0.05)
        data = arduino.readline().decode('utf-8').strip()
        return data
    except serial.SerialException as e:
        print(f"SerialException: {e}")
        return None

def main():
    global arduino
    try:
        arduino = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=.1)
        
        angle_range = 20
        tour = 2
        
        # for _ in range(tour):
        while True:
            for angle_value in range(0, 180, angle_range):
                print(f"Sending: {angle_value}")
                scaled_value = int((angle_value / 180) * 255)
                data = write_read(scaled_value)
                if data:
                    print(f"Received: {data}")
                time.sleep(0.2)
            
            for angle_value in range(180, 0, -angle_range):
                print(f"Sending: {angle_value}")
                scaled_value = int((angle_value / 180) * 255)
                data = write_read(scaled_value)
                if data:
                    print(f"Received: {data}")
                time.sleep(0.2)
        
        # while True:
        #     angle = input("Servo açısını girin (0-180): ")  # Kullanıcıdan açı değeri alın
        #     if angle.isdigit():
        #         angle_value = int(angle)
        #         if 0 <= angle_value <= 180:
        #             # Açı değerini 0-255 aralığına ölçekleyerek gönderin
        #             scaled_value = int((angle_value / 180) * 255)
        #             print(f"Sending: {scaled_value}")
        #             data = write_read(scaled_value)
        #             if data:
        #                 print(f"Received: {data}")
        #         else:
        #             print("Açı 0 ile 180 arasında olmalıdır.")
        #     else:
        #         print("Lütfen geçerli bir sayı girin.")
    
    except serial.SerialException as e:
        print(f"SerialException: {e}")
    
    except KeyboardInterrupt:
        print("Program sonlandırıldı.")
    
    finally:
        if 'arduino' in globals() and arduino.is_open:
            arduino.close()
            print("Port kapatıldı.")

if __name__ == "__main__":
    main()
