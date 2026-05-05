from psycopg2.extras import execute_values
import logging

def create_temp_tables(db_connection, proveedor_datos, pdv_datos, productos_datos):
    
    try:
        with db_connection.cursor() as cur:
            cur.execute("""
            CREATE TEMP TABLE IF NOT EXISTS proveedores (
                glnproveedor TEXT PRIMARY KEY,
                proveedor TEXT
            );
            CREATE TEMP TABLE IF NOT EXISTS puntosdeventa (
                glnretailerlocation TEXT PRIMARY KEY,
                punto_de_venta TEXT
            );
            CREATE TEMP TABLE IF NOT EXISTS productos(
                gtin TEXT PRIMARY KEY,
                descripcion_logyca TEXT,
                categoria TEXT
            );
            CREATE TEMP TABLE IF NOT EXISTS sales_daily_report (
                day DATE,
                glnprovider TEXT,
                proveedor TEXT,
                glnretailerlocation TEXT,
                punto_de_venta TEXT,
                gtin TEXT,
                descripcion_logyca TEXT,
                categoria TEXT,
                und_vendidas FLOAT8,
                ventas FLOAT8,
                PRIMARY KEY (day, glnprovider, glnretailerlocation, gtin)
            );
            CREATE TEMP TABLE IF NOT EXISTS inventory_daily_report (
                day DATE,
                glnprovider TEXT,
                glnretailerlocation TEXT,
                gtin TEXT,
                und_inventario FLOAT8,
                inventarios FLOAT8,
                PRIMARY KEY (day, glnprovider, glnretailerlocation, gtin)
            );
            """)

            execute_values(cur, "INSERT INTO proveedores (glnproveedor, proveedor) VALUES %s ON CONFLICT DO NOTHING", proveedor_datos)
            execute_values(cur, "INSERT INTO puntosdeventa (glnretailerlocation, punto_de_venta) VALUES %s ON CONFLICT DO NOTHING", pdv_datos)
            execute_values(cur, "INSERT INTO productos (gtin, descripcion_logyca, categoria) VALUES %s ON CONFLICT DO NOTHING", productos_datos)
        
        db_connection.commit()

    except Exception as e:
        logging.error("Error creating or populating temp tables", exc_info=True)
        db_connection.rollback()
        raise