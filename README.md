 #### Реализовать систему транзакций.
 * Она должна принимать запросы на ввод или вывод денег и заносить их в базу данных.
 * Также она должна отдавать данные по транзакции из бд при запросе инфы по какой-либо транзакции.

 #### Необходимо реализовать http api для внешних потребителей, которые и будут создавать транзакции и просить информацию о них.
 Оцениваться он будет по удобству, понятности, предсказуемости и прочим вещам, которые мы все любим.

* Система должна быть доступной и отказоустойчивой, способной жить под высокой нагрузкой
запросы на создание транзакций должны всегда выполнятся рано или поздно,
то есть если что-то в сервисе упадёт из-за какого-либо nil pointerа, клиенты не должны терять
способность создавать заявки на создание транзакций.
* Ваше решение будет оцениваться по критериям понятности и поддерживаемости - гипотетические
члены вашей команды не должны тратить лишнее время на расшифровку вашего замысла,
исследуя вашу архитектуру или читая ваш код.
* Необходимо использовать postgresql в качестве бд.

 Плюсом будет openapi описание вашего публичного api.
 Также плюсом будет простой compose-файл для всей инфы

#### Инструкция для запуска:
* заполнить данными файл config.ini
* скачать зависимости `pip install -r requirements.txt` затем активировать их
* в консоли `uvicorn main:app --reload`