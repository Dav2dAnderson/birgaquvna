# Django Startup Project Architecture Guidelines

Ushbu hujjat loyihaning Clean / Modular Monolith arxitekturasi tuzilmasi, papkalarning vazifalari va kod yozish qoidalarini belgilab beradi.

---

## 📁 Papkalar Tuzilmasi (Directory Structure)

```text
.
├── apps/                  # Biznes mantiq modullari (Django Apps)
│   ├── users/             # Foydalanuvchilar va autentifikatsiya
│   ├── products/          # Mahsulotlar / Xizmatlar
│   └── orders/            # Buyurtmalar va to'lovlar
├── config/                # Loyiha global sozlamalari
│   ├── settings/          # Muhitlar bo'yicha settings (base, local, prod)
│   ├── urls.py            # Asosiy URL marshrutlari
│   ├── asgi.py            # Async / WebSocket qo'llab-quvvatlash
│   └── wsgi.py            # Standard Web Server interface
├── core/                  # Umumiy / Shared komponentlar
│   ├── models.py          # Base models (TimeStampedModel, UUIDModel)
│   ├── exceptions.py      # Custom exception xatolar
│   ├── permissions.py     # Global ruxsatnomalar
│   └── utils/             # Yordamchi utilitalar
├── infra/                 # Infratuzilma va Deployment
│   ├── docker/            # Dockerfile va Nginx konfiguratsiyalari
│   └── docker-compose.yml # Container orchestration
├── requirements/          # Kutubxonalar ro'yxati
│   ├── base.txt           # Asosiy kutubxonalar
│   ├── local.txt          # Development uchun
│   └── prod.txt           # Production uchun
├── tests/                 # End-to-End va Integratsion testlar
├── .env.example           # Muhit o'zgaruvchilari shabloni
├── .gitignore             # Git ga qo'shilmaydigan fayllar
└── manage.py              # Django buyruqlar fayli
```

---

## 🔍 Qatlamlar va Papkalar Tafsiloti

### 1. `apps/` — Biznes Modullari
Har bir domen alohida Django dasturi (app) sifatida shakllantiriladi.
Har bir app ichidagi tavsiya etiladigan fayllar tuzilmasi:
* `models.py` — Ma'lumotlar bazasi jadvallari va ORM strukturasi.
* `views.py` / `api.py` — HTTP/REST API controller/endpoint'lar.
* `serializers.py` — REST API uchun validation va serialization.
* `services.py` — **Biznes logika** (Data mutation, to'lovlar, uchinchi tomon API integratsiyalari).
* `selectors.py` — Ma'lumotlarni bazadan o'qish (Read-only queries).

### 2. `bot/` — Telegram Bot Integratsiyasi
* Bot to'g'ridan-to'g'ri Django ORM va `apps/*/services.py` dagi biznes logikadan foydalanadi.
* Bot kodi va Web kodi biznes logikani takrorlamaydi, bitta `service` funksiyasini chaqiradi.

### 3. `config/` — Global Sozlamalar
* `settings/` papkasi 3 ga bo'linadi:
  * `base.py` — Barcha ortamlar uchun umumiy sozlamalar.
  * `local.py` — Lokal ishlab chiqish uchun.
  * `prod.py` — Server (Production) muhiti uchun.

### 4. `core/` — Qayta Ishlatiluvchi Komponentlar
* Loyihadagi barcha modullar uchun umumiy bo'lgan base modellar (masalan `created_at`, `updated_at` maydonlariga ega `TimeStampedModel`).
* *Qoida:* `core/` moduli ichidagi fayllar `apps/` papkasidan hech narsa import qilmasligi shart!

### 5. `infra/` — Deployment va Infratuzilma
* Deployment uchun kerakli barcha Dockerfile, Nginx config, Systemd unit fayllari va CI/CD skriptlari shu yerda saqlanadi.

---

## 🛠 Kod Yozish Qoidalari (Architecture Rules)

1. **Fat Services, Thin Views:** `views.py` yoki bot handler'lar ichida murakkab biznes logika yozilmaydi. Barcha logika `services.py` ga chiqariladi.
2. **Circular Dependency Taqiqi:** Bitta app boshqa app'ga to'g'ridan-to me'yordan ortiq bog'lanib qolmasligi kerak.
3. **Virtual Environment:** `myenv/` yoki `.venv` papkasi har doim `.gitignore` ga kiritiladi va repo'ga yuklanmaydi.