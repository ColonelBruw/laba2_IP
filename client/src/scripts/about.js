let theme_btn = document.getElementById('Theme');

//Функция переключения темы
function switchTheme() {
        theme_btn_img = theme_btn.firstElementChild.src
        if (theme_btn_img.split("/").at(-1) === "moon.png") {
            document.documentElement.setAttribute('data-theme', 'dark');
            document.querySelector('#ThemeIcon').src = '/sun.jpg'
            document.querySelector('#HeaderImg').src = '/carfast_negate.png'
        } else {
            document.documentElement.setAttribute('data-theme', 'light')
            document.querySelector('#ThemeIcon').src = '/moon.png'
            document.querySelector('#HeaderImg').src = '/carfast.png'
        }
    }
    
//Смена темы
theme_btn.addEventListener('click', switchTheme);