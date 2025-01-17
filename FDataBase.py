import sqlite3
import math
import time
from flask import url_for
 
class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()
 
    def getMenu(self):
        sql = '''SELECT * FROM review'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print("Ошибка чтения из БД")
        return []
    
    def addReview(self, title, text):
        try:
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO review VALUES(NULL, ?, ?, ?)", (title, text, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД "+str(e))
            return False
 
        return True
    
    def getPost(self, alias):
        try:
            self.__cur.execute("SELECT title, text FROM review WHERE url LIKE ? LIMIT 1", (alias,))
            res = self.__cur.fetchone()
        except sqlite3.Error as e:
            print("Ошибка получения статьи из БД "+str(e))
 
        return (False, False)
    
    def getPostsAnonce(self):
        try:
            self.__cur.execute(f"SELECT id, title, text, time FROM review ORDER BY time DESC")
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print("Ошибка получения статьи из БД "+str(e))
        return []
    
    def addUser(self, name, email, hash_psw):
     '''Добавление пользователя в БД'''
        try:
            # не добавляем пользователя с одинаковым email
            self.__cur.execute(f"SELECT COUNT() as `count` FROM users WHERE email LIKE '{email}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Пользователь с таким email уже существует")
                return False
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO users VALUES(NULL, ?, ?, ?, ?, NULL)", (name, email, hash_psw, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления пользователя в БД "+str(e))
            return False
        return True

    def getUser(self, user_id):
     '''Получение id пользователя'''
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False 
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))
        return False
    
    def getUserByEmail(self, email):
     '''Получение email пользователя'''
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False 
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))
        return False
    
    def updateUserAvatar(self, avatar, user_id):
        '''Изменение аватара пользователя'''
        if not avatar:
            return False
        try:
            binary = sqlite3.Binary(avatar)
            self.__cur.execute(f"UPDATE users SET avatar = ? WHERE id = ?", (binary, user_id))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка обновления аватара в БД: "+str(e))
            return False
        return True
