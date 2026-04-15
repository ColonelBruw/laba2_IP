# Добавляем текущую папку в sys.path для 
# корректного импорта зависимостей db_config

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db_config import DatabaseConnection
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from psycopg2 import sql
from datetime import datetime

# Датакласс заявки на трудоустройство

@dataclass
class JobApplication:
    pos_name: str
    applicant_id: int

# DAO-класс для взаимодействия с заявками на работу

class JobApplicationDAO:
    """DAO для работы с заявками на работу"""
    
    def __init__(self, db_connection: DatabaseConnection):
        self.db = db_connection
    
    def create(self, application: Dict[str, Any]) -> int:
        """Создание новой заявки"""
        query = sql.SQL("""
            INSERT INTO job_applications (position_name, applicant_id)
            VALUES (%s, %s)
            RETURNING id
        """)
        
        with self.db.get_cursor() as cursor:
            cursor.execute(query, (application['position_name'], application['applicant_id']))
            return cursor.fetchone()[0]
    
    def read(self, application_id: int) -> Optional[Dict[str, Any]]:
        """Получение заявки по ID"""
        query = sql.SQL("""
            SELECT id, position_name, applicant_id
            FROM job_applications
            WHERE id = %s
        """)
        
        with self.db.get_cursor() as cursor:
            cursor.execute(query, (application_id,))
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'position_name': row[1],
                    'applicant_id': row[2],
                }
            return None
    
    def update(self, application_id: int, data: Dict[str, Any]) -> bool:
        """Обновление заявки"""
        if not data:
            return False
        
        set_clause = []
        values = []
        
        for key, value in data.items():
            set_clause.append(sql.Identifier(key))
            values.append(value)
        
        query = sql.SQL("""
            UPDATE job_applications
            SET ({}) = ROW ({})
            WHERE id = %s
        """).format(
            sql.SQL(', ').join(set_clause),
            sql.SQL(', ').join(sql.Placeholder() * len(set_clause))
        )
        
        values.append(application_id)
        
        with self.db.get_cursor() as cursor:
            cursor.execute(query, values)
            return cursor.rowcount > 0
    
    def delete(self, appointment_id: int) -> bool:
        """Удаление заявки"""
        query = sql.SQL("DELETE FROM job_applications WHERE id = %s")
        
        with self.db.get_cursor() as cursor:
            cursor.execute(query, (appointment_id,))
            return cursor.rowcount > 0
    
    def get_all(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Получение всех заявок с пагинацией"""
        query = sql.SQL("""
            SELECT id, position_name, applicant_id
            FROM job_applications
            ORDER BY id
            LIMIT %s OFFSET %s
        """)
        
        with self.db.get_cursor() as cursor:
            cursor.execute(query, (limit, offset))
            rows = cursor.fetchall()
            return [
                {
                    'id': row[0],
                    'position_name': row[1],
                    'applicant_id': row[2]
                }
                for row in rows
            ]