from smartphone import Smartphone

catalog = []

catalog.append(Smartphone("Apple", "iphone 17", "+79123456789"))
catalog.append(Smartphone("Samsung", "Galaxy", "+79234567890"))
catalog.append(Smartphone("Google", "Pixel", "+79098765432"))
catalog.append(Smartphone("Infinix", "12 Play", "+79354672190"))
catalog.append(Smartphone("Honer", "10 XP", "+79285904553"))

for smartphone in catalog:
    print(f"{smartphone.brand,} - {smartphone.model}. {smartphone.phone_number}")
