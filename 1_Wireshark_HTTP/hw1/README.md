# Практика 1. Wireshark: HTTP (сдать до 23.02.2022) 

## [Файл с описанием лабораторной работы](./HoweWork1.pdf)

## Задание 1. Базовое взаимодействие HTTP GET/response (2 балла) 

![](./images/1_request.png)
1. Мой браузер и сервер пользуется HTTP 1.1
2. Доступные языки моего браузера RU, ENG 
Доступные браузеры на моём устройстве(?), доступные кодировки.
3. Мой `ip=192.168.0.157`, gaia.cs.umass.edu `ip=128.119.245.12`
4. На основной запрос `200` (OK), но потом сайт нас отправляет за иконкой, которая, видимо, переехала и возращает `404` (Not Found)

![](./images/1_response.png)

5. Last-Modified: Sun, 19 Feb 2023 06:59:01 GMT
6. Content-Length: 128\r\n


## Задание 2. HTTP CONDITIONAL GET/response (2 балла) 
![](./images/2_req1.png)

1. Поле `If-Modified-Since` отсутствует.  
2. Первый GET вернул полный файл, убедиться можно по `[Content length: 371]`

![](./images/2_req2.png)

3. Да, есть поле и время последнего изменения этого файла на сервере. `[If-Modified-Since: Sun, 19 Feb 2023 06:59:01 GMT]`
4. На повторный запрос сервер вернул код `304 (Not Modified)` - скачанный нами файл лежит в кеше и не требует повторного скачивания т.к. не изменился. И ещё раз убедиться можно не найди поля `Content length`

## Задание 3. Получение длинных документов (2 балла)

![](./images/3_req.png)

1. Мой браузер отправил 1 HTTP запрос. `No. = 35` 
2. Код ответа `200 OK`, `No.=44`

![](./images/3_resp_segments.png)

3.  Как видно для передачи файла потребовалось 3 сегмента (3 tcp "пакета"). Можно заменить, что сам контент весить 4500 байт, а передавалось на tcp уровне 4861 байт

4. Насколько я понимаю нет. (Я не нашёл, да и странно говорить, высокому уровню что делать  низкому) (?)

## Задание 4. HTML-документы со встроенными объектами (2 балла) 

![](./images/4_http_get.png)

1. 3 HTTP GET запроса (Основной + 2 картинки). 
    * <http://gaia.cs.umass.edu/GET/pearson.png>
    * <http://kurose.cslash.net/8E_cover_small.jpg> 
2. Изображения загружались параллельно, можно заметить, например, что GET 1 картинки имеет номер *24*, а ответ на него *46*. А для  GET 2 картики имеет номер *36*, а ответ *42*. При последовательной загрузки сначала скачался бы один файл, а другой бы ждал окончания, чего мы не видими здесь. (Общий комментарий был дан на лекции - интернет подефолту работает асинхронно)

## Задание 5. HTTP-аутентификация (2 балла)

![](./images/5_authorization.png)

1. На первый запрос сервер выдал код `401 Unauthorized`

2. На второй запрос сервер выдал код `200 OK`.
Во втором GET запросе появилось поле: <br>
`[Authorization: Basic d2lyZXNoYXJrLXN0dWRlbnRzOm5ldHdvcms=\r\n]` <br>
`[Credentials: wireshark-students:network]` <br>
Как мы видим, введённый нами, логин и пароль по HTTP передаётся в открытом ввиде

