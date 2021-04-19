# Game WEB Api
<img src="https://raw.githubusercontent.com/swagger-api/swagger.io/wordpress/images/assets/SWU-logo-clr.png" height="50">

Обслуживание и поддержка сетевой игры

[![View in Swagger](http://jessemillar.github.io/view-in-swagger-button/button.svg)](http://tp-project2021.herokuapp.com/api/v1/docs/)

## Config: headers
| Имя | Тип | Описание |
| --- |-----|----------|
| cities | dict | Конфигурация городов |
| count_cities | int | Количество городов на карте |
| count_users | int | Количество игроков на карте |
| factories | dict | Конфигурация фабрик |
| map | dict | Положение объектов на карте |
| resource_ids | dict | Описание ресурсов |
| size_map | list | Размер карты |
| transfer_price | int | Стоимость трансфера за 1 клетку |

## Config: cities
| Имя | Тип | Описание |
| --- |-----|----------|
| cities_names | list | Дефолтные названия городов |
| city_payout | int | Выплата города за ед. доставленного ресурса |
| rates_dif | int | Коэфицент разницы для товаров разного качества |
| requied_levels | dict | Минимальная необходимая поставка городу |
| upgrades_levels | dict | Кол-во необходимых ресурсов для повышения level |

## Config: factories
| Имя | Тип | Описание |
| --- |-----|----------|
| coef_levelup | list, ints | Кол-во секунд, необходимых чтобы довести коэфицент до 1. Формула: (1-start_coef) / coef_levelup[level] - в сек. |
| factory_levels | dict, ints | Стоимость апгрейда фабрики. Формула: factory_levels[level] / coef |
| max_products | dict, ints | Кол-во продукции, которую требует и поставляет завод. |
| price_factory | int | Стоимость фабрики |
| start_coef | float | Дефолтное значение coef |

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
| username | str | Ник игрока |
| session_token | str | Уникальный токен пользователя в текущей сессии, по которому происходит API и Socket общение |
| is_ready | bool | Флаг, показывающий, готов ли игрок к старту матча |
| balance | float | Игровой баланс пользователя |
| profit_per_sec | float | Delta, на которую изменяется баланса игрока за 1 секунду |
| datetime | str | Время последнего обновления информации по пользователю в UTC (ISO 8601) |

## Структура объекта Factory
| Имя | Тип | Описание |
| --- |-----|----------|
| _id | str | ID объекта  |
| username | str | Ник игрока, который владеет текущей фабрикой  |
| resource_id | int | ID ресурса, в диапазоне [1, 4] |
| coords | tuple, ints | Координаты расположения фабрики |
| city_id | str | ID города, на который сфокусирована фабрика |
| source_id | tuple, ints | ID ресурса, откуда добывается руда |
| level | int | Уровень прокачки завода |
| coef | float | Коэффициент отработки завода, множитель стоимости апгрейда |
| delta_coef | float | Изменение коэф. в секунду |
| datetime | str | Время последнего обновления информации по фабрике в UTC (ISO 8601) |

## Структура объекта City
| Имя | Тип | Описание |
| --- |-----|----------|
| _id | str | ID объекта  |
| name | str | Название города |
| coords | tuple, ints | Координаты расположения города |
| resource_levels | dict | Уровни прокачки ресурсов, в диапазоне [1, 4] |
| resource_stage | dict | Уровни прокачки ресурсов, в диапазоне [0, level_max] |
| resource_delta | float | Delta, на которую изменяется уровень за 1 секунду |
| datetime | str | Время последнего обновления информации по городу в UTC (ISO 8601) |

## Структура объекта Source
| Имя | Тип | Описание |
| --- |-----|----------|
| _id | str | ID объекта  |
| resource_id | int | ID ресурса, в диапазоне [1, 4]  |
| coords | tuple, ints | Координаты расположения источников |
| remain | float | Остатки ресурса в источнике |
| delta | float | Delta, на которую изменяется ресурс источника за 1 секунду |
| datetime | str | Время последнего обновления информации по источнику в UTC (ISO 8601) |

**Game WEB Api** by *[sevadp](https://github.com/sevadp)*
