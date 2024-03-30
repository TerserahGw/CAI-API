const sidebar = document.getElementById('sidebar');
const sidebarToggle = document.getElementById('sidebar-toggle');
const menuBtn = document.getElementById('menu-btn');
const contentTitle = document.getElementById('content-title');
const content = document.getElementById('content');
let currentMenu = null;

function changeContent(menu) {
    if (menu === currentMenu) {
        return;
    }
    currentMenu = menu;
    contentTitle.innerText = menu; 
    if (menu === 'Dashboard') {
        content.innerHTML = `
            <div class="container">
                <div class="container-item">
                    <h3>Informasi Penggunaan API</h3>
                    <p>Gunakanlah API Saya Dengan Bijak, Tolong Beri kredit Saat Memakai Api Saya, Api Ini Bisa Untuk Berbagai Macam Hal Contohnya Bot Telegram,Bot Whatsapp, Bot Discord, Website, Dll</p>
                    <p>Mungkin Kedepannya Akan Saya Tambahkan Berbagai Macam Fitur Dan Memperbaharui UI. Untuk Mensupport Saya Berikan Star Pada Github Saya</p>
                </div>
                <div class="container-item">
                    <h3>Back To Simpel UI</h3>
                    <p>Kembali Ke Tampilan Lama!.</p>
                    <a href="/api">Let's Go!</a>
                </div>
            </div>
        `;
    } else if (menu === 'CharacterAI1') {
        content.innerHTML = `
            <div class="container">
                <div class="container-item">
                    <h3>Cari Karakter</h3>
                    <p>Mencari karakter dengan memasukkan kueri.</p>
                    <a href="/api/search?q=">Coba Sekarang</a>
                    <p><strong>Parameter Variable:</strong> q : (search adalah nama character)</p>
                </div>
                <div class="container-item">
                    <h3>Mulai Obrolan Baru</h3>
                    <p>Mulai sesi obrolan baru dengan karakter.</p>
                    <a href="/api/newchat?q=">Coba Sekarang</a>
                    <p><strong>Parameter Variable:</strong> q : (newchat adalah id character)</p>
                </div>
                <div class="container-item">
                    <h3>Karakter yang Sedang Tren</h3>
                    <p>Melihat karakter yang sedang tren saat ini.</p>
                    <a href="/api/trending">Coba Sekarang</a>
                </div>
                <div class="container-item">
                    <h3>Karakter yang Direkomendasikan</h3>
                    <p>Melihat karakter yang direkomendasikan untuk saat ini.</p>
                    <a href="/api/rec">Coba Sekarang</a>
                </div>
                <div class="container-item">
                    <h3>Buat Character AI</h3>
                    <p>Membuat Char Anda Sendiri.</p>
                    <a href="/api/create?name=&greeting=&identifier=">Coba Sekarang</a>
                    <p><strong>Parameter Variable:</strong> name, greeting, identifier</p>
                </div>
                <div class="container-item">
                    <h3>Obrolan dengan Character AI</h3>
                    <p>Terlibat dalam percakapan dengan karakter AI.</p>
                    <a href="/api/cai?charid=&message=">Coba Sekarang</a>
                    <p><strong>Parameter Variable:</strong> charid, message</p>
                </div>
            </div>
        `;
    } else if (menu === 'CharacterAI2') {
        content.innerHTML = `
            <div class="container">
                <div class="container-item">
                    <h3>Cooming Soon</h3>
                    <p>Sedang Dikerjakan, Mohon Pakai V1</p>
                    <a href="/api?q=">Coba CharacterAI 1</a>
                    <p><strong>Have Fun</strong></p>
                </div>
                <!-- Add more content for CharacterAI2 -->
            </div>
        `;
    } else if (menu === 'OtherAPI') {
        content.innerHTML = `
            <div class="container">
                <div class="container-item">
                    <h3>YTDL</h3>
                    <p>Mengunduh video YouTube dengan URL yang diberikan.</p>
                    <a href="https://keila-api.vercel.app/youtube?q=">Coba Sekarang</a>
                    <p><strong>Parameter Variable:</strong> q : (URL video YouTube)</p>
                </div>
                <div class="container-item">
                    <h3>YTPlay</h3>
                    <p>Memutar audio YouTube dengan judul yang diberikan.</p>
                    <a href="https://keila-api.vercel.app/play?q=">Coba Sekarang</a>
                    <p><strong>Parameter Variable:</strong> q : (judul lagu atau video YouTube)</p>
                </div>
                <div class="container-item">
                    <h3>Pixiv</h3>
                    <p>Mencari gambar di Pixiv berdasarkan kata kunci.</p>
                    <a href="https://keila-api.vercel.app/pixiv?q=">Coba Sekarang</a>
                    <p><strong>Parameter Variable:</strong> q : (kata kunci pencarian)</p>
                </div>
                <!-- Add more content for OtherAPI -->
            </div>
        `;
    }
    sidebar.classList.remove('show');
}

// api.js

sidebarToggle.addEventListener('click', function() {
    sidebar.classList.toggle('show');
});

menuBtn.addEventListener('click', function() {
    sidebar.classList.toggle('show');
});

function openUrl(url) {
    window.open(url, '_blank');
}

document.addEventListener("DOMContentLoaded", function() {
    changeContent('Dashboard');
});
