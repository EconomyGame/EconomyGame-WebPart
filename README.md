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
| users | list | Список игроков, находящихся в игровой сессии |
| factories | list | Список фабрик, расположенных на карте |
| cities | list | Список городов, расположенных на карте |
| sources | list | Список источников с ресурсам |
| datetime | str | Дата и время начала игры по UTC (ISO 8601) |

## Структура объекта User
| Имя | Тип | Описание |
| --- |-----|----------|
| session_token | str | Уникальный токен пользователя в текущей сессии, по которому происходит API и Socket общение |
| is_ready | bool | Флаг, показывающий, готов ли игрок к старту матча |
| balance | float | Игровой баланс пользователя |
| profit_per_sec | float | Delta, на которую изменяется баланса игрока за 1 секунду |
| datetime | str | Время последнего обновления информации по пользователю в UTC (ISO 8601) |

## Структура объекта Factory
| Имя | Тип | Описание |
| --- |-----|----------|
| session_token | str | token игрока, который владеет текущей фабрикой  |
| resource_id | int | ID ресурса, в диапазоне [1, 4] |
| coords | tuple, ints | Координаты расположения фабрики |
| city_name | str | Название города, на который сфокусирована фабрика |
| source_coords | tuple, ints | Координаты, откуда добывается руда |
| level | int | Уровень прокачки завода |
| coef | float | Коэффициент КПД завода |
| datetime | str | Время последнего обновления информации по фабрике в UTC (ISO 8601) |

## Структура объекта City
| Имя | Тип | Описание |
| --- |-----|----------|
| name | str | Название города |
| coords | tuple, ints | Координаты расположения города |
| resource_levels | dict | Уровни прокачки ресурсов, в диапазоне [1, 4] |
| resource_stage | dict | Уровни прокачки ресурсов, в диапазоне [0, level_max] |
| resource_delta | float | Delta, на которую изменяется уровень за 1 секунду |
| datetime | str | Время последнего обновления информации по городу в UTC (ISO 8601) |

## Структура объекта Source
| Имя | Тип | Описание |
| --- |-----|----------|
| resource_id | int | ID ресурса, в диапазоне [1, 4]  |
| coords | tuple, ints | Координаты расположения источников |
| remain | float | Остатки ресурса в источнике |
| delta | float | Delta, на которую изменяется ресурс источника за 1 секунду |
| datetime | str | Время последнего обновления информации по источнику в UTC (ISO 8601) |

**Game WEB Api** by *[sevadp](https://github.com/sevadp)*
