
## Описание проекта
Сервис по сбору вакансий по указанным параметрам клиента и рассылка по почте

### Стек технологий
- Django
- Selenium
- schedule
- PostgreSQL
- Docker
- asyncio
- Pytest
---

### Установка
Перед запуском проекта убедитесь, что у вас установлен python, docker и docker-compose.

```bash
python --version
```

```
docker --version
```

```
docker-compose --version
```

Переходим в рабочую директорию и клонируем проект.

```bash
git clone https://github.com/Timur-Razzakov/data_collection_service
```

Установливаем зависимости.

```
pip install -r requirements.txt
```

Создаём .env файл и добавляем следующие настройки

- Настройки сервера
  - `SERVER_HOST=`... (поумолчанию 0.0.0.0)
  - `SERVER_PORT=`... (поумолчанию 8000)
  
- Настройки базы данных 
  - `POSTGRES_HOST=`... (поумолчанию 0.0.0.0)
  - `POSTGRES_PORT=`... (поумолчанию 5432)
  - `POSTGRES_DB=`... (обязательное поле)
  - `POSTGRES_USER=`... (обязательное поле)
  - `POSTGRES_PASSWORD=`... (обязательное поле)
 
- Настройка Email 
  - `EMAIL_HOST=`... (поумолчанию smtp.gmail.com)
  - `EMAIL_PORT=`... (поумолчанию 587)
  - `EMAIL_HOST_USER=`... (обязательное поле)
  - `EMAIL_HOST_PASSWORD=`... (обязательное поле)
  
- Секретный ключ
  - `SECRET_KEY=`... (обязательное поле)


Запускаем проект на компьютере

```
python manage.py runserver
```

Запускаем проект в docker (но для этого обязательно укажите в вашем env-файле: **POSTGRES_HOST=db**)

```
docker-compose up
```


### Несколько скринов проекта

![image](https://user-images.githubusercontent.com/75569467/147512641-a24ddbb9-4d6b-40d1-a9cf-0db48d2f2805.png)


![image](https://user-images.githubusercontent.com/75569467/147512658-8fdb1ee3-e1be-497c-9890-05df8209678d.png)


![image](https://user-images.githubusercontent.com/75569467/147512683-58ada14d-8a84-4c04-bdf3-b30188268432.png)


![image](https://user-images.githubusercontent.com/75569467/147512741-74be2fb9-0f87-437e-8e4d-c3c94c2a0ddc.png)


![image](https://user-images.githubusercontent.com/75569467/147512692-907d4139-115d-4d7e-a259-b83350fb6d98.png)

Приятного использования:)

---
