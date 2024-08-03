Python backend developer test. 
API для сервиса хранения видеофайлов с возможностью менять разрешение.
В качестве фреймворка используется Django Rest. Для конвертации видео - ffmpeg-python (https://github.com/kkroening/ffmpeg-python)
```
curl -X POST http://localhost:8000/file/ -F "file.mp4"
```
Сохраняет файл в папку videos. Ответом возвращает id, UUID — идентификатор
```
curl -X PATCH http://localhost:8000/file/{id}/change_resolution/
 -H "Content-Type: application/json" -d "{\"width\": 120, \"height\": 120}"
```
Изменяет разрешение файла на width и height указанные в запросе. Возвращает индикатор того что обработка началась. Не того что она именно закончилась 
(success: Boolean)

```
curl -X GET http://localhost:8000/file/{id}/
 
```

Возвращает информацию о выбранном файле в следующем виде:
```
{
  id: uid,
  file: FileField, расположение файла
  filename: string,
  processing: Boolean - идёт ли процесс обработки
  processing_success: null | true | false  - отображает успешность последней операции над видео. Дефолтное значение null.
}
```
```
curl -X DELETE http://localhost:8000/file/{id}/
 
```
Удаляет файл, а также ассоциированный с ним обьект базы данных. возвращает  success: Boolean


