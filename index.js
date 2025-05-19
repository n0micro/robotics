const PORT = 3000;
let robots = [];
let currentRobotIndex = 0;
let currentImageIndex = 0;

function loadRobots() {
    fetch('/robots.json')
        .then(response => response.json())
        .then(data => {
            robots = data;
            updateGallery();
        })
        .catch(error => {
            console.error('Помилка завантаження роботів:', error);
            // Тестові дані для демонстрації, якщо сервер недоступний
            robots = [
                {
                    id: 1,
                    name: "Робот-помічник",
                    description: "Програмований робот, який може виконувати прості завдання в класі. Розроблений учнями 10-А класу під керівництвом вчителя інформатики.",
                    images: ["https://via.placeholder.com/300x240?text=Робот+1"]
                },
                {
                    id: 2,
                    name: "Робот-дослідник",
                    description: "Інноваційний робот для наукових досліджень. Має датчики температури, вологості та тиску.",
                    
                    images: ["https://via.placeholder.com/300x240?text=Робот+2"]
                },
                {
                    id: 3,
                    name: "Робот-конструктор",
                    description: "Модульний робот для навчання основам робототехніки. Можна збирати в різних конфігураціях.",
                    price: "180 грн.",
                    images: ["https://via.placeholder.com/300x240?text=Робот+3"]
                },
                {
                    id: 4,
                    name: "Робот-художник",
                    description: "Робот, який може малювати різні зображення за допомогою маркерів та олівців.",
                    price: "210 грн.",
                    images: ["https://via.placeholder.com/300x240?text=Робот+4"]
                }
            ];
            updateGallery();
        });
}

function updateGallery() {
    const gallery = document.getElementById('gallery');
    gallery.innerHTML = '';
    
    robots.forEach((robot, index) => {
        const card = document.createElement('div');
        card.className = 'robot-card';
        
        const img = document.createElement('img');
        img.src = robot.images[0];
        img.alt = robot.name || 'Робот';
        img.onclick = () => openModal(index);
        
        const info = document.createElement('div');
        info.className = 'robot-info';
        
        const title = document.createElement('div');
        title.className = 'robot-title';
        title.textContent = robot.name || 'Робот без назви';
        
        const desc = document.createElement('div');
        desc.className = 'robot-desc';
        desc.textContent = robot.description || 'Опис відсутній';
        
        const footer = document.createElement('div');
        footer.className = 'robot-footer';
        
        const price = document.createElement('div');
        
        const button = document.createElement('a');


        
        footer.appendChild(price);
        footer.appendChild(button);
        
        info.appendChild(title);
        info.appendChild(desc);
        info.appendChild(footer);
        
        card.appendChild(img);
        card.appendChild(info);
        
        gallery.appendChild(card);
    });
}

function openModal(index) {
    currentRobotIndex = index;
    currentImageIndex = 0;
    updateModal();
    document.getElementById('modal').style.display = 'flex';
}

function closeModal() {
    document.getElementById('modal').style.display = 'none';
}

function updateModal() {
    const robot = robots[currentRobotIndex];
    document.getElementById('modal-img').src = robot.images[currentImageIndex];
    document.getElementById('modal-description').innerText = robot.description;
}

function nextImage() {
    const robot = robots[currentRobotIndex];
    currentImageIndex = (currentImageIndex + 1) % robot.images.length;
    updateModal();
}

function prevImage() {
    const robot = robots[currentRobotIndex];
    currentImageIndex = (currentImageIndex - 1 + robot.images.length) % robot.images.length;
    updateModal();
}

// Завантаження при старті
window.onload = loadRobots;