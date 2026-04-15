from dataclasses import dataclass
from contextlib import contextmanager
from psycopg2 import pool

@dataclass
class DatabaseConfig:
    host: str
    port: int
    database: str
    user: str
    password: str
    min_connections: int
    max_connections: int

class DatabaseConnection:
    """Управление пулом соединений с БД"""
    
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self._pool = None
    
    def connect(self):
        """Инициализация пула соединений"""
        self._pool = pool.SimpleConnectionPool(
            self.config.min_connections,
            self.config.max_connections,
            host=self.config.host,
            port=self.config.port,
            database=self.config.database,
            user=self.config.user,
            password=self.config.password
        )
    
    @contextmanager
    def get_cursor(self):
        """Контекстный менеджер для получения курсора"""
        conn = self._pool.getconn()
        try:
            yield conn.cursor()
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            self._pool.putconn(conn)
    
    def close(self):
        """Закрытие всех соединений"""
        self._pool.closeall()