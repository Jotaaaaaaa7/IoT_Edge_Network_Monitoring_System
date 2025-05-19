FROM almalinux:9

RUN yum install -y iputils jq cronie && yum clean all

# Copiar scripts principales
COPY monitor_worker.sh /usr/local/bin/monitor_worker.sh
COPY cron_jobs/dynamic_cron.sh /usr/local/bin/dynamic_cron.sh
COPY health_check.sh /usr/local/bin/health_check.sh

# Crear directorio utils y copiar scripts allí
RUN mkdir -p /usr/local/bin/utils
COPY utils/*.sh /usr/local/bin/utils/

# Dar permisos
RUN chmod +x /usr/local/bin/*.sh /usr/local/bin/utils/*.sh



# Para ver desde el contenedor: docker exec -it monitor_engine bash (logs, runcheck, cronlog, config)
RUN echo "alias logs='tail -f /var/log/iot_monitor.log'" >> /root/.bashrc && \
    echo "alias runcheck='monitor_worker.sh'" >> /root/.bashrc && \
    echo "alias cronlog='cat /etc/cron.d/monitor_cron'" >> /root/.bashrc && \
    echo "alias config='cat /shared-data/devices.json'" >> /root/.bashrc \
    echo "alias health='/usr/local/bin/health_check.sh'" >> /root/.bashrc


# Primero ejecuta dynamic_cron.sh, luego inicia crond
CMD ["sh", "-c", "/usr/local/bin/dynamic_cron.sh && crond && tail -f /dev/null"]



#* Después del docker compose up --> Para probar el registro de logs
# docker compose exec -it monitor_engine bash
#     monitor_worker.sh