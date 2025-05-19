import json
import os

CONFIG_PATH = "/shared-data/devices.json"  # Volumen compartido entre contenedores

def load_devices():
    """
    Carga la lista de dispositivos desde un archivo JSON.

    Verifica si el archivo de configuración existe. Si no existe, devuelve una lista vacía.
    Si el archivo existe, intenta cargar y deserializar su contenido en formato JSON.
    En caso de que el archivo tenga un formato inválido, también devuelve una lista vacía.

    Returns:
        list: Una lista de dispositivos cargados desde el archivo JSON, o una lista vacía si el archivo no existe
              o tiene un formato inválido.
    """
    if not os.path.exists(CONFIG_PATH):
        return []
    with open(CONFIG_PATH, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_device(device_entry):
    """
    Guarda un nuevo dispositivo en el archivo JSON.

    Crea el directorio /shared-data si no existe.
    """
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)  # 👈 crea la carpeta si no existe

    devices = load_devices()
    devices.append(device_entry)
    with open(CONFIG_PATH, "w") as f:
        json.dump(devices, f, indent=4)

def save_devices(devices):
    """
    Guarda la lista de dispositivos en el archivo JSON.

    Crea el directorio /shared-data si no existe.
    """
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)  # 👈 crea la carpeta si no existe

    with open(CONFIG_PATH, "w") as f:
        json.dump(devices, f, indent=4)


def update_device(device):
    """Actualiza un dispositivo existente en el archivo de configuración"""
    devices = load_devices()
    for i, d in enumerate(devices):
        if d['host'] == device['host']:
            devices[i] = device
            break
    save_devices(devices)
    return True

def delete_device(host):
    """Elimina un dispositivo por su dirección IP/hostname"""
    devices = load_devices()
    devices = [d for d in devices if d['host'] != host]
    save_devices(devices)
    return True
