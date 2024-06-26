import time
import board
import neopixel
import digitalio
import pwmio

FAN_SPEEDS = [
    {"pixel": (255, 0, 0), "duty_cycle": 0x0000},  # red, 0%
    {"pixel": (255, 255, 0), "duty_cycle": 0x5555},  # yellow, 33%
    {"pixel": (0, 255, 0), "duty_cycle": 0xAAAA},  # green, 67%
    {"pixel": (0, 0, 255), "duty_cycle": 0xFFFF},  # blue, 100%
]

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
fan = pwmio.PWMOut(board.A2, frequency=22000)
button = digitalio.DigitalInOut(board.A0)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP


def set_state(selected_fan_speed):
    pixel_fill = FAN_SPEEDS[selected_fan_speed]["pixel"]
    fan_duty_cycle = FAN_SPEEDS[selected_fan_speed]["duty_cycle"]

    print(f"Setting pixel to {pixel_fill}")
    pixel.fill(pixel_fill)

    fan.duty_cycle = fan_duty_cycle
    print(f"Set fan duty cycle to {fan.duty_cycle}")


button_up = True
fan_speed = 0
set_state(fan_speed)

while True:
    if button.value != button_up:
        button_up = button.value

        if button_up:
            print("button is released")
            fan_speed = (fan_speed + 1) % len(FAN_SPEEDS)
            set_state(fan_speed)

        else:
            print("button is pressed")
