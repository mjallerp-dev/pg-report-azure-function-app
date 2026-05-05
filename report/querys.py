from datetime import datetime, timedelta
import logging

def generate_report(db_connection, glns_proveedores, glns_pdv, glns_productos):

    try:
        with db_connection.cursor() as cur:

            start_date = datetime.today() - timedelta(days=7)

            for i in range(7):

                date_now = start_date + timedelta(days=i)

                cur.execute("""
                    INSERT INTO sales_daily_report (day, glnprovider, proveedor, glnretailerlocation, punto_de_venta, gtin, descripcion_logyca, categoria, und_vendidas, ventas)
                SELECT
                    d.day,
                    d.glnprovider::TEXT,
                    p.proveedor,
                    d.glnretailerlocation::TEXT,
                    pdv.punto_de_venta,
                    d.gtin::TEXT,
                    prod.descripcion_logyca,
                    prod.categoria,
                    SUM(d.sales),
                    SUM(d.sales * d.price)
                FROM ddvi d
                    JOIN proveedores p ON d.glnprovider::TEXT = p.glnproveedor
                    JOIN puntosdeventa pdv ON d.glnretailerlocation::TEXT = pdv.glnretailerlocation
                    JOIN productos prod ON d.gtin::TEXT = prod.gtin
                WHERE d.day = %s
                    AND d.glnprovider::TEXT IN %s
                    AND d.glnretailerlocation::TEXT IN %s
                    AND d.gtin::TEXT IN %s
                    AND NOT (COALESCE(d.sales, 0) = 0 AND COALESCE(d.inventory, 0) = 0)
                GROUP BY d.day, d.glnprovider, p.proveedor, d.glnretailerlocation, pdv.punto_de_venta, d.gtin, prod.descripcion_logyca, prod.categoria
                ON CONFLICT (day, glnprovider, glnretailerlocation, gtin) DO UPDATE
                SET und_vendidas = EXCLUDED.und_vendidas,
                    ventas = EXCLUDED.ventas;
                """, (date_now.date(), glns_proveedores, glns_pdv, glns_productos))

                logging.info("Ventas del dia %s procesado...", date_now.date())

            date_inv = datetime.today() - timedelta(days=1)

            cur.execute("""
                INSERT INTO inventory_daily_report (day, glnprovider, glnretailerlocation, gtin, und_inventario, inventarios)
            SELECT
                d.day,
                d.glnprovider::TEXT,
                d.glnretailerlocation::TEXT,
                d.gtin::TEXT,
                SUM(d.inventory),
                SUM(d.inventory * d.price)
            FROM ddvi d
            WHERE d.day = %s
                AND d.glnprovider::TEXT IN %s
                AND d.glnretailerlocation::TEXT IN %s
                AND d.gtin::TEXT IN %s
                AND NOT (COALESCE(d.sales, 0) = 0 AND COALESCE(d.inventory, 0) = 0)
            GROUP BY d.day, d.glnprovider, d.glnretailerlocation, d.gtin
            ON CONFLICT (day, glnprovider, glnretailerlocation, gtin) DO UPDATE
            SET und_inventario = EXCLUDED.und_inventario,
                inventarios = EXCLUDED.inventarios;
                        """, (date_inv.date(), glns_proveedores, glns_pdv, glns_productos))
            
            logging.info("Inventarios del dia %s procesado...", date_inv.date())

        final_query = """
            WITH CTE AS (
            SELECT
              glnprovider, proveedor, glnretailerlocation, punto_de_venta, gtin, descripcion_logyca, categoria,
              AVG(und_vendidas) AS prom_und_vendidas,
              AVG(ventas) AS prom_ventas
            FROM sales_daily_report
            GROUP BY glnprovider, proveedor, glnretailerlocation, punto_de_venta, gtin, descripcion_logyca, categoria
            )
            SELECT
                ied.glnprovider::TEXT, CTE.proveedor, ied.glnretailerlocation::TEXT, CTE.punto_de_venta, ied.gtin::TEXT,
                CTE.descripcion_logyca, CTE.categoria,
                CTE.prom_und_vendidas, CTE.prom_ventas,
                ied.und_inventario, ied.inventarios
            FROM inventory_daily_report ied
            LEFT JOIN CTE
                ON ied.glnprovider::TEXT = CTE.glnprovider
                AND ied.glnretailerlocation::TEXT = CTE.glnretailerlocation
                AND ied.gtin::TEXT = CTE.gtin
        """
        db_connection.commit()
        return final_query


    except Exception:
        db_connection.rollback()
        logging.error("Error generating report", exc_info=True)
        raise

