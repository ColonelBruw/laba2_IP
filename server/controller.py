# Импорт FastAPI
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware

# Импорт зависимостей из модели
from model.db_config import DatabaseConfig, DatabaseConnection
from model.db_user_dao import User, UserDAO
from model.db_job_application_dao import JobApplication, JobApplicationDAO
from model.db_service_appointment_dao import ServiceAppointment, ServiceAppointmentDAO

# Импорт dotenv для доступа к переменным окружения
from dotenv import load_dotenv
import os

# Импорт re для валидации с помощью регулярных выражений
import re

load_dotenv()

print(os.getenv('DB_MIN_CONNS'))

app = FastAPI()
# Настройка CORS для разрешения запросов с фронтенда
app.add_middleware(
    CORSMiddleware,
    # allow_origins=[f"http://{os.getenv("APP_HOST")}:{os.getenv("APP_PORT")}",   # Адрес Astro приложения
    #                f"http://{os.getenv("API_HOST")}:{os.getenv("API_PORT")}/api/submit-job-application",
    #                f"http://{os.getenv("API_HOST")}:{os.getenv("API_PORT")}/api/submit-service-appointment", # Адреса FastAPI приложения
    #                f"http://{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}", # Адрес БД
    #                ],
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

config = DatabaseConfig(
        host = os.getenv('DB_HOST'),
        # host = '0.0.0.0',
        port = os.getenv('DB_PORT'),
        database = os.getenv('DB_NAME'),
        user = os.getenv('DB_USER'),
        password = os.getenv('DB_PASSWORD'),
        minconn = os.getenv('DB_MIN_CONNS'),
        maxconn = os.getenv('DB_MAX_CONNS')
    )

# Валидация формы заявки на работу

@app.post("/api/submit-job-application")
async def handle_job_application(
    first_name: str = Form(..., max_length=30),
    last_name: str = Form(..., max_length=30),
    phone: str = Form(..., max_length=12),
    email: str = Form(..., max_length=30),
    pos: str = Form(..., max_length=30)
):
    if not all(bool(re.match('[а-яА-Я]', name)) for name in (first_name, last_name)):
        return {
            'status': '400',
            'message': 'Впишите имя и фамилию кириллицей, без цифр и спецсимволов'
        }
    
    if not bool(re.match(r'^(\+7|8)\d{10}$', phone)):
        return {
            'status': '400',
            'message': 'Введите номер телефона в одном из форматов \
                        +7ХХХХХХХХХХ, 8XXXXXXXXXX'
        }
    
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not bool(re.match(email_pattern, email)):
        return {
            'status': '400',
            'message': 'Введите корректную электронную почту'
        }
    
    if pos == 'none':
        return {
            'status': '400',
            'message': 'Выберите желаемую должность'
        }
    
    db = DatabaseConnection(config)
    try:
        db.connect()
    except Exception as e:
        print("Не удалось подключиться к БД:", e)
        return {
            'status': '400',
            'message': f'Проблемки'
        }
    else:
        user_dao = UserDAO(db)
        job_application_dao = JobApplicationDAO(db)

        applicant_id = user_dao.get_id_by_name(first_name, last_name)
        if not applicant_id:
            new_user = {
                'first_name': first_name.lower().capitalize(),
                'last_name': last_name.lower().capitalize(),
                'phone_number': phone if phone[0] != '+' else phone[1:],
                'email': email
            }

            applicant_id = user_dao.create(new_user)

        # Если телефон указанный в форме отличается от уже имеющегося в базе, 
        # то заменяем номер в БД на указанный в форме    
        elif user_dao.read(applicant_id)['phone_number'] != phone and user_dao.read(applicant_id)['phone_number'] != phone[1:]:
            user_dao.update(applicant_id, {'phone_number': phone})
        
        new_application = {
            'position_name': pos,
            'applicant_id': applicant_id
        }

        new_application_id = job_application_dao.create(new_application)

    # db.connect()
    # user_dao = UserDAO(db)
    # job_application_dao = JobApplicationDAO(db)

    # applicant_id = user_dao.get_id_by_name(first_name, last_name)
    # if not applicant_id:
    #     new_user = {
    #         'first_name': first_name.lower().capitalize(),
    #         'last_name': last_name.lower().capitalize(),
    #         'phone_number': phone if phone[0] != '+' else phone[1:],
    #         'email': email
    #     }

    #     applicant_id = user_dao.create(new_user)

    # # Если телефон указанный в форме отличается от уже имеющегося в базе, 
    # # то заменяем номер в БД на указанный в форме    
    # elif user_dao.read(applicant_id)['phone_number'] != phone and user_dao.read(applicant_id)['phone_number'] != phone[1:]:
    #     user_dao.update(applicant_id, {'phone_number': phone})
    
    # new_application = {
    #     'position_name': pos,
    #     'applicant_id': applicant_id
    # }

    # new_application_id = job_application_dao.create(new_application)

    return {
            'status': '200',
            'message': f'Заявка под номером {new_application_id} успешно заполнена!'
        }

# Валидация формы записи на услугу

@app.post("/api/submit-service-appointment")
async def handle_job_application(
    date: str = Form(..., max_length=10),
    time: str = Form(..., max_length=5),
    first_name: str = Form(..., max_length=30),
    last_name: str = Form(..., max_length=30),
    phone: str = Form(..., max_length=12),
    service_name: str = Form(..., max_length=30)
    ):
    
    # Валидация введенной даты
    date_pattern = r'^(\d{4})-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$'
    if not bool(re.match(date_pattern, date)):
        return {
            'status': '400',
            'message': 'Выберите дату записи'
        }
    
    # Валидация введенного времени
    time_pattern = r'^([01]\d|2[0-3]):([0-5]\d)$'
    if not bool(re.match(time_pattern, time)):
        return {
            'status': '400',
            'message': 'Выберите время записи'
        }
    
    # Валидация введенного имени
    if not all(bool(re.match('[а-яА-Я]', name)) for name in (first_name, last_name)):
        return {
            'status': '400',
            'message': 'Впишите имя и фамилию кириллицей, без цифр и спецсимволов'
        }
    
    # Валидация введенного номера телефона
    if not bool(re.match(r'^(\+7|8)\d{10}$', phone)):
        return {
            'status': '400',
            'message': 'Введите номер телефона в одном из форматов \
                        +7ХХХХХХХХХХ, 8XXXXXXXXXX'
        }

    db = DatabaseConnection(config)
    try:
        db.connect()
    except Exception as e:
        print("Не удалось подключиться к БД:", e)
    else:
        user_dao = UserDAO(db)
        service_appointment_dao = ServiceAppointmentDAO(db)

        client_id = user_dao.get_id_by_name(first_name, last_name)
        if not client_id:
            new_user = {
                'first_name': first_name.lower().capitalize(),
                'last_name': last_name.lower().capitalize(),
                'phone_number': phone if phone[0] != '+' else phone[1:]
            }

            client_id = user_dao.create(new_user)
        
        # Если телефон указанный в форме отличается от уже имеющегося в базе, 
        # то заменяем номер в БД на указанный в форме    
        elif user_dao.read(client_id)['phone_number'] != phone and user_dao.read(client_id)['phone_number'] != phone[1:]:
            user_dao.update(client_id, {'phone_number': phone if phone[0] != '+' else phone[1:]})

        existing_appointment = service_appointment_dao.get_id_by_date_and_time(date, time)
        if existing_appointment:
            return {
            'status': '400',
            'message': 'Выбранные время и дата заняты. \
                        Пожалуйста, выберите другие время и дату'
        }
        
        new_appointment = {
            'service_name': service_name,
            'date': date,
            'time': time,
            'client_id': client_id
        }

        new_appointment_id = service_appointment_dao.create(new_appointment)

        return {
                'status': '200',
                'message': f'Запись под номером {new_appointment_id} на услугу {service_name} прошла успешно!'
            }