import RPi.GPIO as GPIO
import time
import os

def get_cpu_temperature():
    """Read the CPU temperature"""
    temp = os.popen("vcgencmd measure_temp").readline()
    return float(temp.replace("temp=", "").replace("'C\n", ""))

# Define the GPIO pin connected to the fan
FAN_PIN = 18  # Change if using a different pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN_PIN, GPIO.OUT)

# Set up PWM on the fan pin
fan_pwm = GPIO.PWM(FAN_PIN, 100)  # 100 Hz frequency
fan_pwm.start(0)  # Start with the fan off

# Temperature thresholds (adjust as needed)
TEMP_LOW = 45  # Temperature to start reducing speed
TEMP_HIGH = 70  # Max speed threshold

def control_fan():
    """Adjusts the fan speed based on CPU temperature"""
    try:
        while True:
            temp = get_cpu_temperature()
            
            if temp < TEMP_LOW:
                duty_cycle = 0  # Fan off
            elif temp > TEMP_HIGH:
                duty_cycle = 100  # Full speed
            else:
                # Linear scaling between TEMP_LOW and TEMP_HIGH
                duty_cycle = (temp - TEMP_LOW) / (TEMP_HIGH - TEMP_LOW) * 100
            
            fan_pwm.ChangeDutyCycle(duty_cycle)
            print(f"Temp: {temp:.1f}°C | Fan Speed: {duty_cycle:.1f}%")
            
            time.sleep(5)  # Adjust polling interval as needed
    except KeyboardInterrupt:
        print("Fan control stopped")
    finally:
        fan_pwm.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    control_fan()
