// Анимации при скролле и взаимодействии
document.addEventListener('DOMContentLoaded', function() {
    // Анимация появления элементов при скролле
    const animatedElements = document.querySelectorAll('.course-card, .lesson-content, .feature-item');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1 });
    
    animatedElements.forEach(element => {
        element.style.transition = 'all 0.6s ease';
        observer.observe(element);
    });

    // Плавающая анимация для иконок
    const floatingIcons = document.querySelectorAll('.course-icon, .feature-icon');
    floatingIcons.forEach(icon => {
        icon.style.animation = 'float 5s ease-in-out infinite';
    });

    // Параллакс эффект для звездного фона
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const parallaxElements = document.querySelectorAll('.space-bg');
        
        parallaxElements.forEach(element => {
            const rate = scrolled * -0.5;
            element.style.transform = `translate3d(0px, ${rate}px, 0px)`;
        });
    });
});

// Глобальные функции для навигации
function goBackToSelection() {
    const courseSelection = document.querySelector('.course-selection');
    const lessonContainer = document.getElementById('lessonContainer');
    
    lessonContainer.style.transition = 'all 0.5s ease';
    lessonContainer.style.opacity = '0';
    lessonContainer.style.transform = 'translateY(20px)';
    
    setTimeout(() => {
        lessonContainer.style.display = 'none';
        courseSelection.style.display = 'block';
        
        setTimeout(() => {
            courseSelection.style.opacity = '1';
            courseSelection.style.transform = 'translateY(0)';
        }, 50);
    }, 500);
}

function startCourse(course) {
    const courseSelection = document.querySelector('.course-selection');
    const lessonContainer = document.getElementById('lessonContainer');
    
    courseSelection.style.transition = 'all 0.5s ease';
    courseSelection.style.opacity = '0';
    courseSelection.style.transform = 'translateY(20px)';
    
    setTimeout(() => {
        courseSelection.style.display = 'none';
        lessonContainer.style.display = 'block';
        
        const courseContent = generateCourseContent(course);
        lessonContainer.querySelector('.container').innerHTML = courseContent;
        
        setTimeout(() => {
            lessonContainer.style.transition = 'all 0.5s ease';
            lessonContainer.style.opacity = '1';
            lessonContainer.style.transform = 'translateY(0)';
        }, 50);
    }, 500);
}

function generateCourseContent(course) {
    const courseData = {
        'traveler': {
            title: 'Космический путешественник',
            description: 'Основы Astra Linux для начинающих',
            modules: 6,
            color: 'var(--star)'
        },
        'navigator': {
            title: 'Сетевой штурман', 
            description: 'Сетевое администрирование и безопасность',
            modules: 5,
            color: 'var(--comet)'
        },
        'engineer': {
            title: 'Космический инженер',
            description: 'Продвинутое администрирование и разработка',
            modules: 5,
            color: 'var(--rocket)'
        }
    };

    const data = courseData[course] || courseData['traveler'];

    return `
        <div class="progress-container">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h4>${data.title} - Урок 1 из ${data.modules}</h4>
                <span style="color: var(--comet);">Прогресс: 0%</span>
            </div>
            <div class="progress">
                <div class="progress-bar" style="width: 0%"></div>
            </div>
        </div>

        <div class="lesson-content visible">
            <h1 class="mb-4" style="color: ${data.color};">${data.title}</h1>
            <p class="lead mb-4">${data.description}</p>
            
            <div class="comic-panel">
                <div class="character-dialog">
                    <div class="character-name">Кряк</div>
                    <p>Ура! Мы начинаем наше космическое путешествие в мир ${data.title}! Я так excited!</p>
                </div>
                
                <div class="character-dialog" style="margin-left: 2rem;">
                    <div class="character-name">Др. Крядберг</div>
                    <p>Отлично, Кряк! В этом курсе мы изучим все необходимое для успешного освоения ${data.title}. Готовься к увлекательным приключениям!</p>
                </div>

                <div class="character-dialog">
                    <div class="character-name">Крякель</div>
                    <p>Наш корабль готов к запуску! Системы проверены, можно начинать обучение!</p>
                </div>
            </div>

            <div class="comic-panel">
                <h4 style="color: var(--comet);">📖 Что вас ждет в этом курсе:</h4>
                <ul class="mt-3">
                    <li>Интерактивные уроки с комиксами</li>
                    <li>Практические задания и тесты</li>
                    <li>Автоматическая проверка знаний</li>
                    <li>Система прогресса и достижений</li>
                    <li>Поддержка нашей космической эскадры</li>
                </ul>
            </div>

            <div class="text-center mt-5">
                <button class="btn btn-space btn-lg" onclick="startFirstLesson('${course}')">
                    <i class="fas fa-rocket me-2"></i>Начать первый урок
                </button>
            </div>
        </div>

        <div class="lesson-navigation text-center mt-4">
            <button class="btn btn-outline-space" onclick="goBackToSelection()">
                <i class="fas fa-arrow-left me-2"></i>Вернуться к выбору курса
            </button>
        </div>
    `;
}

function startFirstLesson(course) {
    alert(`🚀 Запускаем первый урок курса "${course}"! В будущем здесь будет загружаться контент урока.`);
}