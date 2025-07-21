## Aplicativo para gestión de vehiculos (taller mecánico).

Sistema Integrador en el Manejo y control de la informacion relevante de un taller mecanico para mejorar los procesos.

## Dependencias (pip)
- fastapi
- uvicorn
- python-jose
- sqlmodel

### Uso:
- Crea un archivo llamado ".env" que contenga lo siguiente:
    - DATABASE_URL="mssql+pyodbc://USUARIO:CONTRASEÑA@nodossolutions.com:1435/gestion_taller?driver=ODBC+Driver+17+for+SQL+Server".
- Crea un entorno virtual y activalo para no tener las dependencias instaladas en el sistema.
- Ejecutar con: `python main.py`.
- Puede que se deba instalar algún paquete/controlador para poder conectarse a SQLServer, busca unixodbc para linux o [aquí](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver17#version-17) para windows.

### En trabajo, por completar:
- [ ] Los modelos deberían estar en diferentes archivos para mejor organización.
- [ ] Hay algo de código repetido.
- [ ] Configurar los id de ciertas tablas como auntoincrementales.
