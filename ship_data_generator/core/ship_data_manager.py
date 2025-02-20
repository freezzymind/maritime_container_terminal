from ship_data_generator import Automatically, Manually

answer = input('выберите 1 если хотите ввести данные вручную или 2 если хотите автоматически сгенерировать данные.')

if answer == '1':
    ship = Manually()
elif answer == '2':
    ship = Automatically()
else:
    print('соси писюн')


if __name__ == "__main__":
    print(ship.get_params())