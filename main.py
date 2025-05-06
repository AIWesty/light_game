from abc import ABC, abstractmethod


class GameEntity(ABC): #простой абстрактный метода для реализации полиморфизма
    @abstractmethod
    def get_info(self):
        pass


class Character(GameEntity): #обычный класс персонажа
    def __init__(self, name, health, damage, weapon):
        self.name = name
        self._health = health
        self._damage = damage 
        self._weapon = weapon

    def get_info(self):
        return f"{self.name}: {self._health} HP"

    #геттеры и сеттеры для приватных атрибутов
    @property
    def damage(self): 
        return self._damage


    @property
    def health(self):  
        return self._health
    

    @health.setter 
    def health(self, value): 
        if not isinstance(value, (float, int)):
            raise ValueError("Значение здоровья может принимать только числовое значение")
        self._health = value
        

    def display_info(self):
        return f'name - {self.name}, health {self.name} - {self._health}'

    #атака
    def attack(self, other_char):
        if not isinstance(other_char, Character):
            raise ValueError('Можно атаковать только другого героя')
        damage_dealt = self._damage
        other_char._health -= damage_dealt
        return (f'{self.name} наносит урон: {damage_dealt} игроку {other_char.name}, '
                f'здоровье игрока {other_char.name} - {other_char._health}')


class NPC:
    def __init__(self, name):
        self.name = name  

    def speak(self):
        return f'Привет, я NPC, мое имя - {self.name}'


class Trading:
    def trade(self):  
        return 'происходит сделка'

 
class Merchant(NPC, Trading): #классы для множественного наследования
    pass


class Warrior(Character): #различные персонажи
    def __init__(self, name, health, damage, weapon):
        super().__init__(name, health, damage, weapon)

    def get_info(self):
        return f"{super().get_info()} (оружие: {self._weapon})"

    def attack(self, other_char):
        base_attack = super().attack(other_char)
        return base_attack.replace("наносит урон", "наносит урон с помощью меча")


class Mage(Character):
    def __init__(self, name, health, weapon):
        super().__init__(name, health, damage=10, weapon=weapon)

    def get_info(self):
        return f"{super().get_info()} (оружие: {self._weapon})"

    def attack(self, other_char):
        base_attack = super().attack(other_char)
        return base_attack.replace("наносит урон", "наносит магический урон")


class Archer(Character, Trading):
    def __init__(self, name, health, damage, weapon):
        super().__init__(name, health, damage, weapon)

    def shoot(self):
        return f"{self.name} стреляет из {self._weapon}!"

    def trade(self):
        trade_result = super().trade()
        print(f"Лучник {self.name} готов торговать")
        return trade_result


class Inventory(dict):
    def add_item(self, item, quantity=1):
        if self.validate_item_quantity(item, quantity):
            if item in self:
                self[item] += quantity
            else:
                self[item] = quantity
            print(f"Добавлено: {item} x{quantity}")

    def delete_item(self, item, quantity=1):
        if self.validate_item_quantity(item, quantity):
            if item not in self:
                raise KeyError('Такого предмета нет в инвентаре')
            self[item] -= quantity
            if self[item] == 0:
                del self[item]
            print(f"Удалено: {item} x{quantity}")

    @staticmethod
    def validate_item_quantity(item, quantity):
        if not isinstance(item, str) or not isinstance(quantity, (int, float)):
            raise ValueError('Предмет может быть только строкой, а количество только числом')
        return True


# Пример работы
if __name__ == "__main__":
    warrior = Warrior("Арагорн", 120, 20, "меч")
    mage = Mage("Гэндальф", 80, "посох")  # Убрал лишний параметр damage
    
    characters = [warrior, mage]
    
    for character in characters:
        print(character.get_info())
    
    print(warrior.attack(mage))
    print(mage.attack(warrior))
    
    merchant = Merchant("Торговец Боб")
    print(merchant.speak())
    print(merchant.trade())
    
    archer = Archer("Леголас", 100, 15, "лук")
    print(archer.shoot())
    print(archer.trade())
    
    inventory = Inventory()
    inventory.add_item("стрела", 10)
    inventory.add_item("золото", 50)
    inventory.delete_item("стрела", 5)