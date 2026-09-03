from __future__ import annotations
import socket, subprocess, sys

def free_port(start=8501,end=8599):
    for p in range(start,end+1):
        with socket.socket() as s:
            try:
                s.bind(('127.0.0.1',p))
                return p
            except OSError:
                pass
    raise RuntimeError('No free port between 8501 and 8599.')

if __name__=='__main__':
    p=free_port()
    print(f'ResilioNet Local → http://localhost:{p}')
    subprocess.run([sys.executable,'-m','streamlit','run','app.py','--server.address','127.0.0.1','--server.port',str(p)],check=False)
