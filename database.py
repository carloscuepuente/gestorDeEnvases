import sqlite3
from xlsxwriter.workbook import Workbook

def cliente_checker(*clientes):
    #esta aun no hace nada, de hecho creo que lanza error
    import re
    for cliente in clientes:
        try:
            cliente is tuple
        except:
            raise "ErrorCliente"
    
#hay que asegurarse de que los clientes tengan todos los campos
#hay que asegurar que los campos tengan los campos correctos

# regex para un rif ^([VEJPGvejpg]{1})-([0-9]{8})-([0-9]{1}$)

class Database():
    
    def __init__(self,nombre):
        """
        Inicializador de la base de datos, necesita un nombre ejemplo Nombre.db
        """
        import sqlite3
        self.nombre = nombre
        conexion = sqlite3.connect(self.nombre)
        conexion.close()


    @property
    def create_table_base(self):
        #crea la tabla de la base de datos
        import sqlite3
        conexion = sqlite3.connect(self.nombre)
        cursor = conexion.cursor()
        cursor.execute('''CREATE TABLE clientes (
                    Rif VARCHAR(15) PRIMARY KEY,
                    Cliente VARCHAR(100),
                    Galones INTEGER,
                    Cuñete20L INTEGER,
                    Carbolla60L INTEGER,
                    Tambor210L INTEGER,
                    UltimaFacturacion timestamp,
                    Ultimadevolucion timestamp,
                    CHECK( Galones >=0 AND 
                            Cuñete20L >= 0 AND
                            Carbolla60L >= 0 AND
                            Tambor210L >= 0 ))''')
        conexion.commit()
        conexion.close()


    def conect_to_database(self):
        #esta en realidad no esta haciendo nada por ahora
        import sqlite3
        conexion = sqlite3.connect(self.nombre)
        cursor = conexion.cursor()
        return cursor


    def crear_cliente(self,cliente):
        #crea los clientes, en teoria es capaz de crear varios clientes de golpe, hay que testear
        self.clientes = cliente
        import sqlite3
        conexion = sqlite3.connect(self.nombre)
        cursor = conexion.cursor()
        try:
            cursor.executemany("INSERT INTO clientes VALUES (?,?,?,?,?,?,DateTime('now'),DateTime('now'))", self.clientes)

        except sqlite3.IntegrityError:
            conexion.close()
            return "ErrorOperacional"
        
        conexion.commit()
        conexion.close()



    def remove_cliente(self,rif):
        #borra un registro de la base de datos, solo borra uno a uno
        import sqlite3
        self.rif = rif
        conexion = sqlite3.connect(self.nombre)
        cursor = conexion.cursor()
        cursor.execute("""
        DELETE FROM clientes WHERE Rif='{}'
        """.format(self.rif))
        conexion.commit()

        conexion.close()

    
    def update_cliente(self, clientes):
        """
        Actulizar campos especificos de un cliente o grupo de clientes, por 
        default sera actualizar todos los campos menos el rif.
        """
        import sqlite3
        self.clientes = clientes
        conexion = sqlite3.connect(self.nombre)
        cursor = conexion.cursor()

        for i in self.clientes:
            cursor.execute("""
            UPDATE clientes SET Cliente = '{}',
            Galones ='{}', 
            Cuñete20L = '{}',
            Carbolla60L = '{}',
            Tambor210L = '{}'
            WHERE Rif = '{}'
            """.format(i[1],i[2],i[3],i[4],i[5],i[0]))
        
        conexion.commit()
        conexion.close()


    def sum_envases(self,clientes):
        #si le paso un cliente que no existe, no hace nada, habria que ver si existen y los que no existen anunciarlo
        #de alguna manera
        import sqlite3
        self.clientes = clientes
        conexion = sqlite3.connect(self.nombre)
        cursor = conexion.cursor()
        for i in self.clientes:
            cursor.execute("""
            UPDATE clientes SET Galones = Galones + '{}', 
            Cuñete20L = Cuñete20L + '{}',
            Carbolla60L = Carbolla60L + '{}',
            Tambor210L = Tambor210L + '{}',
            UltimaFacturacion = DateTime('now')
            WHERE Rif = '{}'
            """.format(i[2],i[3],i[4],i[5],i[0]))
        
        conexion.commit()
        conexion.close()

    def substract_envases(self,clientes):
        #si le paso un cliente que no existe, no hace nada, iagual de la de sumar
        import sqlite3
        self.clientes = clientes
        conexion = sqlite3.connect(self.nombre)
        cursor = conexion.cursor()
        try:    
            for i in self.clientes:
                cursor.execute("""
                UPDATE clientes SET Galones = Galones - '{}', 
                Cuñete20L = Cuñete20L - '{}',
                Carbolla60L = Carbolla60L - '{}',
                Tambor210L = Tambor210L - '{}',
                UltimaDevolucion = Datetime('now')
                WHERE Rif = '{}'
                """.format(i[2],i[3],i[4],i[5],i[0]))
        except sqlite3.IntegrityError:
            conexion.close()
            return "ErrorOperacional"

        
        conexion.commit()
        conexion.close()


    def show_data(self):
        #por ahora solo esta imprimiendo por consola los clientes
        import sqlite3
        conexion = sqlite3.connect(self.nombre)
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM clientes")
        clientes = cursor.fetchall()
        conexion.close()
        return clientes


    def show_client(self,rif=""):
        #muestra los datos de la base de datos un registro unico de un rif
        self.rif = rif
        import sqlite3
        conexion = sqlite3.connect(self.nombre)
        cursor = conexion.cursor()
        cursor.execute("""
        SELECT * FROM clientes WHERE Rif='{}'
        """.format(self.rif))
        cliente = cursor.fetchone()
        if cliente is None:
            print("Cliente no encontrado")
        else:
            return cliente
        
        conexion.close()


    def show_cliente_by_name(self,name = ""):
        self.name = name
        conexion = sqlite3.connect(self.nombre)
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT * FROM clientes WHERE Cliente LIKE ?
            """, ("%" + self.name + "%",)
        )
        cliente = cursor.fetchall()
        return cliente

    def export_database(self,filename = ""):
        self.filename = filename
        excel = Workbook(self.filename)
        worksheet = excel.add_worksheet()
        conexion = sqlite3.connect(self.nombre)
        cursor = conexion.cursor()
        database = cursor.execute("SELECT * FROM clientes")
        for i, row in enumerate(database):
            for j, value in enumerate(row):
                worksheet.write(i,j,value)
        excel.close()
        conexion.close()

