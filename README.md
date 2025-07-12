### backend para un taller mecánico.

Uso:
* tener un archivo .env con la url de la base de datos configurada (DATABASE_URL="mssql+pyodbc://USUARIO:CONTRASEÑA@nodossolutions.com:PUERTO/NOMBRE_BASE_DE_DADOS?driver=ODBC+Driver+17+for+SQL+Server").
* se recomienda crear un entorno virtual para no tener las dependencias instaladas en el sistema.
* para instalar las rependencias: `pip install -r requirements.txt`.
* para ejecutar: `uvicorn main:app --reload`.
* En linux puede que se deba instalar algún paquete para poder conectarse a SQLServer (unixodbc).
