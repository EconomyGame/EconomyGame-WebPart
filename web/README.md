# Game WEB Api
<img src="https://raw.githubusercontent.com/swagger-api/swagger.io/wordpress/images/assets/SWU-logo-clr.png" height="50">

Обслуживание и поддержка сетевой игры

[![View in Swagger](http://jessemillar.github.io/view-in-swagger-button/button.svg)](http://tp-project2021.herokuapp.com/api/v1/docs/)

## Структура объекта Game
| Имя | Тип | Описание |
| --- |-----|----------|
| _id | id | ID игры, представленный в виде ObjectID класса |
| is_started | bool | Флаг, показывающий, началась ли игра |
| ref_code | str | Игровой код, по которому можно подключиться к сессии |
| users | dict | Список игроков, находящихся в игровой сессии |
| factories | dict | Список фабрик, расположенных на карте |
| cities | dict | Список городов, расположенных на карте |
| sources | dict | Список источников с ресурсам |
| datetime | str | Дата и время начала игры по UTC (ISO 8601) |

**Game WEB Api** by *[sevadp](https://github.com/sevadp)*
