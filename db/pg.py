import psycopg2
"""
Postgresql connection class
"""
class Pg:
    # def __init__(self):
    #     self.database="postgres"
    #     self.user = "liupengju"
    #     self.password = "liupengju"
    #     self.host = "10.77.110.152"
    #     self.port = "5433"

    def __init__(self):
        self.database="postgres"
        self.user = "postgres"
        self.password = "postgres"
        self.host = "10.77.10.171"
        self.port = "5432"

    def get_conn(self):
        conn = psycopg2.connect(database=self.database, user=self.user, password=self.password, host=self.host, port=self.port)
        return conn