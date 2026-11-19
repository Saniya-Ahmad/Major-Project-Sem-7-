"""Make Arduino's required folder/file naming layout without duplicating maintained code."""
from pathlib import Path
import shutil
root=Path(__file__).resolve().parent
out=root/'build/esp32_caalc'; out.mkdir(parents=True,exist_ok=True)
for name in ('esp32_caalc.ino','caalc_core.h','round_constants.h'): shutil.copy2(root/name,out/name)
print('Open',out/'esp32_caalc.ino','in Arduino IDE. Board core: esp32 2.0.17; ESP32 Dev Module.')
