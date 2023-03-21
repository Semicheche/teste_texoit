import jaydebeapi
import os
import yaml
from yaml.loader import SafeLoader


class Base(object):
    _instance = None

    def __init__(self):
        try:
            self.cur_dir = os.path.dirname(os.path.abspath(__file__))
            with open(f'{self.cur_dir}/config.yaml', 'r') as f:
                self.data = yaml.load(f, Loader=SafeLoader)


            self.driver = self.data['h2']['driver']
            self.url =  self.data['h2']['url']
            self.driver_args = self.data['h2']['args']
            self.jars = f"{self.cur_dir}/{self.data['h2']['jars']}"
            self.connection = jaydebeapi.connect(jclassname=self.driver,
                                    url= self.url,
                                    driver_args= self.driver_args,
                                    jars=self.jars,)
        except ConnectionError:
            print("Erro ao conctar ao Banco de Dados")
            return False

        self._create_tables()

    def cursor(self):
        return self.connection.cursor()

    def _create_tables(self):
        cursor = self.cursor()

        self._check_table_exist(cursor)
        cursor.execute(("CREATE TABLE movie ("
                        "`id` INTEGER PRIMARY KEY AUTO_INCREMENT,"
                        "`year` INTEGER,"
                        "`title` VARCHAR(255),"
                        "`studio` VARCHAR(255),"
                        "`producer` VARCHAR(255),"
                        "`winner` BOOLEAN DEFAULT NULL"
                        ");"))
        cursor.close()
        self._seed_database()

    def _check_table_exist(self, cursor):
        cursor.execute(("DROP TABLE IF EXISTS movie;"))

    def _seed_database(self):
        cursor = self.connection.cursor()
        filename = 'movielist.csv'

        if not os.path.exists(f'{self.cur_dir}/{filename}'):
            return FileExistsError
        try:
            print("---- READ FILE SEED ----")
            cursor.execute(f"SELECT * FROM CSVREAD('{self.cur_dir}/{filename}',null,'charset=UTF-8 fieldSeparator=;');")
            values = cursor.fetchall()

            print("---- POPULATED TABLE ----")
            sql = "INSERT INTO movie(`year`, `title`, `studio`, `producer`, `winner`) VALUES (?, ?, ?, ?, ?)"
            cursor.executemany(sql, values)
            cursor.close()
        except Exception:
            print("Error ao ler e inserir dados no Banco")
            return False

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance