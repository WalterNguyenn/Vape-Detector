
import csv
import datetime
import serial
import time
import os

# Define your thresholds
pm25_threshold = 30  # Adjust based on your requirements
pm10_threshold = 50  # Adjust based on your requirements
location = "Bathroom #1"  # Replace with your actual location

# Initialize serial connection (Adjust 'COM3' to your actual port)
ser = serial.Serial('COM3', baudrate=9600, timeout=1)

def log_data_to_csv(current_time, location, status):
    directory_path = r'C:\Users\Laolu James\Desktop\Csv'
    
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    
    file_path = os.path.join(directory_path, 'vape_detection_log.csv')
    headers = ["Time", "Location", "Status"]

    file_exists = os.path.isfile(file_path)
    
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(headers)
        writer.writerow([current_time, location, status])

def read_from_sensor():
    ser.flushInput()
    data = ser.read(10)
    if len(data) == 10 and data[0] == 0xAA and data[1] == 0xC0:
        pm25 = int.from_bytes(data[2:4], byteorder='little') / 10
        pm10 = int.from_bytes(data[4:6], byteorder='little') / 10
        
        # Display the current readings
        print(f"PM2.5: {pm25} μg/m³, PM10: {pm10} μg/m³")
        
        # Check if readings exceed thresholds
        if pm25 > pm25_threshold or pm10 > pm10_threshold:
            return True, pm25, pm10
    return False, pm25, pm10

def main():
    last_logged_time = datetime.datetime.now()
    
    try:
        while True:
            threshold_exceeded, pm25, pm10 = read_from_sensor()
            if threshold_exceeded:
                print("Threshold Exceeded")
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if (datetime.datetime.now() - last_logged_time) >= datetime.timedelta(minutes=1):
                    log_data_to_csv(current_time, location, "Exceeded")
                    last_logged_time = datetime.datetime.now()
            else:
                # You can uncomment the next line if you want to log 'Not Exceeded' statuses too
                # log_data_to_csv(current_time, location, "Not Exceeded")
                pass
            time.sleep(1)  # Check sensor every second
    except KeyboardInterrupt:
        print("Program terminated")
        ser.close()

if __name__ == "__main__":
    main()