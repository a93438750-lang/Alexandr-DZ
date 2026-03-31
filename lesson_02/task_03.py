def is_year_leap(year):
    return year % 4 == 0
result = is_year_leap(2024)
print(f"{2024}: {result}")