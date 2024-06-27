import time
import board
import neopixel
import digitalio
import pwmio

MAX_FAN_DUTY_CYCLE = 0xAAAA
FAN_PWM_FREQUENCY = 22_000

COLOR_RED = (255, 0, 0)
COLOR_YELLOW = (255, 255, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)

FAN_SPEEDS = [
    {"pixel": COLOR_RED, "duty_cycle_pct": 0.00},
    {"pixel": COLOR_YELLOW, "duty_cycle_pct": 0.33},
    {"pixel": COLOR_GREEN, "duty_cycle_pct": 0.66},
    {"pixel": COLOR_BLUE, "duty_cycle_pct": 1.00},
]

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
fan = pwmio.PWMOut(board.A2, frequency=FAN_PWM_FREQUENCY)
button = digitalio.DigitalInOut(board.A0)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP


def set_state(selected_fan_speed):
    pixel_fill = FAN_SPEEDS[selected_fan_speed]["pixel"]
    duty_cycle_pct = FAN_SPEEDS[selected_fan_speed]["duty_cycle_pct"]
    fan_duty_cycle = int(MAX_FAN_DUTY_CYCLE * duty_cycle_pct)

    print(f"Setting pixel to {pixel_fill}")
    pixel.fill(pixel_fill)

    fan.duty_cycle = fan_duty_cycle
    print(f"Set fan duty cycle to {fan.duty_cycle}")


button_up = True
fan_speed = 0
set_state(fan_speed)


while True:
    button_value = button.value
    if button_value != button_up:
        button_up = button_value

        if button_up:
            print("button is released")

        else:
            print("button is pressed")
            fan_speed = (fan_speed + 1) % len(FAN_SPEEDS)
            set_state(fan_speed)
            time.sleep(0.250)
