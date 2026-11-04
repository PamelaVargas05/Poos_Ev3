from persistencia.conexion import abrir_conexion


def crear_tablas():
    conexion = None
    try:
        conexion = abrir_conexion()
        cursor = conexion.cursor()

        sentencias = [
            """
            CREATE TABLE IF NOT EXISTS departamento (
                id INT PRIMARY KEY AUTO_INCREMENT,
                nombre VARCHAR(100) NOT NULL UNIQUE
            ) ENGINE=InnoDB
            """,
            """
            CREATE TABLE IF NOT EXISTS empleado (
                id INT PRIMARY KEY AUTO_INCREMENT,
                nombre VARCHAR(120) NOT NULL,
                correo VARCHAR(150) NOT NULL UNIQUE,
                telefono VARCHAR(30),
                fecha_inicio DATE NOT NULL,
                salario_base DECIMAL(12,2) NOT NULL DEFAULT 0,
                tipo VARCHAR(20) NOT NULL DEFAULT 'BASE',
                bono_anual DECIMAL(12,2) NOT NULL DEFAULT 0,
                tarifa_hora DECIMAL(12,2) NOT NULL DEFAULT 0,
                departamento_id INT NULL,
                CONSTRAINT fk_empleado_departamento FOREIGN KEY (departamento_id)
                    REFERENCES departamento(id) ON UPDATE CASCADE ON DELETE SET NULL
            ) ENGINE=InnoDB
            """,
            """
            CREATE TABLE IF NOT EXISTS proyecto (
                id INT PRIMARY KEY AUTO_INCREMENT,
                nombre VARCHAR(120) NOT NULL UNIQUE,
                descripcion VARCHAR(500),
                fecha_inicio DATE NOT NULL,
                activo BOOLEAN NOT NULL DEFAULT TRUE
            ) ENGINE=InnoDB
            """,
            """
            CREATE TABLE IF NOT EXISTS indicador_api (
                id INT PRIMARY KEY AUTO_INCREMENT,
                fuente VARCHAR(150) NOT NULL,
                codigo VARCHAR(50) NOT NULL,
                fecha DATE NOT NULL,
                valor DECIMAL(18,6) NOT NULL,
                unidad VARCHAR(50) NOT NULL,
                verificado_en DATETIME NOT NULL,
                CONSTRAINT uq_indicador_fuente_codigo_fecha
                    UNIQUE (fuente, codigo, fecha)
            ) ENGINE=InnoDB
            """,
        ]
        for sql in sentencias:
            cursor.execute(sql)

        cursor.execute(
            """
            SELECT 1
            FROM information_schema.STATISTICS
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = 'indicador_api'
              AND INDEX_NAME = 'uq_indicador_fuente_codigo_fecha'
            LIMIT 1
            """
        )
        if cursor.fetchone() is None:
            cursor.execute(
                """
                ALTER TABLE indicador_api
                ADD CONSTRAINT uq_indicador_fuente_codigo_fecha
                UNIQUE (fuente, codigo, fecha)
                """
            )

        # Tabla para el acceso seguro de la Unidad 3.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuario (
                id INT PRIMARY KEY AUTO_INCREMENT,
                nombre_usuario VARCHAR(30) NOT NULL UNIQUE,
                sal CHAR(32) NOT NULL,
                clave_hash CHAR(64) NOT NULL,
                empleado_id INT NULL,
                rol VARCHAR(10) NOT NULL DEFAULT 'empleado',
                CONSTRAINT ck_usuario_rol CHECK (rol IN ('admin', 'empleado')),
                CONSTRAINT fk_usuario_empleado FOREIGN KEY (empleado_id)
                    REFERENCES empleado(id) ON UPDATE CASCADE ON DELETE SET NULL
            ) ENGINE=InnoDB
        """)

        cursor.execute(
            """
            SELECT COLUMN_NAME
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'usuario'
            """
        )
        columnas_usuario = {fila[0] for fila in cursor.fetchall()}
        if "empleado_id" not in columnas_usuario:
            cursor.execute("ALTER TABLE usuario ADD COLUMN empleado_id INT NULL")
        if "rol" not in columnas_usuario:
            cursor.execute(
                "ALTER TABLE usuario ADD COLUMN rol VARCHAR(10) "
                "NOT NULL DEFAULT 'empleado'"
            )
        cursor.execute(
            "UPDATE usuario SET rol = 'empleado' "
            "WHERE rol IS NULL OR rol NOT IN ('admin', 'empleado')"
        )
        cursor.execute(
            """
            SELECT CONSTRAINT_NAME
            FROM information_schema.TABLE_CONSTRAINTS
            WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'usuario'
              AND CONSTRAINT_NAME = 'fk_usuario_empleado'
            """
        )
        if cursor.fetchone() is None:
            cursor.execute(
                """
                ALTER TABLE usuario ADD CONSTRAINT fk_usuario_empleado
                FOREIGN KEY (empleado_id) REFERENCES empleado(id)
                ON UPDATE CASCADE ON DELETE SET NULL
                """
            )
        cursor.execute(
            """
            SELECT CONSTRAINT_NAME
            FROM information_schema.TABLE_CONSTRAINTS
            WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'usuario'
              AND CONSTRAINT_NAME = 'ck_usuario_rol'
            """
        )
        if cursor.fetchone() is None:
            cursor.execute(
                "ALTER TABLE usuario ADD CONSTRAINT ck_usuario_rol "
                "CHECK (rol IN ('admin', 'empleado'))"
            )


        # Normaliza instalaciones anteriores que tenían tablas MyISAM o columnas antiguas.
        cursor.execute("ALTER TABLE departamento ENGINE=InnoDB")
        cursor.execute("ALTER TABLE empleado ENGINE=InnoDB")
        cursor.execute(
            """
            ALTER TABLE empleado
                ADD COLUMN IF NOT EXISTS telefono VARCHAR(30),
                ADD COLUMN IF NOT EXISTS fecha_inicio DATE NOT NULL DEFAULT '2000-01-01',
                ADD COLUMN IF NOT EXISTS salario_base DECIMAL(12,2) NOT NULL DEFAULT 0,
                ADD COLUMN IF NOT EXISTS tipo VARCHAR(20) NOT NULL DEFAULT 'BASE',
                ADD COLUMN IF NOT EXISTS bono_anual DECIMAL(12,2) NOT NULL DEFAULT 0,
                ADD COLUMN IF NOT EXISTS tarifa_hora DECIMAL(12,2) NOT NULL DEFAULT 0,
                ADD COLUMN IF NOT EXISTS departamento_id INT NULL
            """
        )
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM information_schema.REFERENTIAL_CONSTRAINTS
            WHERE CONSTRAINT_SCHEMA = DATABASE()
            AND CONSTRAINT_NAME = 'fk_empleado_departamento'
            """
        )
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                """
                ALTER TABLE empleado
                ADD CONSTRAINT fk_empleado_departamento
                FOREIGN KEY (departamento_id) REFERENCES departamento(id)
                ON UPDATE CASCADE ON DELETE SET NULL
                """
            )
        cursor.execute("ALTER TABLE proyecto ENGINE=InnoDB")

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS proyecto_empleado (
                proyecto_id INT NOT NULL,
                empleado_id INT NOT NULL,
                PRIMARY KEY (proyecto_id, empleado_id),
                CONSTRAINT fk_pe_proyecto
                    FOREIGN KEY (proyecto_id) REFERENCES proyecto(id) ON DELETE CASCADE,
                CONSTRAINT fk_pe_empleado
                    FOREIGN KEY (empleado_id) REFERENCES empleado(id) ON DELETE CASCADE
            ) ENGINE=InnoDB
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS registro_tiempo (
                id INT PRIMARY KEY AUTO_INCREMENT,
                fecha DATE NOT NULL,
                horas DECIMAL(5,2) NOT NULL CHECK (horas > 0 AND horas <= 24),
                descripcion VARCHAR(500) NOT NULL,
                empleado_id INT NOT NULL,
                proyecto_id INT NOT NULL,
                CONSTRAINT fk_rt_empleado
                    FOREIGN KEY (empleado_id) REFERENCES empleado(id) ON DELETE CASCADE,
                CONSTRAINT fk_rt_proyecto
                    FOREIGN KEY (proyecto_id) REFERENCES proyecto(id) ON DELETE CASCADE
            ) ENGINE=InnoDB
            """
        )
        conexion.commit()
    except Exception:
        if conexion:
            conexion.rollback()
        raise
    finally:
        if conexion:
            conexion.close()


if __name__ == "__main__":
    crear_tablas()
    print("Base de datos preparada correctamente.")
