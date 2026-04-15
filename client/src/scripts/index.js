// import { API_HOST, API_PORT } from 'astro:env/client';

const modal = document.getElementById('Modal');
const modal_btn = document.getElementById('EmploymentButton');
const submit_btn = document.getElementById('SubmitButton');
const theme_btn = document.getElementById('Theme');
const close_span = document.querySelector('.CloseModal');

// Открытие формы
modal_btn.addEventListener('click', function() {
    modal.style.display = 'block'
});

// Закрытие формы по крестику
close_span.addEventListener('click', function() {
    modal.style.display = 'none'
});

// Отправка данных формы
modal.onsubmit = async (event) => {
    event.preventDefault();

    submit_btn.disabled = true;

    const formData = new FormData(modal);

    console.log(formData)

    try {
        // Отправка данных на FastAPI сервер
        const response = await fetch(`http://localhost:8000/api/submit-job-application`, {
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
        modal.style.display = 'none'
    }
});

//Функция переключения темы
function switchTheme() {
        theme_btn_img = theme_btn.firstElementChild.src
        if (theme_btn_img.split("/").at(-1) === "moon.png") {
            document.documentElement.setAttribute('data-theme', 'dark');
            document.querySelector('#ThemeIcon').src = '/sun.jpg'
            document.querySelector('#HeaderImg').src = '/carfast_negate.png'
            document.querySelector('#UpperDiv1Img').src = '/carfast_negate.png'
        } else {
            document.documentElement.setAttribute('data-theme', 'light')
            document.querySelector('#ThemeIcon').src = '/moon.png'
            document.querySelector('#HeaderImg').src = '/carfast.png'
            document.querySelector('#UpperDiv1Img').src = '/carfast.png'
        }
    }
    
//Смена темы
theme_btn.addEventListener('click', switchTheme);

//Установка картинок на задний план в блоке выбора услуг
for (let i = 1; i < 7; i++) {
    let service_button = document.getElementById('ServiceBlock' + i)
    service_button.style.setProperty('background-image', 'url("services' + i + '.jpg")');
}