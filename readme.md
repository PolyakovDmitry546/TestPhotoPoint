## Задача
Предлагаем вам создать "голый" джанго проект,
который по переходу на страницу /get-current-usd/ бужет отображать в json формате
актуальный курс доллара к рублю (запрос по апи, найти самостоятельно) и 
показывать 10 последних запросов (паузу между запросами курсов должна быть не менее 10 секунд)

## Реализовано

В папке exchange_rates_providers/openexchangerates реализованы методы получения курса USDRUB через API сайта https://openexchangerates.org

В папке exchange_rates ноходится вьюшка для метода
/get-current-usd/ и сервис с логикой получения курса валют.

Пауза между запросами к внешнему API задается в праметре EXCHANGE_RATE_REQUEST_INTERVAL в переменных окружения.

В папке tests находятся тесты на весь реализованный функционал.

## Запуск проекта

```bash
git clone https://github.com/PolyakovDmitry546/TestPhotoPoint.git
cd TestPhotoPoint
```
Добавить файл с переменными окружения .env в папку проекта, использовать в качестве примера .env.example. 
В параметре OPENEXCHANGERATES_APP_ID необходимо записать идентификатор приложения полученный с сайта https://openexchangerates.org

### Используя докер

```bash
docker build -t test_photo_point .
docker run -p 8000:8000 test_photo_point
```

### Используя локальное окружение
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt 
python .\src\manage.py migrate
python .\src\manage.py runserver
```