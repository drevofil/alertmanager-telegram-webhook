# Интеграция Alertmanager и телеграм канала с настроенными темами.

## Универсальная сборка

```shell
./build.sh Dockerfile.ubi9 brrra/telegram:1.7-ubi9
```

### В Buildah

```shell
buildah bud -f Dockerfile.ubi9 -t brrra/telegram:1.7-ubi9
```

### В Docker

```shell
docker build -f Dockerfile.bullseye . -t brrra/telegram:1.7-bullseye
```

## Запуск

1. `appkey` - ключ приложения python (рандомная строка)
2. `username` - логин базовой авторизации для отправки алертов 
3. `password`- пароль базовой авторизации для отправки алертов 
4. `chatid` - чат (канал, группа), в который отправляются уведомления
5. `bot_token`- токен бота
6. `show_labels` - default - `true`, опциональная переменная для отключения отправки label алертов в сообщение

```shell
podman run \
-p 9119:9119 \
-e appkey=1123123 \
-e username=212312 \
-e password=3312321 \
-e chatid=1312321 \
-e bot_token=1123123 \
-e show_labels=false \
--name alertmanager-telegram-webhook \
brrra/telegram:1.7 
```

#### В Docker

```shell
docker run \
-p 9119:9119 \
-e appkey=1123123 \
-e username=212312 \
-e password=3312321 \
-e chatid=1312321 \
-e bot_token=1123123 \
-e show_labels=false \
--name alertmanager-telegram-webhook \
brrra/telegram:1.7 
```


## Использование

### Оправка в тему чата

Для отправки в тему чата телеграм используется параметр `?channel=число` в URL.

### Логгирование

Для изменения уровня логирования, передать переменную `loglevel` с одним из следующих значений `debug`,`info`,`warning`,`error`,`critical`.

### Проверка работы (без базовой авторизации)

```shell
curl -XPOST --data '{"status":"resolved","groupLabels":{"alertname":"instance_down"},"commonAnnotations":{"description":"i-0d7188fkl90bac100 of job ec2-sp-node_exporter has been down for more than 2 minutes.","summary":"Instance i-0d7188fkl90bac100 down"},"alerts":[{"status":"resolved","labels":{"name":"olokinho01-prod","instance":"i-0d7188fkl90bac100","job":"ec2-sp-node_exporter","alertname":"instance_down","os":"linux","severity":"page"},"endsAt":"2019-07-01T16:16:19.376244942-03:00","generatorURL":"http://pmts.io:9090","startsAt":"2019-07-01T16:02:19.376245319-03:00","annotations":{"description":"i-0d7188fkl90bac100 of job ec2-sp-node_exporter has been down for more than 2 minutes.","summary":"Instance i-0d7188fkl90bac100 down"}}],"version":"4","receiver":"infra-alert","externalURL":"http://alm.io:9093","commonLabels":{"name":"olokinho01-prod","instance":"i-0d7188fkl90bac100","job":"ec2-sp-node_exporter","alertname":"instance_down","os":"linux","severity":"page"}}' http://localhost:9119/alert\?channel\=12
```
