import random
from tkinter import *
from tkinter import messagebox


class TransportVehicle:
  def __init__(self, max_speed, pollution_level, noise_level, energy_source):
    self.max_speed = max_speed
    self.pollution_level = pollution_level
    self.noise_level = noise_level
    self.energy_source = energy_source
    self.current_speed = random.randint(1, max_speed)
    self.direction = None

  def setStartCords(self, streets): #Вызывается в самом начале для спавна транспорта
    key_street = random.choice(streets)  #Выбор улицы для спавна
    x = key_street.getX() #Получение координат от улицы
    y = key_street.getY()
    self.vector = key_street.vector
    if self.vector == 'h':
      x = random.choice([1, 75])
      self.x = x
      self.y = y
      if x == 1:
        self.direction = 1
      else:
        self.direction = -1
    else:
      y = random.choice([1, 75])
      self.y = y
      self.x = x
      if y == 1:
        self.direction = 1
      else:
        self.direction = -1

  def speedControl(self, city):
    if self.energy_source == "Внешний":
      #ДОБАВИТЬ В СИТИ CПИСОК МАШИН НА КАЖДОЙ УЛИЦЕ
      for car in city.get_cars_on_street(self.getCurStreetName()):
        if (car != self) and car.getDirection() == self.getDirection(): 
          self.current_speed = car.current_speed
        else:
          self.current_speed += random.randint(-3, 3)
    else:
      self.current_speed += random.randint(-3, 3)

    if self.current_speed > self.max_speed:
      self.current_speed = self.max_speed

    if self.current_speed < 2:
      self.current_speed = 3
    
  def setTransportCurPosition(self, streets, intersections):
    if self.getX() < 1 or self.getX() > 800 or self.getY() < 1 or self.getY() > 800:
      self.position = "Вне города"
    else:
      for street in streets:
        if street.getVector() == 'v' and street.getX() == self.getX():
          self.curStreet = street
          self.vector = street.getVector()
          self.position = street.getName() #########
        if street.getVector() == 'h' and street.getY() == self.getY():
          self.curStreet = street
          self.vector = street.vector
          self.position = street.getName()
      for intersection in intersections:
        if intersection.getY() == self.getY() and intersection.getX() == self.getX():
          self.position = "Перекресток"

  def checkTransportCurPosition(self):
    if self.position == "Вне города":
      self.direction = (-1) * self.direction
      print(f"Выезд за город {self}")
    if self.position == "Перекресток":
      self.direction = random.choice([-1, 1])
      self.vector = random.choice(["h", "v"])


  def getCurStreetName(self):
    return self.curStreet.getName()

  def getX(self):
    return self.x

  def get_vehicle_type(self):
    return self.vehicle_type

  def getY(self):
    return self.y

  def get_transport_pollution_level(self):
    return self.pollution_level

  def getDirection(self):
    return self.direction

  def getVector(self):
    return self.vector

  def getPosition(self):
    return self.position

  def getEnergySource(self):
    return self.energy_source
  
  def changePosition(self, city):
    if self.vector == "h":
      for i in range(self.current_speed):
        self.x += self.direction
        self.setTransportCurPosition(city.getStreets(), city.getIntersections())
        if self.getPosition() == "Перекресток":
          self.checkTransportCurPosition()         #ВОЗМОЖНО МОЖНО ЗАМЕНИТЬ
          self.position = "Выезд с перекрестка"
          break
        if self.getPosition() == "Вне города":
          self.checkTransportCurPosition()
          break

    if self.vector == "v":
      for i in range(self.current_speed):
        self.y += self.direction
        self.setTransportCurPosition(city.getStreets(), city.getIntersections())
        if self.getPosition() == "Перекресток":
          self.checkTransportCurPosition()         #ВОЗМОЖНО МОЖНО ЗАМЕНИТЬ
          self.position = "Выезд с перекрестка"
          break
        if self.getPosition() == "Вне города":
          self.checkTransportCurPosition()
          break
    for street in city.getStreets():
      street.setCur_Vehicles(city.getTransports())
    print(f"КООРДИНАТЫ МАШИНЫ {self.get_vehicle_type()}: {self.position};  X:{self.getX()};  Y:{self.getY()}     СКОРОСТЬ: {self.current_speed}  НАПРАВЛЕНИЕ: {self.getDirection()}")

class PassengerVehicle(TransportVehicle):
  def __init__(self, max_speed, pollution_level, noise_level, energy_source, max_passengers):
    super().__init__(max_speed, pollution_level, noise_level, energy_source)
    self.vehicle_type = "Пассажирский"
    self.max_passengers = max_passengers
    self.current_passengers = random.randint(0, max_passengers)

  def getPassengers(self):
    return self.current_passengers

class CargoVehicle(TransportVehicle):
  def __init__(self, max_speed, pollution_level, noise_level, energy_source, max_cargo_weight):
    super().__init__(max_speed, pollution_level, noise_level, energy_source)
    self.vehicle_type = "Грузовой"
    self.max_cargo_weight = max_cargo_weight
    self.current_cargo_weight = random.randint(0, max_cargo_weight)

  def getWeight(self):
    return self.current_cargo_weight

class Street:
  def __init__(self, name, x, y):
    self.y = y
    self.x = x
    self.name = name
    if self.y != None:
      self.vector = 'h'
    else:
      self.vector = 'v'

  def getPassengersAmount(self):
    value = 0
    for car in self.getCur_Vehicles():
      if car.vehicle_type == "Пассажирский":
        value = value + car.getPassengers()
    return value

  def getWeightAmount(self):
    value = 0
    for car in self.getCur_Vehicles():
      if car.vehicle_type == "Грузовой":
        value = value + car.getWeight()
    return value
  
  def setCur_Vehicles(self, vehicles):
    #Добавление машин на улицу
    self.cur_vehicles = []
    for car in vehicles:
      if car.getCurStreetName() == self.getName():
        self.cur_vehicles.append(car)

  def getVector(self):
    return self.vector

  def getCur_Vehicles(self):
    return self.cur_vehicles

  def getName(self):
    return self.name

  def getX(self):
    return self.x

  def getY(self):
    return self.y

class Intersection:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def getY(self):
    return self.y

  def getX(self):
    return self.x


class City:
  def __init__(self, streets, intersections, transports, x, y):
    self.x = x
    self.y = y
    self.streets = streets
    self.intersections = intersections
    self.transports = transports
    self.cars_on_streets = dict()


  def getStreets(self):
    return self.streets

  def getIntersections(self):
    return self.intersections

  def getTransports(self):
    return self.transports

  def set_cars_on_streets(self):
    for street in self.streets:
      self.cars_on_streets[street.getName()] = street.getCur_Vehicles()

  def get_cars_on_street(self, street_name):
    return self.cars_on_streets[street_name]

  def show_car_info_canvas(self, event):
    for car in self.transports:
        if ((car.getX() == event.x - 5) or (car.getX() == event.x + 5)) or ((car.getY() == event.y + 5) or (car.getY() == event.y - 5)):
            messagebox.showinfo('Данные о машине', f"Координаты машины: ({car.getX()}, {car.getY()}).\nСкорость: {car.current_speed}\n Источник питания: {car.energy_source}\n Тип машины: {car.vehicle_type}\n Максимальная скорость: {car.max_speed}\n Уровень шума: {car.noise_level}\n Уровень загрязнения: {car.pollution_level}")

  def set_vehicles_canvas(self):
    cars = []
    canvas.delete('car')
    for car in self.transports:
      cars.append(canvas.create_rectangle(car.getX() - 5, car.getY() - 5, car.getX() + 5, car.getY() + 5, fill='red', tag='car'))
      print('Создание рисунка тачки')
    for carr in cars:
      canvas.tag_bind(carr, '<Enter>', self.show_car_info_canvas)
      print('Привязка команд для тачки')
      canvas.pack()

  def show_street_info_canvas(self, event):
    for street in self.streets:
      if street.getX() == event.x:
        messagebox.showinfo('Данные об улице', f'Название улицы: {street.getName()}')
      elif street.getY() == event.y:
        messagebox.showinfo('Данные об улице', f'Название улицы: {street.getName()}')
  
  def simulate_all(self):
    self.set_cars_on_streets()
    print(self.cars_on_streets)
    for car in cars:
      car.speedControl(self)
      car.changePosition(self)
    #messagebox.showinfo('Текущий момент в городе')
    self.set_vehicles_canvas()
  
  def get_abs_pollution_level(self):
    x = int(x_tf.get())
    y = int(y_tf.get())
    pollution = 0
    for street in self.streets:
      if x == street.getX():
        for car in street.getCur_Vehicles():
          if car.getY() == y:
            pollution += car.get_transport_pollution_level()
      if y == street.getY():
        for car in street.getCur_Vehicles():
          if car.getX() == x:
            pollution += car.get_transport_pollution_level()
    messagebox.showinfo('Уровень загрязнения в точке', f"В точке ({x}, {y}) уровень загрязнения составляет {pollution} г/м")
  

  def get_abs_noise_level(self):
    x = int(x_tf.get())
    y = int(y_tf.get())
    noise = 0
    for street in self.streets:
      if x == street.getX():
        for car in street.getCur_Vehicles():
          noise += 1 / abs(y - car.getY())
      if y == street.getY():
        for car in street.getCur_Vehicles():
          noise += 1 / abs(x - car.getX())
    messagebox.showinfo('Уровень шума в точке', f"В точке ({x}, {y}) уровень шума составляет {noise} децибел")


  def get_passengers_on_street(self):
    searched_street = (street_name.get())
    cnt_pas = 0
    for street in self.streets:
      if street.getName() == searched_street:
        cnt_pas = street.getPassengersAmount()
    messagebox.showinfo('Количество пассажиров', f'На {searched_street} {cnt_pas} пассажиров')

  def get_weight_on_street(self):
    searched_street = (street_name.get())
    cnt_pas = 0
    for street in self.streets:
      if street.getName() == searched_street:
        cnt_pas = street.getWeightAmount()
    messagebox.showinfo('Вес груза', f'На {searched_street} {cnt_pas} кг груза')  

  def getCargoTransportAmount(self):
    valu = 0
    for car in self.getTransports():
      if car.get_vehicle_type() == 'Грузовой':
        valu = valu + 1
    messagebox.showinfo('Количество грузового транспорта', f'В городе {valu} грузовых средств')

  def getPassengerTransportAmount(self):
    valuee = 0
    for car in self.getTransports():
      if car.get_vehicle_type() == 'Пассажирский':
        valuee = valuee + 1
    messagebox.showinfo('Количество пассажирского транспорта', f'В городе {valuee} пассажирских средств') 

  def getExternalEnergySourceTransportAmount(self):
    valueee = 0
    for car in self.getTransports():
      if car.getEnergySource() == 'Внешний':
        valueee = valueee + 1
    messagebox.showinfo('Количество экологичного транспорта', f'В городе {valueee} экологичных средств')
  


street1 = Street("ул. Гоголя", 16, None)
street2 = Street("ул. Ленина", None, 45)
street3 = Street("ул. Сталина", None, 60)


car1 = PassengerVehicle(30, 10, 10, "Внешний", 15)
car2 = CargoVehicle(10, 10, 10, "Внутренний", 10)
car3 = CargoVehicle(15, 15, 15, 'Внутренний', 20)

cars = [car1, car2, car3]
streets = [street1, street2, street3]


#Разделение улиц на горизонтальные и вертикальные
h_streets = [street for street in streets if street.getVector() == "h"]
v_streets = [street for street in streets if street.getVector() == "v"]

#Создание перекрестков
intersections = []
for h_street in h_streets:
  for v_street in v_streets:
    intersections.append(Intersection(v_street.getX(), h_street.getY()))



city1 = City(streets, intersections, cars, 0, 1000)

for street in streets:
  print(f"{street.getName()} X:{street.getX()}, Y:{street.getY()}, {street.getVector()}")

print(".=================================.")

print(f"Перекрестки: {intersections}")

print(".=================================.")


#Спавн машин на улице
for car in cars:
  car.setStartCords(streets)
  car.setTransportCurPosition(streets, intersections)
  print(car.checkTransportCurPosition())
  print(f"КООРДИНАТЫ МАШИНЫ {car.get_vehicle_type()}  X: {car.getX()}, Y: {car.getY()} СКОРОСТЬ: {car.current_speed}")


print(".=================================.")

for street in streets:
  street.setCur_Vehicles(cars)
  print("Список машин: ", street.getName(), street.getCur_Vehicles())

############################################
  

    
#####################################  

# Создаем окно
window = Tk()
window.title('Получение данных')
window.geometry('800x300')

# Метки и поля для ввода координат
x_lb = Label(window, text="Введите координату X точки:")
x_lb.grid(row=0, column=0,)

y_lb = Label(window, text="Введите координату Y точки:")
y_lb.grid(row=1, column=0,)

x_tf = Entry(window)
x_tf.grid(row=0, column=1,)

y_tf = Entry(window)
y_tf.grid(row=1, column=1, )

# Метка и поле для ввода названия улицы
street_name_label = Label(window, text='Введите название улицы:')
street_name_label.grid(row=3, column=0, padx=10, pady=10)

street_name = Entry(window)
street_name.grid(row=3, column=1, padx=10, pady=10)

# Кнопка узнать уровень загрязнения в точке
pollution_btn = Button(window, text='Узнать уровень загрязнения в точке', command=city1.get_abs_pollution_level)
pollution_btn.grid(row=2, column=0, padx=10, pady=10)

noise_btn = Button(window, text='Узнать уровень шума в точке', command=city1.get_abs_noise_level)
noise_btn.grid(row=2, column=1, padx=10, pady=10)


#Кнопка узнать вес груза на улице


# Кнопки для выполнения действий
button = Button(window, text="Симуляция след. шага", command=city1.simulate_all)
button.grid(row=10, column=0, columnspan=2, padx=10, pady=10)

passenger_btn = Button(window, text='Узнать количество пассажиров на улице', command=city1.get_passengers_on_street)
passenger_btn.grid(row=4, column=0,padx=10, pady=10)

passenger_btn = Button(window, text='Узнать вес груза на улице', command=city1.get_weight_on_street)
passenger_btn.grid(row=4, column=1,padx=10, pady=10)

passenger_transports_btn = Button(window, text='Узнать количество Пассажирского транспорта', command=city1.getPassengerTransportAmount)
passenger_transports_btn.grid(row=5, column=0)

cargo_transports_btn = Button(window, text='Узнать количество Грузового транспорта', command=city1.getCargoTransportAmount)
cargo_transports_btn.grid(row=5, column=1)

external_transports_btn = Button(window, text='Узнать количество экологичного транспорта ', command=city1.getExternalEnergySourceTransportAmount)
external_transports_btn.grid(row=5, column=2)

###

root = Tk()
root.geometry('800x800')
root.title("Пример вывода информации при наведении")

canvas = Canvas(root, width=800, height=800)
canvas.pack()


street1 = canvas.create_line(0, 45, 800, 45)
street2 = canvas.create_line(0, 60, 800, 60)
street3 = canvas.create_line(16, 0, 16, 800)
canvas.tag_bind(street1, '<Button-1>', city1.show_street_info_canvas)
canvas.tag_bind(street2, '<Button-1>', city1.show_street_info_canvas)
canvas.tag_bind(street3, '<Button-1>', city1.show_street_info_canvas)


# Создаем прямоугольник на Canvas
#rectangle = canvas.create_rectangle(15, 15, 25, 25, fill='blue')

# Привязываем событие наведения к прямоугольнику
#canvas.tag_bind(rectangle, '<Enter>', show_info)



# Запуск главного цикла окна
window.mainloop()
root.mainloop()
