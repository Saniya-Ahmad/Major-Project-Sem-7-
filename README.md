# CAALC-128: authenticated IoT audio research prototype

**Design and Implementation of a Lightweight Cellular Automata-Based Authenticated Cipher for Post-Quantum-Oriented Secure IoT Audio Communication**

Python 3.11+ • Windows/Linux/macOS laptop • optional one ESP32-WROOM-32 • audio only.

This project contains an experimental custom Feistel/duplex cipher, an independently tested portable C++ implementation, lossless authenticated WAV containers, a Streamlit demonstration, ML-KEM-512/HKDF key establishment, the Ascon authors' final-standard reference implementation, and an ESP32 sender/receiver workflow. **CAALC has no proven 128-bit or post-quantum security.** Use the separate Ascon option when established AEAD is required, together with an authenticated key-management protocol.

Read `results/VERIFICATION.md` for the actual executed/unexecuted checks. Host timings and synthetic test audio are supplied; no physical device measurements are claimed.

## Quick start (no hardware)

Extract the ZIP and open a terminal in `CAALC128_Project`.

Windows PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If PowerShell prevents activation, use `.\.venv\Scripts\python.exe` instead of `python`; activation is optional. A newer installed Python can be used in place of `py -3.11`.

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

For the Ascon comparison and C++ cross-checks install GCC/G++ (Linux), Xcode command-line tools (macOS, providing gcc/g++ aliases), or MSYS2 UCRT64 GCC (Windows). Put the compiler's bin directory on PATH. The Python-only CAALC cipher/audio modes do not need a compiler. Prebuilt libraries from the test machine are not distributed; build locally:

```bash
python build_native.py
python main.py test
python main.py demo
python main.py mlkem
python main.py dashboard
```

Open the local URL shown by Streamlit, usually `http://localhost:8501`. The default dashboard is now one page: upload audio, Encrypt, listen to a quiet ciphertext preview, Decrypt, and listen to authenticated recovered audio. Keys are generated automatically. Save the key from the optional session details if you need to decrypt later. See `DASHBOARD_UPDATE.md` for updating an existing installation.

The previous seven-screen research dashboard remains available with `python -m streamlit run main.py -- --advanced-dashboard`. Its ML-KEM button creates a new key file; it does not silently replace the dashboard key. The simple dashboard uses locally generated random keys, not an ML-KEM exchange.

`demo` generates a two-second **synthetic chirp**, encrypts it to `results/encrypted.caf`, reconstructs `results/recovered.wav`, and writes waveform/spectrogram and loss-simulation results. `results/demo.key` is a disposable demonstration key, not a secret suitable for deployment. Do not share recordings and their real key together.

## Nine requested execution modes

| Mode | Command |
|---|---|
| 1. Correctness, KATs, cross-language checks | `python main.py test` |
| 2. Encrypt WAV | `python main.py encrypt input.wav audio.caf --key results/session.key` |
| 3. Decrypt and verify | `python main.py decrypt audio.caf recovered.wav --key results/session.key` |
| 4. Audio quality | `python main.py analyze input.wav recovered.wav` |
| 5. Security screening | `python main.py experiments` |
| 6. Native Ascon comparison | `python main.py benchmark input.wav --trials 200` |
| 7. ML-KEM-512 + HKDF | `python main.py mlkem` |
| 8. Dashboard | `python main.py dashboard` |
| 9. Receiver | `python main.py receiver --key session.key --sid YOUR_16_HEX_SESSION_ID --seconds 15 --play` |

Additional commands:

```bash
python main.py keygen
python main.py encrypt input.wav audio.caf --key results/session.key --frame-ms 40
python main.py encrypt input.wav standard.caf --key results/session.key --algorithm ascon
python main.py simulate input.wav --key results/session.key --loss 0.1 --jitter-ms 15
python main.py play recovered.wav
```

Use separate traffic keys for real Ascon and CAALC sessions. The decryption container selects its authenticated algorithm ID automatically. Acceptable WAV: uncompressed signed PCM16, mono, 8 or 16 kHz. Optional external conversion:

```bash
ffmpeg -i recording.mp3 -ac 1 -ar 8000 -c:a pcm_s16le input.wav
```

Empty audio encrypts correctly, but MSE/PSNR/SNR require at least one sample. Mismatched lengths/rates are rejected rather than silently aligned or resampled. For exact recovery, MSE=0 and PSNR/SNR=∞; JSON represents non-finite values as strings. Silent originals with nonzero reconstruction error have SNR=−∞. Encrypted bytes are not playable WAV audio.

## Optional ESP32: no source-code editing required

See [hardware instructions](docs/HARDWARE.md) for wiring, budget ceilings, installation, exact flash commands, receiver setup, and verification. Firmware credentials/key/session are supplied over local USB at runtime.

Microphone-free USB loopback (after flashing):

```bash
python hardware_session.py --serial COM5 --mode USB --wav results/original.wav --seconds 4 --out results/usb_received.wav
```

Replace `COM5` with the actual port (Linux commonly `/dev/ttyUSB0`). Use a fresh ML-KEM key instead of a random key by appending `--key results/session.key` after running `main.py mlkem`. This is controlled USB provisioning, **not** authenticated network PQ key exchange.

Microphone to Wi-Fi receiver:

```bash
python hardware_session.py --serial COM5 --mode MIC --ssid YourWiFi --host 192.168.1.25 --seconds 10 --out results/mic_received.wav --play
```

The script prompts privately for the Wi-Fi password and starts the UDP receiver before provisioning the board. The capture window includes a 25-second connection allowance, so it runs longer than `--seconds`. Only same-LAN UDP is demonstrated. No cloud, second board, speaker module, SD card or Arduino Uno is required.

## Source map

- `main.py`: Python reference, audio/file/wire format, metrics, statistical experiments, native wrappers, receiver, dashboard, CLI.
- `caalc_core.h`, `round_constants.h`, `native.cpp`: shared exact portable C++ cipher for host and ESP32.
- `esp32_caalc.ino`: microphone/USB input, crypto, UDP/USB output, timings.
- `hardware_session.py`: fresh key/session provisioning and capture without code edits.
- `esp32_benchmark.ino`: optional same-device native CAALC/Ascon benchmark.
- `build_native.py`, `prepare_arduino.py`, `prepare_hardware_benchmark.py`: reproducible build preparation.
- `tests/`, `test_vectors/`: functional/transport/UI tests and public known-answer values.
- `vendor/ascon/`: upstream final-standard reference source, with licensing and provenance in `vendor/PROVENANCE.md`.
- `docs/SPECIFICATION.md`: exact mathematical, AEAD, nonce and protocol specification.
- `docs/ACADEMIC_REPORT.md`: abstract, methodology, discussion, presentation outline and viva.
- `results/`: measured host results, plots, logs and verification status.

## Operational limits and limitations

Fresh key per hardware boot is mandatory; do not manually reuse key+session after reset. Receiver replay state is session-local and does not survive restart; start a new session after receiver restart. Start reception before sending. Firmware capture is fixed at 8 kHz, 20 ms; Python file modes support 8/16 kHz and 10/20/40 ms. Real-time playback requires a working host audio device/PortAudio; recording works without a speaker. Linux may need the system `libportaudio2` package.

This is a research demonstration, not a hardened network service. CAALC security, authenticated endpoint identity, physical real-time performance, energy, side-channel leakage, hardware audio quality and ₹500 local procurement remain to be validated. Memory/code figures are compiler/implementation-specific. The supplied Ascon source is portable reference code, not necessarily the fastest available ESP32 implementation.

## Sources

- NIST SP 800-232 (final): https://csrc.nist.gov/pubs/sp/800/232/final
- NIST FIPS 203: https://csrc.nist.gov/pubs/fips/203/final
- Ascon authors' source and KATs: https://github.com/ascon/ascon-c
- pqcrypto Python bindings: https://github.com/backbone-hq/pqcrypto
- Espressif I2S legacy API: https://docs.espressif.com/projects/esp-idf/en/v4.4.5/esp32/api-reference/peripherals/i2s.html

The attached presentation and handwritten note informed scope. Changes from the slides are explicitly listed in the academic report. Bibliographic claims in the earlier slides have not been treated as independently verified evidence of a research gap.

## Reproduce the supplied evaluation

```bash
python reproduce.py
python reproduce.py --summary-only --large
```

The first command rebuilds the two native libraries and reruns offline demonstrations, ML-KEM, screening, benchmarks and pytest. The second reruns the slower 1 MiB CAALC audio check and refreshes the summary. Keep the dated original verification log when comparing a later environment. To reproduce native object/stack measurements on GCC:

```bash
g++ -O2 -std=c++11 -fstack-usage -c native.cpp -o build/caalc.o
gcc -O2 -fstack-usage -Ivendor/ascon -c vendor/ascon/aead.c -o build/ascon.o
size build/caalc.o build/ascon.o
```

The release archive excludes temporary build products and the transient ML-KEM session key. Run the build and ML-KEM commands locally. `results/demo.key` accompanies only the public synthetic example so its encrypted CAF file can be inspected immediately.
