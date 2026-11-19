"""Fresh session provisioning and receiver, with no source edits required."""
import argparse,json,os,socket,time
from pathlib import Path
import main

def provision(port,key,sid,ssid,password,host,udp_port,mode):
    import serial
    for v in (ssid,password,host):
        if any(c.isspace() for c in v): raise ValueError('This compact firmware config requires SSID/password without whitespace')
    with serial.Serial(port,921600,timeout=.1) as ser:
        time.sleep(2); ser.reset_input_buffer()
        ser.write(f'CFG {key.hex()} {sid.hex()} {ssid or "-"} {password or "-"} {host} {udp_port} {mode}\n'.encode()); ser.flush()
        start=time.monotonic()
        while time.monotonic()-start<25:
            line=ser.readline().decode(errors='replace').strip()
            if line: print(line)
            if line=='READY': return
            if line.startswith('ERR'): raise RuntimeError(line)
        raise TimeoutError('Board did not acknowledge provisioning; check COM port, baud and board firmware')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--serial',required=True);p.add_argument('--mode',choices=['USB','MIC'],default='USB');p.add_argument('--wav');p.add_argument('--seconds',type=int,default=10);p.add_argument('--out',default='results/hardware.wav');p.add_argument('--ssid',default='');p.add_argument('--host',default='');p.add_argument('--port',type=int,default=5005);p.add_argument('--play',action='store_true');p.add_argument('--key',help='Optional ML-KEM-generated session.key, use only for a fresh session')
    a=p.parse_args(); import getpass
    key=main.key_read(a.key) if a.key else os.urandom(16); sid=os.urandom(8)
    dest=Path(a.out); dest.parent.mkdir(parents=True,exist_ok=True)
    config=dest.with_suffix('.config.json'); cfg={'ssid':a.ssid or '-','password':'-','host':a.host or '127.0.0.1','mode':a.mode}
    # USB keeps the port open, avoiding a second reset and lost provisioning.
    if a.mode=='USB':
        if not a.wav: p.error('--wav is required for USB input')
        main.write_json(config,cfg)
        print(main.receive(key,sid,a.out,a.seconds,a.port,a.serial,a.play,session_config=config,serial_audio=a.wav))
    else:
        if not a.host or not a.ssid: p.error('MIC requires --host laptopIPv4 and --ssid')
        password=getpass.getpass('Wi-Fi password (blank for open network): ')
        # Receiver runs before provisioning so initial sequence frames are not missed.
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            result=pool.submit(main.receive,key,sid,a.out,a.seconds+25,a.port,None,a.play)
            time.sleep(.1); provision(a.serial,key,sid,a.ssid,password,a.host,a.port,'MIC'); print(result.result())
    # Key intentionally not printed or saved. Optional ML-KEM input stays in its user-created file.
