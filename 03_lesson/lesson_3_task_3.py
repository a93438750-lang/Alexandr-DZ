from address import Address
from mailing import Mailing
 
from_addr = Address("123456", "Смоленск", "Мира", "12", "114") 

to_addr = Address("345764", "Кострома", "Советская", "12", "120")

mailing = Mailing(
    to_address=to_addr,
     from_address=from_addr,
      cost=300,
       track="RU123498765" 
)
print(f"Отправление {mailing.track} из {mailing.from_address.index}, "
      f"{mailing.from_address.city}, {mailing.from_address.street}, "
      f"{mailing.from_address.house} - {mailing.from_address.apartment} "
      f"в {mailing.to_address.index}, {mailing.to_address.city}, "
      f"{mailing.to_address.street}, {mailing.to_address.house} -"
      f"{mailing.to_address.apartment}. Стоимость {mailing.cost} рублей.")