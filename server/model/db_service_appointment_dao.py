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

# Датакласс услуги автосервиса

@dataclass
class ServiceAppointment:
    service_name: str
    date: datetime
    time: datetime
    client_id: int

# DAO-класс для работы с записями на услуги автосервиса

class ServiceAppointmentDAO:
    """DAO для работы с записями услуг"""
    
    def __init__(self, db_connection: DatabaseConnection):
        self.db = db_connection
    
    def create(self, appointment: Dict[str, Any]) -> int:
        """Создание новой записи"""
        query = sql.SQL("""
            INSERT INTO service_appointments (service_name, date, time, client_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """)
        
        with self.db.get_cursor() as cursor:
            cursor.execute(query, (appointment['service_name'], appointment['date'], appointment['time'], appointment['client_id']))
            return cursor.fetchone()[0]
    
    def read(self, appointment_id: int) -> Optional[Dict[str, Any]]:
        """Получение записи по ID"""
        query = sql.SQL("""
            SELECT id, service_name, date, time, client_id
            FROM service_appointments
            WHERE id = %s
        """)
        
        with self.db.get_cursor() as cursor:
            cursor.execute(query, (appointment_id,))
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'service_name': row[1],
                    'date': row[2],
                    'time': row[3],
                    'client_id': row[4]
                }
            return None
    
    def update(self, appointment_id: int, data: Dict[str, Any]) -> bool:
        """Обновление записи"""
        if not data:
            return False
        
        set_clause = []
        values = []
        
        for key, value in data.items():
            set_clause.append(sql.Identifier(key))
            values.append(value)
        
        query = sql.SQL("""
            UPDATE service_appointments
            SET ({}) = ROW ({})
            WHERE id = %s
        """).format(
            sql.SQL(', ').join(set_clause),
            sql.SQL(', ').join(sql.Placeholder() * len(set_clause))
        )
        
        values.append(appointment_id)
        
        with self.db.get_cursor() as cursor:
            cursor.execute(query, values)
            return cursor.rowcount > 0
    
    def delete(self, appointment_id: int) -> bool:
        """Удаление записи"""
        query = sql.SQL("DELETE FROM service_appointments WHERE id = %s")
        
        with self.db.get_cursor() as cursor:
            cursor.execute(query, (appointment_id,))
            return cursor.rowcount > 0
    
    def get_all(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Получение всех записей с пагинацией"""
        query = sql.SQL("""
            SELECT id, service_name, date, time, client_id
            FROM service_appointments
            ORDER BY id
            LIMIT %s OFFSET %s
        """)
        
        with self.db.get_cursor() as cursor:
            cursor.execute(query, (limit, offset))
            rows = cursor.fetchall()
            return [
                {
                    'id': row[0],
                    'service_name': row[1],
                    'date': row[2],
                    'time': row[3],
                    'client_id': row[4]
                }
                for row in rows
            ]
        
    def get_id_by_date_and_time(self, date: str, time: str) -> Optional[int]:
        """Получение записи по времени и дате"""
        query = sql.SQL("""
            SELECT id
            FROM service_appointments
            WHERE date = %s AND time = %s
        """)

        with self.db.get_cursor() as cursor:
            cursor.execute(query, (date, time))
            try:
                appointment_id = cursor.fetchone()[0]
            except TypeError:
                appointment_id = None
            return appointment_id