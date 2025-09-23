import os
import sys
# os.environ["QT_API"] = "pyqt6"
sys.argv += ['--opentsdb','127.0.0.1','--grafana=127.0.0.1','--grafana_key=glsa_seBJY5YcvEip7dVLnFwqSm4ULohZVAgQ_890892c0']
from pysca import app
from pysca.device import PYPLC
import pygui.navbar as navbar

def main():
    import argparse
    global Zone_1,Zone_2
    args = argparse.ArgumentParser(sys.argv)
    args.add_argument('--device', action='store', type=str, default='192.168.8.10', help='IP address of the device')
    args.add_argument('--simulator', action='store_true', default=False, help='Same as --device 127.0.0.1')
    ns = args.parse_known_args()[0]
    if ns.simulator:
        ns.device = '127.0.0.1'
        import subprocess
        logic = subprocess.Popen(["python3", "src/krax.py"])
    
    dev = PYPLC(ns.device)
    app.devices['PLC'] = dev
    
    Zone_1 = app.window('ui/zone_1.ui')
    Zone_2 = app.window('ui/zone_2.ui')
    Zone_3 = app.window('ui/zone_3.ui')

    # с использованием navbar
    navbar.append(Zone_1)
    navbar.append(Zone_2)
    navbar.append(Zone_3)
    navbar.instance.show( )
    navbar.instance.setWindowTitle('АСУ ПЕРЕРАБОТКИ И ФАСОВКИ ТРЕПЕЛА 250817 (c) 2025')
    # или 
    # Home.show()               
    
    dev.start(100)
    app.start( ctx = globals() )
    dev.stop( )

    if ns.simulator:
        logic.terminate( )
        pass

if __name__=='__main__':
    main( )
    