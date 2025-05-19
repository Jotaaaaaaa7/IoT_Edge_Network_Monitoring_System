import subprocess

def ping_host(host):
    try:
        result = subprocess.run(["ping", "-c", "1", host], capture_output=True, text=True)
        return result.returncode == 0, result.stdout
    except Exception as e:
        return False, str(e)

def resolve_hostname(hostname):
    try:
        result = subprocess.run(["getent", "hosts", hostname], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip().split()[0]  # Devuelve la IP
        else:
            return None
    except Exception:
        return None
