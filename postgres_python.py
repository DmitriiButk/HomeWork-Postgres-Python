import psycopg2
from psycopg2 import sql


def delete_client_database(conn):
    """Удаляет структуру БД Client."""
    with conn.cursor() as cur:
        cur.execute("""
        DROP TABLE Phone;
        DROP TABLE Client;
        """)
        conn.commit()
    return print(f"Вы удалили структуру БД Client")


def create_database(conn):
    """Создаёт структуру БД Client."""
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Client (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            surname VARCHAR(50) NOT NULL,
            email VARCHAR(60) NOT NULL
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS Phone(
            id SERIAL PRIMARY KEY,
            number bigint NOT NULL,
            Client_id INTEGER REFERENCES Client(id)
        );
        """)
        conn.commit()
    return print(f"Вы создали структуру БД Client")


def add_client(conn, name, surname, email):
    """Добавляет клиента в структуру БД Client."""
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO Client (name, surname, email)
        VALUES (%s, %s, %s);
        """, (name, surname, email,))
        conn.commit()


def add_phone(conn, client_id, number):
    """Добавляет номер телефона в структуру БД Phone, к определённому клиенту."""
    with conn.cursor() as cur:
        cur.execute(sql.SQL("""
        INSERT INTO Phone (number, Client_id)
        VALUES ({number}, {client_id});
        """).format(number=sql.Literal(number), client_id=sql.Literal(client_id),))
        conn.commit()
        print(f"Номер телефона: {number} добавлен клиенту: {client_id}")


def change_client(conn, client_id, name=None, surname=None, email=None):
    """Производит изменение информации клиента."""
    if name is not None:
        with conn.cursor() as cur:
            cur.execute("""UPDATE Client SET name=%s WHERE id=%s;
            """, (name, client_id,))
            conn.commit()
    if name is not None and surname is not None:
        with conn.cursor() as cur:
            cur.execute("""UPDATE Client SET name=%s, surname=%s WHERE id=%s;
            """, (name, surname, client_id,))
            conn.commit()
    if name is not None and email is not None:
        with conn.cursor() as cur:
            cur.execute("""UPDATE Client SET name=%s, email=%s WHERE id=%s;
            """, (name, email, client_id,))
            conn.commit()
    if name is not None and surname is not None and email is not None:
        with conn.cursor() as cur:
            cur.execute("""UPDATE Client SET name=%s, surname=%s, email=%s WHERE id=%s;
            """, (name, surname, email, client_id,))
            conn.commit()
    if surname is not None:
        with conn.cursor() as cur:
            cur.execute("""UPDATE Client SET surname=%s WHERE id=%s;
            """, (surname, client_id,))
            conn.commit()
    if surname is not None and email is not None:
         with conn.cursor() as cur:
             cur.execute("""UPDATE Client SET surname=%s, email=%s WHERE id=%s;
             """, (surname, email, client_id,))
             conn.commit()
    if email is not None:
         with conn.cursor() as cur:
             cur.execute("""UPDATE Client SET email=%s WHERE id=%s;
             """, (email, client_id,))
             conn.commit()


def change_phone(conn, client_id, number):
    """Производит изменение номера телефона клиента."""
    with conn.cursor() as cur:
        cur.execute(sql.SQL("""
        UPDATE Phone SET number={number}
        WHERE Client_id={client_id};
        """).format(number=sql.Literal(number),
                    client_id=sql.Literal(client_id),))
        conn.commit()
        print(f"Номер телефона клиента: {client_id} был изменён на: {number}")


def delete_phone(conn, client_id):
    """Удаляет номер телефона у клиента."""
    with conn.cursor() as cur:
        cur.execute(sql.SQL("""
        DELETE FROM Phone WHERE Client_id={client_id};
        """).format(client_id=sql.Literal(client_id),))
        conn.commit()
        print(f"У клиента: {client_id} был удалён номер телефона.")


def delete_client(conn, client_id):
    """Удаляет клиента."""
    with conn.cursor() as cur:
        cur.execute(sql.SQL("""
        DELETE FROM Phone WHERE Client_id={client_id};
        DELETE FROM Client WHERE id={client_id};
        """).format(client_id=sql.Literal(client_id),))
        conn.commit()
        print(f"Клиент: {client_id} был удалён.")


def find_client(conn, name=None, surname=None, email=None, number= None):
    """Находит клиента и выводит информацию о нём."""
    if name is not None:
        with conn.cursor() as cur:
            cur.execute("""
            SELECT C.name, C.surname, C.email, P.number FROM Client AS C
            LEFT JOIN Phone AS P ON C.id = P.id WHERE C.name=%s;
            """, (name,))
            return print(cur.fetchall())
    if surname is not None:
        with conn.cursor() as cur:
            cur.execute("""
            SELECT C.name, C.surname, C.email, P.number FROM Client AS C
            LEFT JOIN Phone AS P ON C.id = P.id WHERE C.surname=%s;
            """, (surname,))
            return print(cur.fetchall())
    if email is not None:
        with conn.cursor() as cur:
            cur.execute("""
            SELECT C.name, C.surname, C.email, P.number FROM Client AS C
            LEFT JOIN Phone AS P ON C.id = P.id WHERE C.email=%s;
            """, (email,))
            return print(cur.fetchall())
    if number is not None:
        with conn.cursor() as cur:
            cur.execute("""
            SELECT C.name, C.surname, C.email, P.number FROM Client AS C
            LEFT JOIN Phone AS P ON C.id = P.id WHERE P.number=%s;
            """, (number,))
            return print(cur.fetchall())


def view_table(conn, table_name):
    """Выводит информацию о структуре БД (необходимо ввести название структуры БД)."""
    with conn.cursor() as cur:
        cur.execute(sql.SQL("""
        SELECT * FROM {table_name}
        """).format(table_name = sql.Identifier(table_name.lower()),))
        return print(cur.fetchall())


if __name__ == '__main__':
    with psycopg2.connect(database="clients_db", user="postgres", password="postgres") as conn:
        # delete_client_database(conn)
        # create_database(conn)
        # add_client(conn,"Дмитрий", "Бутков", "razdva@gmail.com")
        # add_client(conn, "Андрей", "Ярославский", "trichetire@gmail.com")
        # add_client(conn, "Елизавета", "Борова", "pyatshest@gmail.com")
        # view_table(conn, "Client")
        # add_phone(conn, 1, 89999999999)
        # add_phone(conn, 2, 88888888888)
        # add_phone(conn, 3, 87777777777)
        # view_table(conn, "Phone")
        # change_client(conn, 1, "Альберт", "Быстров", "poltinnik@gmail.com")
        # change_client(conn, 1, "Oleg")
        # change_client(conn, 2, "Karina", "Verbova")
        # change_client(conn, 2, "Кристина", "Зраза", "zraza@gmail.com")
        # change_client(conn, 3, "Анатолий", "Курников", "kurnikpro@gmail.com")
        # view_table(conn, "Client")
        # change_phone(conn, 1, 77777777777)
        # change_phone(conn, 2, 66666666666)
        # view_table(conn, "Phone")
        # delete_phone(conn, 1)
        # delete_phone(conn, 2)
        # delete_phone(conn, 3)
        # view_table(conn, "Phone")
        # find_client(conn, "Анатолий")
        # delete_client(conn, 1)
        # delete_client(conn, 2)
        # delete_client(conn, 3)
        # view_table(conn, "Client")
        # view_table(conn, "Phone")
    conn.close()
