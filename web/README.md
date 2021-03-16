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

## Структура объекта User
| Имя | Тип | Описание |
| --- |-----|----------|
| session_token | token | Уникальный токен пользователя в текущей сессии, по которому происходит API и Socket общение |
| is_ready | bool | Флаг, показывающий, готов ли игрок к старту матча |
| balance | int | Игровой баланс пользователя |
| profit_per_sec | int | Delta, на которую изменяется баланса игрока за 1 секунду |
| datetime | str | Время последнего обновления информации по пользователю в UTC (ISO 8601) |

**Game WEB Api** by *[sevadp](https://github.com/sevadp)*
