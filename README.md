## Aplicativo para gestión de vehiculos (taller mecánico).

Sistema Integrador en el Manejo y control de la informacion relevante de un taller mecanico para mejorar los procesos.

### Uso:
* Configurar una variable de entorno para la base de datos (DATABASE_URL="mssql+pyodbc://USUARIO:CONTRASEÑA@nodossolutions.com:1435/gestion_taller?driver=ODBC+Driver+17+for+SQL+Server").
* Crear un entorno virtual para no tener las dependencias instaladas en el sistema.
* `pip install -r requirements.txt`.
* Ejecutar con: `uvicorn main:app --reload`.
* En linux puede que se deba instalar algún paquete para poder conectarse a SQLServer (unixodbc).

### En trabajo, por completar:
- [ ] La autenticación no está completada.
- [ ] Los modelos deberían estar en diferentes archivos para mejor organización.
- [ ] Hay algo de código repetido.
- [ ] Configurar los id de las tablas para que no sean modificables desde la API.
