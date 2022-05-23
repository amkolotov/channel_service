Ссылка на google sheet: https://docs.google.com/spreadsheets/d/1gbigMD3e6D7z79kMZ1ajSq8geM3vRw1f1D_QVyS8aq4/edit#gid=645828047

Запуск скрипта
- для запуска скрипта необходимо зайти в папку channel_script.
- для получения сообщений в телеграмм необходимо связаться с телекгрмм ботом @channels_service_test,
затем прейти по адресу https://api.telegram.org/bot5320735825:AAF5g6KKBRU2iG8I3a4ioVh8fKTMKrjk8UE/getUpdates,
скопировать id from и заменить его в CHAT_ID файла .env.
- запустить команду 'docker-compose build', затем 'docker-compose up'.

Запуск приложения Django REST framework, Vue.js
- для запуска приложения необходимо из корневой папки запустить 'docker-compose build', затем 'docker-compose up'
и перейти по адресу http://localhost:3000, api доступно по адресу http://localhost:8000/api/v1.
