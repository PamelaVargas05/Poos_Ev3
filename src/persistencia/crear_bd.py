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
        ]

        for sql in sentencias:
            cursor.execute(sql)

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
