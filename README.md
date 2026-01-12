# Telegram Avatar Color Inspector

Небольшая утилита на PyQt5 для проверки цвета аватарки по Telegram ID в разных клиентах:

- **Telegram Desktop**
- **Telegram X (Android)**
- **Telegram iOS**
- **Telegram macOS (native)**

Цвет считается по `peer_id % 7` 
## Установка

У тебя уже есть `requirements.txt` с `PyQt5`, так что достаточно:

```bash
pip install -r requirements.txt
```

## Запуск

```bash
python 1.py
```

## Как пользоваться

1. Запусти приложение.
2. В выпадающем списке **Клиент** выбери нужный клиент (Desktop / TGX / iOS / macOS).
3. В поле снизу введи Telegram ID построчно.
4. Нажми:
   - **«Фильтр по выбранному цвету»** — сначала кликни по цвету в палитре, потом увидишь только ID с этим цветом.
   - **«Показать цвета для ID (во всех клиентах)»** — покажет строку вида  
     `123456789: TDesktop=Red, TGX=Red, iOS=Orange, macOS=Orange`.

Этого достаточно, чтобы быстро смотреть, какой цвет аватарки будет у любого ID в разных клиентах.
