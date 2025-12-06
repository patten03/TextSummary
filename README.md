# Описание программы
TextSummary - это API-сервис на FastAPI для суммаризации длинных текстов через LLM gemma3 при помощи LLM-сервиса Ollama и с сохранением истории запросов в PostgreSQL.
# Инструкция по сборке
## Зависимости
- Docker version 29.0.0
- NVIDIA Container Toolkit CLI version 1.18.0
- Python не требуется, он 

## Процесс сборки
Для начала создайте папки в директории TextSummary для сервиса Ollama и базы данных PostgreSQL
```
mkdir ollama
```
```
mkdir pgdata
```
Соберите контейнер с Ollama и загрузите туда gemma3
```
docker compose up -d ollama
```
```
docker exec -it ollama ollama pull gemma3
```
Создайте .env файл и запишите туда переменные для базы данных
```
touch .env
```
Пример данных:
```
POSTGRES_PASSWORD=admin123
POSTGRES_USER=admin123
POSTGRES_DB=summaries
```
Для запуска контейнеров и начала окончательной сборки введите:
```
docker compose up
```
