# Добавляем текущую папку в sys.path для 
# корректного импорта зависимостей db_config

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db_config import DatabaseConnection
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from psycopg2 import sql

# Датакласс пользователя

@dataclass
class User:
    first_name: str
    second_name: str
    phone_number: str
    email: str

# DAO-класс для работы с пользователями

class UserDAO:
    """DAO для работы с пользователями"""
    
    def __init__(self, db_connection: DatabaseConnection):
        self.db = db_connection
    
    def create(self, user: Dict[str, Any]) -> int:
        """Создание нового пользователя"""

        set_clause = []
        values = []
        
        for key, value in user.items():
            set_clause.append(sql.Identifier(key))
            values.append(value)

        query = sql.SQL("""
            INSERT INTO users ({})
            VALUES ({})
            RETURNING id
        """).format(
            sql.SQL(', ').join(set_clause),
            sql.SQL(', ').join(sql.Placeholder() * len(set_clause))
        )
        
        with self.db.get_cursor() as cursor:
            cursor.execute(query, values)
            return cursor.fetchone()[0]
    
    def read(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Получение пользователя по ID"""
        query = sql.SQL("""
            SELECT id, first_name, last_name, phone_number, email
            FROM users
            WHERE id = %s
        """)
        
        with self.db.get_cursor() as cursor:
            cursor.execute(query, (user_id,))
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'first_name': row[1],
                    'last_name': row[2],
                    'phone_number': row[3],
                    'email': row[4]
                }
            return None
    
    def update(self, user_id: int, data: Dict[str, Any]) -> bool:
        """Обновление данных пользователя"""
        if not data:
            return False
        
        set_clause = []
        values = []
        
        for key, value in data.items():
            set_clause.append(sql.Identifier(key))
            values.append(value)
        
        query = sql.SQL("""
            UPDATE users
            SET ({}) = ROW ({})
            WHERE id = %s
        """).format(
            sql.SQL(', ').join(set_clause),
            sql.SQL(', ').join(sql.Placeholder() * len(set_clause))
        )
        
        values.append(user_id)
        
        with self.db.get_cursor() as cursor:
            cursor.execute(query, values)
            return cursor.rowcount > 0
    
    def delete(self, user_id: int) -> bool:
        """Удаление пользователя"""
        query = sql.SQL("DELETE FROM users WHERE id = %s")
        
        with self.db.get_cursor() as cursor:
            cursor.execute(query, (user_id,))
            return cursor.rowcount > 0
    
    def get_all(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Получение всех пользователей с пагинацией"""
        query = sql.SQL("""
            SELECT id, first_name, last_name, phone_number, email
            FROM users
            ORDER BY id
            LIMIT %s OFFSET %s
        """)
        
        with self.db.get_cursor() as cursor:
            cursor.execute(query, (limit, offset))
            rows = cursor.fetchall()
            return [
                {
                    'id': row[0],
                    'first_name': row[1],
                    'last_name': row[2],
                    'phone_number': row[3],
                    'email': row[4]
                }
                for row in rows
            ]
        
    def get_id_by_name(self, first_name: str, last_name: str) -> Optional[int]:
        """Получение ID пользователя по его имени и фамилии"""
        query = sql.SQL("""
            SELECT id
            FROM users
            WHERE first_name = %s AND last_name = %s
        """)

        with self.db.get_cursor() as cursor:
            cursor.execute(query, (first_name, last_name))
            try:
                user_id = cursor.fetchone()[0]
            except TypeError:
                user_id = None
            return user_id