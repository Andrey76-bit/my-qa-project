const translations = {
    ru: {
        title: "IT Start",
        subtitle: "Твой проводник в мир технологий",
        professions_title: "Выбери свою профессию",
        prof_qa: "QA Engineer — тестирование ПО",
        qa_desc: "QA-инженер проверяет программы на ошибки, пишет тесты и автоматизирует проверки. Очень востребованная профессия для входа в IT.",
        prof_dev: "Разработчик (Python, JavaScript)",
        dev_desc: "Разработчик пишет код, создаёт сайты, приложения и сервисы. Python отлично подходит для бэкенда и автоматизации, JavaScript — для фронтенда.",
        prof_devops: "DevOps — автоматизация и инфраструктура",
        devops_desc: "DevOps-инженер связывает разработку и эксплуатацию: настраивает CI/CD, Docker, Kubernetes, следит за стабильностью систем.",
        start_title: "С чего начать?",
        start_1: "Изучи основы программирования (Python или JavaScript).",
        start_2: "Пройди базовый курс по выбранной профессии.",
        start_3: "Практикуйся: пиши проекты, тесты, скрипты.",
        start_4: "Собери портфолио на GitHub.",
        start_5: "Откликайся на вакансии и не бойся отказов.",
        history_title: "Моя история",
        history_text: "Привет! Я Андрей. Мой путь в IT начался с старого ноутбука ASUS и желания освоить новую профессию. Я установил Linux, научился работать с терминалом, изучил Python, SQL, Selenium, Playwright, Docker, CI/CD и основы безопасности. Сегодня у меня есть портфолио на GitHub и первые отклики от работодателей. Я верю, что каждый может войти в IT, если идти шаг за шагом и не сдаваться.",
        knowledge_title: "Что нужно для старта",
        knowledge_python: "Основы Python или JavaScript",
        knowledge_python_desc: "Начни с синтаксиса, переменных, циклов и функций. Python отлично подходит для новичков.",
        knowledge_sql: "SQL и базы данных",
        knowledge_sql_desc: "Умение писать SELECT, JOIN, GROUP BY помогает тестировщику проверять данные.",
        knowledge_testing: "Тестирование ПО (ручное и автоматизация)",
        knowledge_testing_desc: "Изучи тест-дизайн, баг-репорты и основы Selenium/Playwright — это сердце QA.",
        knowledge_git: "Работа с Git и GitHub",
        knowledge_git_desc: "Git нужен для контроля версий, совместной работы и портфолио. Начни с commit, push, branch.",
        knowledge_cicd: "Понимание CI/CD и Docker",
        knowledge_cicd_desc: "CI/CD автоматизирует проверки, Docker упаковывает окружение. Очень ценятся в командах.",
        knowledge_english: "Английский на уровне чтения документации",
        knowledge_english_desc: "Хотя бы базовый английский открывает доступ к лучшим материалам и удалённым вакансиям.",
        footer: "Сделано с душой для начинающих айтишников"
    },
    en: {
        title: "IT Start",
        subtitle: "Your guide to the world of technology",
        professions_title: "Choose your profession",
        prof_qa: "QA Engineer — software testing",
        qa_desc: "QA engineer checks software for bugs, writes tests, and automates checks. Very in-demand profession for entering IT.",
        prof_dev: "Developer (Python, JavaScript)",
        dev_desc: "Developer writes code, creates websites, apps, and services. Python is great for backend and automation, JavaScript for frontend.",
        prof_devops: "DevOps — automation and infrastructure",
        devops_desc: "DevOps engineer connects development and operations: sets up CI/CD, Docker, Kubernetes, ensures system stability.",
        start_title: "Where to start?",
        start_1: "Learn programming basics (Python or JavaScript).",
        start_2: "Take a basic course in your chosen field.",
        start_3: "Practice: write projects, tests, scripts.",
        start_4: "Build a GitHub portfolio.",
        start_5: "Apply for jobs and don't be afraid of rejections.",
        history_title: "My story",
        history_text: "Hi! I'm Andrey. My journey into IT started with an old ASUS laptop and a desire to learn a new profession. I installed Linux, learned to work with the terminal, studied Python, SQL, Selenium, Playwright, Docker, CI/CD and security basics. Today I have a portfolio on GitHub and first responses from employers. I believe everyone can enter IT if you go step by step and never give up.",
        knowledge_title: "What you need to start",
        knowledge_python: "Basics of Python or JavaScript",
        knowledge_python_desc: "Start with syntax, variables, loops and functions. Python is great for beginners.",
        knowledge_sql: "SQL and databases",
        knowledge_sql_desc: "Ability to write SELECT, JOIN, GROUP BY helps testers verify data.",
        knowledge_testing: "Software testing (manual and automation)",
        knowledge_testing_desc: "Learn test design, bug reports, and basics of Selenium/Playwright — this is the heart of QA.",
        knowledge_git: "Git and GitHub",
        knowledge_git_desc: "Git is needed for version control, collaboration, and portfolio. Start with commit, push, branch.",
        knowledge_cicd: "Understanding CI/CD and Docker",
        knowledge_cicd_desc: "CI/CD automates checks, Docker packages environment. Highly valued in teams.",
        knowledge_english: "English for reading documentation",
        knowledge_english_desc: "At least basic English opens access to the best materials and remote vacancies.",
        footer: "Made with soul for beginner IT specialists"
    }
};

function setLanguage(lang) {
    localStorage.setItem('lang', lang);
    applyLanguage();
}

function applyLanguage() {
    const lang = localStorage.getItem('lang') || 'ru';
    document.querySelectorAll('[data-i18n]').forEach(element => {
        const key = element.getAttribute('data-i18n');
        if (translations[lang] && translations[lang][key]) {
            element.textContent = translations[lang][key];
        }
    });
    document.documentElement.lang = lang;
}

// Аккордеон первого уровня
document.addEventListener('click', function(e) {
    const header = e.target.closest('.accordion-header');
    if (header) {
        const item = header.parentElement;
        const content = item.querySelector('.accordion-content');
        const isActive = content.classList.contains('active');
        document.querySelectorAll('.accordion-content.active').forEach(c => c.classList.remove('active'));
        if (!isActive) {
            content.classList.add('active');
        }
    }

    // Вложенные подпункты
    const subHeader = e.target.closest('.sub-header');
    if (subHeader) {
        const subItem = subHeader.parentElement;
        const subContent = subItem.querySelector('.sub-content');
        if (subContent) {
            subContent.classList.toggle('active');
        }
    }
});

applyLanguage();
