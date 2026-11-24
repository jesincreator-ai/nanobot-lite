# MicroPython SD-card mount helper for ESP32-WROOM.
# Adjust pins for your wiring. Typical SPI: SCK=18, MOSI=23, MISO=19, CS=5.
import machine, os

def mount_sd():
    try:
        spi=machine.SPI(2, baudrate=1000000, polarity=0, phase=0,
                       sck=machine.Pin(18), mosi=machine.Pin(23), miso=machine.Pin(19))
        sd=machine.SDCard(slot=2, cs=machine.Pin(5), spi=spi)
        os.mount(sd, '/sd')
        try: os.mkdir('/sd/billi')
        except OSError: pass
        print('SD mounted at /sd; BILLI folder ready')
        return True
    except Exception as e:
        print('SD mount failed; check module wiring and MicroPython build:', e)
        return False

if __name__=='__main__': mount_sd()
