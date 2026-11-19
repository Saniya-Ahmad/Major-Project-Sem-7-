from pathlib import Path
import shutil
root=Path(__file__).resolve().parent; out=root/'build/esp32_benchmark'; out.mkdir(parents=True,exist_ok=True)
for name in ('esp32_benchmark.ino','caalc_core.h','round_constants.h'): shutil.copy2(root/name,out/name)
shutil.copytree(root/'vendor/ascon',out/'src/ascon',dirs_exist_ok=True)
print('Open',out/'esp32_benchmark.ino','in Arduino IDE; same ESP32 core and board as sender.')
