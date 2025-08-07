from aiogram.types import (InlineKeyboardButton, 
                           InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder

main_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="👤 Профиль", callback_data="status"),
        InlineKeyboardButton(text="💼 Тарифы", callback_data="tariffs"),
        
    ],
    [
        InlineKeyboardButton(text="✨ Void", callback_data="about"),
        InlineKeyboardButton(text="🛠️ Поддержка", callback_data="support")
    ],
    [
        InlineKeyboardButton(text="Как подключится? 🔗", callback_data="connect")
    ]
]
)


main_for_infinity_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Профиль", callback_data="status"),
        
    ]
]
)



status_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="↩️ Назад", callback_data="back")
    ]
]
)

back = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="↩️ Назад", callback_data="back"),    
    ]
    
]
)

pay_1M = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="ЮKassa | 259 руб", callback_data="pay_yookassa_31"),    
    ],
    [
        InlineKeyboardButton(text="Telegram Stars | 150 ⭐️", callback_data="pay_stars_1M"),    
    ],
    [
        InlineKeyboardButton(text="↩️ Назад", callback_data="tariffs"),    
    ]
]
)

pay_3M = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="ЮKassa | 589 руб ", callback_data="pay_yookassa_93"),    
    ],
    [
        InlineKeyboardButton(text="Telegram Stars | 350 ⭐️", callback_data="pay_stars_3M"),    
    ],
    [
        InlineKeyboardButton(text="↩️ Назад", callback_data="tariffs"),    
    ]
]
)
pay_6M = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="ЮKassa | 839 руб", callback_data="pay_yookassa_186"),    
    ],
    [
        InlineKeyboardButton(text="Telegram Stars | 500 ⭐️", callback_data="pay_stars_6M"),    
    ],
    [
        InlineKeyboardButton(text="↩️ Назад", callback_data="tariffs"),    
    ]
]
)

pay_1Y = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="ЮKassa | 1249 руб", callback_data="pay_yookassa_372"),    
    ],
    [
        InlineKeyboardButton(text="Telegram Stars | 750 ⭐️", callback_data="pay_stars_1Y"),    
    ],
    [
        InlineKeyboardButton(text="↩️ Назад", callback_data="tariffs"),    
    ]
]
)


tariffs_kb_used = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="1 месяц - 256 руб | 150 ⭐️", callback_data="choice_tarif_1M"),    
    ],
    [
        InlineKeyboardButton(text="3 месяца - 589 руб | 350 ⭐️", callback_data="choice_tarif_3M"),    
    ],
    [
        InlineKeyboardButton(text="6 месяцев - 839 руб | 500 ⭐️", callback_data="choice_tarif_6M"),    
    ],
    [
        InlineKeyboardButton(text="1 год - 1249 руб | 750 ⭐️", callback_data="choice_tarif_1Y"),    
    ],
    [
        InlineKeyboardButton(text="↩️ Назад", callback_data="back")
    ]
]
)
tariffs_kb_not_used = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="7 дней бесплатно 🎁", callback_data="choice_tarif_Trial"),    
    ],
    [
        InlineKeyboardButton(text="1 месяц - 256 руб | 150 ⭐️", callback_data="choice_tarif_1M"),    
    ],
    [
        InlineKeyboardButton(text="3 месяца - 589 руб | 350 ⭐️", callback_data="choice_tarif_3M"),    
    ],
    [
        InlineKeyboardButton(text="6 месяцев - 839 руб | 500 ⭐️", callback_data="choice_tarif_6M"),    
    ],
    [
        InlineKeyboardButton(text="1 год - 1249 руб | 750 ⭐️", callback_data="choice_tarif_1Y"),    
    ],
    [
        InlineKeyboardButton(text="↩️ Назад", callback_data="back")
    ]
]
)
about_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="📰 Новостной канал Void VPN", url="https://journal.tinkoff.ru/telegram-stars/"),    # Заглушка
    ],
    [
        InlineKeyboardButton(text="↩️ Назад", callback_data="back")
    ]
]
)
support_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🛠️ Поддержка Void VPN", url="https://journal.tinkoff.ru/telegram-stars/"),    # Заглушка
    ],
    [
        InlineKeyboardButton(text="↩️ Назад", callback_data="back")
    ]
]
)
connect_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="📕 Руководство по подключению", url="https://journal.tinkoff.ru/telegram-stars/"),    # Заглушка
    ],
    [
        InlineKeyboardButton(text="↩️ Назад", callback_data="back")
    ]
]
)

stars_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Про Telegram Stars", url="https://journal.tinkoff.ru/telegram-stars/")   
    ],
    [
        InlineKeyboardButton(text="Premium bot", url="tg://resolve?domain=PremiumBot")
    ]
]

)
