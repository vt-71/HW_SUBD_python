# pip install psycopg2-binary
# createdb -U admin contacts_hw перейти в папку PostgreSQL

#!!! В программе приняты условия, что фамилия и email клиента уникальны, телефон может принадлежать одному человеку. Имена у разных людей могут совпадать.

import email
import psycopg2


with psycopg2.connect(database='contacts_hw', user='postgres', password='admin') as conn:
    with conn.cursor() as cur:
         
        def create_table(): 
# Функция создает таблицы  
                cur.execute("""
                DROP TABLE phones;
                DROP TABLE personals;
                """)    
                cur.execute("""
                CREATE TABLE IF NOT EXISTS personals(
                id_client SERIAL PRIMARY KEY,
                first_name VARCHAR(40) NOT NULL,
                last_name VARCHAR(40) UNIQUE NOT NULL,
                email VARCHAR(40) UNIQUE); 
                """)
                cur.execute("""
                CREATE TABLE IF NOT EXISTS phones(
                id_client INTEGER NOT NULL REFERENCES personals(id_client),
                phone_client INTEGER);
                """)
                conn.commit() 
        
        def insert_client (recording_list, r):
# Функция вносит нового клиента или редактирует данные у существующего клиента
                if r == 0:           
                        postgres_insert_client = ("""INSERT INTO personals (first_name, last_name, email)
                                                VALUES (%s,%s,%s) RETURNING id_client""")
                        cur.execute (postgres_insert_client, recording_list[:3]) 
                else:
                        cur.execute("""SELECT id_client FROM personals WHERE last_name = %s;""", (recording_list[1],))
                        id_client = cur.fetchone()
                        cur.execute("""UPDATE personals SET (first_name, email) = (%s,%s) WHERE id_client=%s;""", (recording_list[0], recording_list[2], id_client))
                postgres_insert_phone = ("""INSERT INTO phones (id_client, phone_client)
                                                VALUES (%s,%s)""")
                recording_list_phone = [id_client, recording_list[3]]
                cur.execute (postgres_insert_phone, recording_list_phone)         
                conn.commit()  
         
        def insert_phone (last_name, phone_client):
# Функция вносит номер телефона существующего клиента    
                cur.execute("""SELECT id_client FROM personals WHERE last_name = %s;""", (last_name,))
                id_client = cur.fetchone() 
                postgres_insert_phone = ("""INSERT INTO phones (id_client, phone_client)
                                        VALUES (%s,%s)""")
                recording_list = [id_client, phone_client]
                cur.execute (postgres_insert_phone, recording_list)  
        
        def del_phone(last_name, phone_client):
#Функция удаляет телефон существующего клиента
                cur.execute("""SELECT id_client FROM personals WHERE last_name = %s;""", (last_name,))
                id_client = cur.fetchone()
                cur.execute("""
                DELETE FROM phones WHERE id_client=%s AND phone_client=%s;
                """, (id_client, phone_client))
                conn.commit() 
        
        def del_client(last_name):
# Функция удаляет клиента из БД
                cur.execute("""SELECT id_client FROM personals WHERE last_name = %s;""", (last_name,))
                id_client = cur.fetchone()
                cur.execute("""
                DELETE FROM phones WHERE id_client=%s;
                """, (id_client))
                cur.execute("""
                DELETE FROM personals WHERE id_client=%s;
                """, (id_client))
                conn.commit() 
                
        def find_client(client_list):
#Функция, позволяющая найти клиента по его данным
                if client_list[1] != 0:
                        cur.execute("""SELECT * FROM personals WHERE last_name = %s;""", (client_list[1],))
                elif client_list[2] != 0:
                        cur.execute("""SELECT * FROM personals WHERE email = %s;""", (client_list[2],))
                        
                date = cur.fetchone()
                print(f' id клиента: {date[0]}\n имя: {date[1]}\n фамилия: {date[2]}\n email: {date[3]}') 
               
                        
                                
                        
                

        
                
        
        
                

        print('1 - создать новую БД \n2 - ввести данные нового клиента \n3 - внести телефон существующего клиента \n4 - изменить данные клиента \n5 - удалить телефон клиента \n6 - удалить существующего клиента \n7 - найти клиента по его данным')        
        main_menu = int(input('Введите пункт меню: '))

        if main_menu == 1:        
                create_table()
        if main_menu == 2 or main_menu == 4: 
                recording_list = []
                r = 0               
                first_name = input('Введите имя клиента: ')  
                last_name = input('Введите фамилию клиента: ') 
                email = input ('Введите email клиента: ')
                phone_client = input ('Введите номер телефона клиента (цифрами), если нет, введите 0: ')
                recording_list = [first_name, last_name, email, phone_client]
                if main_menu == 4:
                        r = 1
                insert_client(recording_list, r)
        if main_menu == 3:
                last_name = input('Введите фамилию клиента: ') 
                phone_client = input ('Введите номер телефона клиента (цифрами): ')
                insert_phone(last_name, phone_client)
        if main_menu == 5:
                last_name = input('Введите фамилию клиента: ') 
                phone_client = input ('Введите номер удаляемого телефона клиента (цифрами): ')
                del_phone(last_name, phone_client)
                
        if main_menu == 6:
                last_name = input('Введите фамилию клиента: ') 
                del_client(last_name)
        
        if main_menu == 7: 
                client_list = []
                print('Введите данные, которые известны. Если данных нет, введите 0')
                first_name = input('Введите имя клиента: ')  
                last_name = input('Введите фамилию клиента: ') 
                email = input ('Введите email клиента: ')
                phone_client = input ('Введите номер телефона клиента (цифрами), если нет, введите 0: ')
                client_list = [first_name, last_name, email, phone_client]
                find_client(client_list)

                

                
        
        