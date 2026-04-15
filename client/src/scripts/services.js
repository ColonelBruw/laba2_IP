// import { API_HOST, API_PORT } from 'astro:env/client';

const modal = document.getElementById('Modal');
const modal_btns = document.querySelectorAll('.TheService')
const submit_btn = document.getElementById('SubmitButton');
const theme_btn = document.getElementById('Theme');
const close_span = document.querySelector('.CloseModal');

// Задание динамических пределов установления даты в форме
// Записаться можно начиная с завтрашнего дня в интервале 3 месяцев
const min_input_date = new Date();
min_input_date.setDate(min_input_date.getDate() + 1);

const max_input_date = new Date();
max_input_date.setMonth(max_input_date.getMonth() + 3);

document.querySelector('#InputDate').min = min_input_date.toISOString().split('T')[0];
document.querySelector('#InputDate').max = max_input_date.toISOString().split('T')[0];

// Закрытие по крестику
close_span.addEventListener('click', function() {
    modal.style.display = 'none';
});

// Отправка данных формы
modal.onsubmit = async (event) => {
    event.preventDefault();

    submit_btn.disabled = true;

    const formData = new FormData(modal);
    service_name = document.querySelector('.Modal h2').textContent
    formData.append('service_name', service_name)

    console.log(formData)

    try {
        // Отправка данных на FastAPI сервер
        const response = await fetch(`http://localhost:8000/api/submit-service-appointment`, {
            method: 'POST', 
            body: formData
        });

        const result = await response.json();
        console.log(result.pos)

        if (response.ok) {
            if (result.status === "200") {
                alert(result.message)
                modal.reset()
                modal.style.display = 'none'
                submit_btn.disabled = false;
            } else {
                alert(result.message)
                submit_btn.disabled = false;
            }
        } else {
            alert("Ошибка на бекенде")
        }
    } catch (error) {
        alert("Что-то пошло не так...")
    }
}

// Закрытие по клику вне окна
window.addEventListener('click', function(event) {
    if (event.target === modal) {
        modal.style.display = "none"
    }
});

// Функция добавляющая заголовок модальному окну
modal_btns.forEach(btn => {
    btn.addEventListener('click', function() {
        let service_name = btn.querySelector('p').textContent

        let modal_title = document.querySelector('.ModalContent h2')

        modal_title.textContent = service_name
        
        modal.style.display = 'block';
    });
  });

//Функция переключения темы
function switchTheme() {
        theme_btn_img = theme_btn.firstElementChild.src
        if (theme_btn_img.split("/").at(-1) === "moon.png") {
            document.documentElement.setAttribute('data-theme', 'dark');
            document.querySelector('#ThemeIcon').src = '/sun.jpg'
            document.querySelector('#HeaderImg').src = '/carfast_negate.png'

            for (let i = 1; i < 7; i++) {
                document.querySelector('#Service' + i + 'Img').src = '/services1' + i + '_negate.png'
            }
    
        } else {
            document.documentElement.setAttribute('data-theme', 'light')
            document.querySelector('#ThemeIcon').src = '/moon.png'
            document.querySelector('#HeaderImg').src = '/carfast.png'

            for (let i = 1; i < 7; i++) {
                document.querySelector('#Service' + i + 'Img').src = '/services1' + i + '.png'
            }
        }
    }
    
//Смена темы
theme_btn.addEventListener('click', switchTheme);