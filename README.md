# Тестовое задание.

Описание задания в файле [task.md](task.md).

Пример входного файла [example.xlsx](example.xlsx).

## Комментарий к запуску

Проект упакован в docker и автоматизирован с помощью docker compose.

При необходимости изменить имя бд, пользователя или пароль внесите изменения в файл vars.env

Проект выполнен с использованием FastAPI, документация(SwaggerUI) находится по роуту `/docs`

Для запуска : выполните  `docker compose up --build -d`

