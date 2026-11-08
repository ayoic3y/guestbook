from flask import Flask, request
import psycopg2
import os
import time

app = Flask(__name__)

def get_db():
    time.sleep(1) # Ждем БД при старте
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'db'),
        database=os.getenv('POSTGRES_DB', 'ilyadb'),
        user=os.getenv('POSTGRES_USER', 'ilya'),
        password=os.getenv('POSTGRES_PASSWORD', 'secret')
    )

@app.route('/')
def guestbook():
    conn = get_db()
    cur = conn.cursor()
    
    # 1. Создаем таблицу, если ее нет (с колонками name и message)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS guestbook (
            id SERIAL PRIMARY KEY, 
            name VARCHAR(50), 
            message TEXT
        );
    """)
    
    # 2. Получаем данные из HTML-формы (из URL)
    name = request.args.get('name')
    message = request.args.get('message')
    
    # 3. Если данные ввели, сохраняем в БД
    if name and message:
        cur.execute("INSERT INTO guestbook (name, message) VALUES (%s, %s);", (name, message))
        conn.commit()
        
    # 4. Достаем все записи из базы (сначала новые)
    cur.execute("SELECT name, message FROM guestbook ORDER BY id DESC;")
    rows = cur.fetchall()
    
    cur.close()
    conn.close()
    
    # 5. Формируем красивый HTML-ответ
    html = "<h1>Гостевая книга DevOps</h1>"
    html += """
    <form>
        <input type="text" name="name" placeholder="Ваше имя" required>
        <input type="text" name="message" placeholder="Сообщение" required>
        <button type="submit">Отправить</button>
    </form>
    """
    
    for row in rows:
        html += f"<p><b>{row[0]}:</b> {row[1]}</p>"
        
    return html

@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
