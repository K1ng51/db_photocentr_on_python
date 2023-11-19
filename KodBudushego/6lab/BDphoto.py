from fastapi import FastAPI, HTTPException #это для работы с API
from pydantic import BaseModel #для работы с БД
import sqlite3

app = FastAPI() #для запуска приложения

def conn_db (): #подключение к БД
    return sqlite3.connect('Photocentr.db') #возвращение подключения к БД


def create_table(): #создание таблицы в БД
    conn = conn_db() #подключение к БД вывзовом класса
    cursor = conn.cursor() #создание курсора для выполнения SQL-запроса

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Stuff (
        ID_Stuff INTEGER PRIMARY KEY,
        Surname TEXT NOT NULL,
        Stuff_name TEXT NOT NULL,
        Email TEXT NULL,
        Phone TEXT NOT NULL,
        Positions TEXT NULL
        )
    ''') #запрос на создание таблицы сотрудников, если её нет в БД

    conn.commit() #сохранение изменений в БД
    conn.close() #закрытие соединения с БД


def add_stuff(surname, stuff_name, email, phone, positions): #добавление сотрудника в БД
    conn = conn_db()
    cursor = conn.cursor()

    cursor.execute('INSERT INTO Stuff (Surname, Stuff_name, Email, Phone, Positions) VALUES (?, ?, ?, ?, ?)',
                   (surname, stuff_name, email, phone, positions)) #запрос на добовление сотрудника

    conn.commit()
    conn.close()


def select_all_staff(): #вывод всех сотрудников
    conn = conn_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Stuff') #запрос на вывод всех сотрудников
    stuffs = cursor.fetchall() #для сортировки всего, что было выбрано и создания массива

    for stuff in stuffs: #вывод всех сотрудников
        print(stuff)

    conn.close()


def select_stuff_surname(surname): #вывод сотрудников по фамилии
    conn = conn_db()
    cursor = conn.cursor()

    cursor.execute('SELECT Surname, Stuff_name, Email, Phone, Positions FROM Stuff WHERE Surname = ?',
                   (surname,)) #запрос на вывод сотрудников с введённой фамилией
    result = cursor.fetchall()

    for row in result:
        print(row)

    conn.close()


def update_email(new_email, surname): #изменение почты сотрудника по фамилии
    conn = conn_db()
    cursor = conn.cursor()

    cursor.execute('UPDATE Stuff SET Email = ? WHERE Surname = ?',
                   (new_email, surname)) #запрос на обновление таблицы сотрудников

    conn.commit()
    conn.close()


def delete_stuff(id): #удаление сотрудника из таблицы
    conn = conn_db()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM Stuff WHERE ID_Stuff = ?',
                   (id,)) #запрос на удаление сотрудника из БД

    conn.commit()
    conn.close()


def main(): #главная функция
    create_table() #создание таблицы, если таковой нет

    while True: #основа программы
        print('-----------------------------------------')
        print('Выберете действие:')
        print('1. Добавить сотрудника')
        print('2. Вывести всех сотрудников')
        print('3. Поиск сотрудника по фамилии')
        print('4. Изменить почту сотрудника')
        print('5. Удалить сотрудника')
        print('0. Выйти')
        print('-----------------------------------------')
        chois = input('\nНомер действия: ') #выбор действия пользователем
        match chois:
            case '1': #кейс для добавления сотрудника пользователем
                surname = input('\nВведите фамилию нового сотрудника: ')
                stuff_name = input('Введите имя нового сотрудника: ')
                email = input('Введите почту нового сотрудника: ')
                phone = input('Введите телефон нового сотрудника: ')
                positions = input('Введите должность нового сотрудника: ')
                add_stuff(surname, stuff_name, email, phone, positions)
                print('\nСотрудник добавлен!')

            case '2': #кейс для вывода всех сотрудников пользователем
                print('\nСписок сотрудников:')
                select_all_staff()

            case '3': #кейс для добавления сотрудника пользователем
                surname = input('\nВведите фамилию сотрудника для поиска: ')
                select_stuff_surname(surname)

            case '4': #кейс для изменения почты сотрудника пользователем
                surname = input('\nВведите фамилию сотрудника для изменения почты: ')
                new_email = input('Укажите новую почту: ')
                update_email(new_email, surname)
                print('\nПочта успешно обновлена!')

            case '5': #кейс для удаления сотрудника пользователем
                id = input('\nВведите номер сотрудника, которого вы хотите удалить: ')
                delete_stuff(id)
                print('Сотрудник успешно удалён!')

            case '0': #кейс выхода из программы
                print('\nВыход из программы.')
                break

class StuffCreate(BaseModel): #модель данных
    Surname: str #атрибуты БД
    Stuff_name: str
    Email: str = None
    Phone: str
    Positions: str

@app.post("/stuff/", response_model=StuffCreate) #создание
async def create_stuff(stuff: StuffCreate): #асинфронная функция функция для создания данных в БД
    add_stuff(stuff.Surname, stuff.Stuff_name, stuff.Email, stuff.Phone, stuff.Positions)
    return stuff

@app.get("/stuff/") #получение, вывод
async def read_stuff(): #вывод всех сотрудников с помощью API
    conn = conn_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Stuff')
    stuff = cursor.fetchall()

    conn.close()

    return {"stuff": stuff}

if __name__ == '__main__': #конструкция для вызова основной функции
    main()

