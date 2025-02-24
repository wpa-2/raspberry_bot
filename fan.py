from gpiozero import PWMOutputDevice
import time
import os

def get_cpu_temperature():
    """Read the CPU temperature"""
    temp = os.popen("cat /sys/class/thermal/thermal_zone0/temp").readline()
    return float(temp) / 1000  # Convert from millidegrees to degrees

# Define the GPIO pin connected to the fan (PWM)
FAN_PIN = 18  # Change this if using a different pin
fan = PWMOutputDevice(FAN_PIN)

# Adjusted temperature thresholds based on your system
TEMP_LOW = 50  # Fan starts at 10%
TEMP_HIGH = 75  # Fan reaches 100%

# Minimum fan speed when running
MIN_FAN_SPEED = 0.1  # 10%

def control_fan():
    """Adjusts the fan speed based on CPU temperature"""
    try:
        while True:
            temp = get_cpu_temperature()
            
            if temp < TEMP_LOW:
                duty_cycle = 0  # Fan off
            elif temp > TEMP_HIGH:
                duty_cycle = 1  # Full speed (100%)
            else:
                # Linear scaling between TEMP_LOW and TEMP_HIGH, with a minimum speed
                duty_cycle = (temp - TEMP_LOW) / (TEMP_HIGH - TEMP_LOW)
                duty_cycle = max(duty_cycle, MIN_FAN_SPEED)  # Ensure minimum speed
            
            fan.value = duty_cycle  # Set PWM duty cycle
            print(f"Temp: {temp:.1f}°C | Fan Speed: {duty_cycle * 100:.1f}%")
            
            time.sleep(5)  # Adjust polling interval as needed
    except KeyboardInterrupt:
        print("Fan control stopped")
    finally:
        fan.off()

if __name__ == "__main__":
    control_fan()
