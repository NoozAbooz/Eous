This project was made based on this tutorial: https://www.lcsc.com/

This doc is a summary of its key info with my own thoughts

# Outline
- Can control servos
- IMU, altitude (barometer?), etc telemetry
- Non-volatile data storage (sd card)
- Battery-powered

# Spec requirements
- Servos run on 5-6V, drawing ~1A
- Microcontrollers and sensors run on 3.3V, so a 2-cell 7.4V LiPo can power everything once we regulate the power

# Selected parts
- STM32F722RET6 for high clock speed
- ICM-45686 for IMU
- BMP580 for barometer

# Power management
- Power input can be USB (5V) or 7-8V (2-cell LiPo)
- BQ25883 for battery management IC
## Power lines
- LMR51430 3.3V line for MCU, coming out from a buck regulator
- TPS63070 5V buck-boost for servos (need boost incase voltage drops below 5V during load)
