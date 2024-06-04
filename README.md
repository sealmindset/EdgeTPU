# Pineberry Pi Dual Edge TPU

## Preq:
Raspberry Pi 5

Pineboard Coral Edge TPU HAT (Dual TPU Compatible)

Lastest Raspberry Pi Bookworm - 64 bit (e.g., 6.6.31+rpt-rpi-2712 aarch64)

#### Pineboards Ref:

https://pineboards.io/pages/documentation-hat-ai-dual

https://coral.ai/docs/notes/build-coral/

#### Docker Ref:

https://www.diyengineers.com/2024/05/18/setup-coral-tpu-usb-accelerator-on-raspberry-pi-5/

## Image the lastest RPI distro
Write the RPI image to a SD Card. 

## Initial Boot
### Run setup_hat.sh
```
sudo bash setup_hat.sh
```

### Run chk_coral.sh
```
sudo bash chk_coral.sh
```

### Run setup_docker.sh
```
sudo bash setup_docker.sh
```

## Docker
### Build
```
sudo docker build -t "coral" .
```

### Run
```
sudo docker run -it --device /dev/apex_0:/dev/apex_0 --device /dev/apex_1:/dev/apex_1 coral
```

### Test TPU
```
python3 test_tpu.py
```





