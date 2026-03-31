def month_to_season(month):
    if month in (1, 2, 12):
        return"зима"
    if month in (3, 4, 5):
        return"Весна"
    if month in (6, 7,8):
        return"Лето"
    if month in (9, 10, 11):
        return"Осень"
print(month_to_season(2))