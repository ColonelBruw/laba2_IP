# Добавляем текущую папку в sys.path для 
# корректного импорта зависимостей db_config

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db_config import DatabaseConnection
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

###### Абстрактный DAO-класс ######

class BaseDAO(ABC):
    """Абстрактный базовый DAO класс"""
    
    def __init__(self, db_connection: DatabaseConnection):
        self.db = db_connection
    
    @abstractmethod
    def create(self, data: Dict[str, Any]) -> Any:
        pass
    
    @abstractmethod
    def read(self, id: Any) -> Optional[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def update(self, id: Any, data: Dict[str, Any]) -> bool:
        pass
    
    @abstractmethod
    def delete(self, id: Any) -> bool:
        pass
    
    def get_all(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Получение всех записей с пагинацией"""
        pass