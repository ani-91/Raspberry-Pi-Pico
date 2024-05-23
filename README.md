# Project - Neonatal suction device
## Overview
A microcontroller based automated suction device that can expel viral secretion from a baby's (1-30 days) chest/wind pipe to avoid choking.\
Interface and controller logic to read pressure(back pressure) & vacuum(suction manifold) sensors and control suction pump and valves.
An android app for filling the patient details and operational parameters such as frequency, duration of suction etc.
### Blockdiagram
![Screenshot 2023-07-14 080537](https://github.com/ani-91/Raspberry-Pi-Pico/assets/141425684/3d26436f-0803-4ccf-9de3-a8849c8ceba9)
### Main components
- RP2040 Microcontroller
- 20 X 4 LCD
- DS3231 Timer
- AT24C64 EEPROM
- ADS1115 ADC
- XGZP6847D Pressure/Vacuum Sensor
- Vacuum pump
- Couple of 3-D printed couplers, T-joints, enclosure
### Flowchart
![Screenshot 2023-07-14 111839](https://github.com/ani-91/Raspberry-Pi-Pico/assets/141425684/3019bb58-33f0-4e2f-bcb5-3ddd91e7c573)
![Screenshot 2023-07-14 113317](https://github.com/ani-91/Raspberry-Pi-Pico/assets/141425684/41d13e94-25c6-494b-9b68-0e3f7c4f3a1f)
![Screenshot 2023-07-14 113344](https://github.com/ani-91/Raspberry-Pi-Pico/assets/141425684/86e46e92-6010-47bd-aa7d-5ba319386ba8)


