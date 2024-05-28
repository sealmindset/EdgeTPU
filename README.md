# Setup Coral AI PCIe Accelerator on a Raspberry Pi 5

## Install Coral AI PCIe Edge TPU on Raspberry Pi 5
Execute the scripts below to install the drivers and tweak the OS. After each install, it will reboot.

NOTE: TODO - combine all 3 into one

### coralInstall1

```
curl https://raw.githubusercontent.com/sealmindset/EdgeTPU/main/coralInstall1.sh?token=GHSAT0AAAAAACSETBXD7HJN6OEZMKUBWTMAZSVG76A | sh
```

### coralInstall2

```
curl https://raw.githubusercontent.com/sealmindset/EdgeTPU/main/coralInstall3.sh?token=GHSAT0AAAAAACSETBXC3UKAL6AQV74CWGKSZSVHC7Q | sh
```

### coralInstall3

```
curl https://raw.githubusercontent.com/sealmindset/EdgeTPU/main/coralInstall1.sh?token=GHSAT0AAAAAACSETBXD7HJN6OEZMKUBWTMAZSVG76A | sh
```

## Verify the TPU is accessible

```
python verifyTPU.py
```

## Test Coral to see it works

```
python testCoral.py
```


