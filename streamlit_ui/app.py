import streamlit as st
import re
import time
from modules import config_manager
from modules import log_viewer
from modules import network_tools

# Configuración de la página
st.set_page_config(page_title="IoT Edge Monitor", layout="wide")
st.title("📡 IoT Edge Device Monitor")
st.markdown("Sistema de monitorización de dispositivos IoT desde un Edge Gateway")

# Inicializar estados de sesión si no existen
if 'editing_device' not in st.session_state:
    st.session_state.editing_device = None

# Crear dos columnas principales
col1, col2, col3 = st.columns([9, 0.1, 9])

# ─────────────────────────────────────
# 📍 Columna izquierda: Configuración
# ─────────────────────────────────────
with col1:
    st.subheader("⚙️ Configuración")
    st.markdown("Gestiona los dispositivos IoT que deseas monitorizar.")

    # Formulario para añadir o editar dispositivos
    if st.session_state.editing_device is None:
        with st.form("add_device_form"):
            st.markdown("### Añadir nuevo dispositivo")
            ip_or_hostname = st.text_input("Dirección IP o hostname del dispositivo", "")

            # Dividir los parámetros en dos columnas dentro del formulario
            form_col1, form_col2 = st.columns(2)
            with form_col1:
                frequency = st.number_input("Frecuencia (min)", min_value=1, value=5)
            with form_col2:
                latency_threshold = st.number_input("Umbral latencia (ms)", min_value=1, value=100)

            col_ping1, col_ping2 = st.columns([1, 3])
            ping_clicked = col_ping1.form_submit_button("🔍 Probar conectividad")
            submitted = col_ping2.form_submit_button("➕ Añadir dispositivo")

            if ping_clicked:
                if ip_or_hostname:
                    success, response = network_tools.ping_host(ip_or_hostname)
                    if success:
                        st.success("✅ El host respondió correctamente al ping.")
                        st.text(response)
                    else:
                        st.error("❌ El host no respondió.")
                        st.text(response)
                else:
                    st.warning("⚠️ Introduce primero una IP o hostname.")

            if submitted:
                if not re.match(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", ip_or_hostname):
                    st.error("❌ IP o hostname no válido.")
                else:
                    octetos = ip_or_hostname.split('.')
                    is_valid_ip = all(0 <= int(octeto) <= 255 for octeto in octetos)
                    if not is_valid_ip:
                        st.error("❌ IP inválida: octetos fuera de rango.")
                    else:
                        device = {
                            "host": ip_or_hostname,
                            "frequency_min": frequency,
                            "latency_ms": latency_threshold
                        }
                        config_manager.save_device(device)
                        st.success(f"✅ Dispositivo '{ip_or_hostname}' guardado correctamente.")
                        time.sleep(1)
                        st.rerun()
    else:
        # Formulario para editar dispositivo existente
        with st.form("edit_device_form"):
            st.markdown(f"### Editar dispositivo")
            device = st.session_state.editing_device

            ip_or_hostname = st.text_input("Dirección IP o hostname", value=device['host'], disabled=True)

            form_col1, form_col2 = st.columns(2)
            with form_col1:
                frequency = st.number_input("Frecuencia (min)", min_value=1, value=device['frequency_min'])
            with form_col2:
                latency_threshold = st.number_input("Umbral latencia (ms)", min_value=1, value=device['latency_ms'])

            col_cancel, col_save = st.columns([1, 1])
            cancel_clicked = col_cancel.form_submit_button("❌ Cancelar")
            save_clicked = col_save.form_submit_button("💾 Guardar cambios")

            if cancel_clicked:
                st.session_state.editing_device = None
                st.rerun()

            if save_clicked:
                updated_device = {
                    "host": ip_or_hostname,
                    "frequency_min": frequency,
                    "latency_ms": latency_threshold
                }
                # Actualizar el dispositivo en la configuración
                config_manager.update_device(updated_device)
                st.session_state.editing_device = None
                st.success(f"✅ Dispositivo '{ip_or_hostname}' actualizado correctamente.")
                time.sleep(1)
                st.rerun()

    st.subheader("📊 Últimos eventos de monitorización")

    # Botón para refrescar manualmente
    if st.button("🔄 Refrescar datos"):
        st.rerun()

    # Contenedor para los logs
    log_container = st.empty()

    # Mostrar los logs en el contenedor
    log_data = log_viewer.parse_log()
    if log_data:
        log_container.table(log_data)
    else:
        log_container.info("No se han registrado eventos de monitorización aún.")


with col2:
    pass

# ─────────────────────────────────────
# 📍 Columna derecha: Monitorización
# ─────────────────────────────────────
with col3:
    st.subheader("📋 Dispositivos monitoreados")

    devices = config_manager.load_devices()
    if devices:
        for i, device in enumerate(devices):
            col_device, col_edit, col_delete = st.columns([3, 1, 1])

            with col_device:
                st.write(f"🔹 {device['host']} — cada {device['frequency_min']} min — umbral de latencia: {device['latency_ms']} ms")

            with col_edit:
                if st.button("✏️ Editar", key=f"edit_{device['host']}_{i}"):
                    st.session_state.editing_device = device
                    st.rerun()

            with col_delete:
                if st.button("🗑️ Eliminar", key=f"delete_{device['host']}_{i}"):
                    config_manager.delete_device(device['host'])
                    st.success(f"✅ Dispositivo '{device['host']}' eliminado correctamente.")
                    time.sleep(1)
                    st.rerun()
    else:
        st.info("Aún no hay dispositivos configurados.")
