# ZASTAVA

  ### *Доброго времени суток!* **Вашему вниманию** представляется сервис "**Zastava**".

# Требования к эксплуатации
**Для запуска приложения представлены следующие требования:**
1) *PostgreSQL => 14.0*;
2) *Python = 3.8.5*;
3) *Библиотеки из req.txt (для работы модулей анализа и fastAPI)*;
4) *NodeJS

# Способы запуска проекта
#### Виртуальное окружение

Откройте терминал в корне проекта, выполните команды:
```python
python -m venv venv

\venv\Scripts\activate

cd fastapi

pip install -r requirments.txt
```
#### FastAPI

В папке **fastapi**, выполнить:

`uvicorn main:app --reload`

После того как вы запустите свою БД, выполнив команду выше будут подняты инстансы fastApi и PostgreSQL. Далее необходимо запустить клиентскую часть приложения


#### Frontend
В папке `frontend`:

Откройте терминал в папке `frontend`, выполните команды:

`npm install`

`npm run serve`

После этого frontend-часть этого проекта будет доступна на *http://localhost:8080/*.

#### Стэк технологий:

FastAPI, VueJS, PostgreSQL, face_recognition, Yamnet_realtime, Roboflow.


