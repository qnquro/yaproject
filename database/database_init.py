import os

import psycopg2 as ps
from psycopg2 import sql
from dotenv import load_dotenv
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import logging

logger = logging.getLogger(__name__)

load_dotenv()
password = os.getenv("PASSWORD")
host = os.getenv("HOST")
user = os.getenv("USER")
db_name = os.getenv("DB_NAME")


def create_table():
    try:
        with ps.connect(
                host=host,
                password=password,
                user=user,
                dbname=db_name
        ) as conn:
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            with conn.cursor() as cursor:
                cursor.execute(sql.SQL("""
                    CREATE TABLE IF NOT EXISTS themes (
                        id SERIAL PRIMARY KEY,
                        title VARCHAR(255) NOT NULL CHECK (title <> ''),
                        parent_id INT REFERENCES themes(id) ON DELETE CASCADE,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                        CONSTRAINT unique_theme_parent UNIQUE (title, parent_id)
                    );
                """))

                cursor.execute(sql.SQL("""
                    CREATE TABLE IF NOT EXISTS discussions (
                        id SERIAL PRIMARY KEY,
                        theme_id INT NOT NULL REFERENCES themes(id) ON DELETE CASCADE,
                        parent_discussion_id INT REFERENCES discussions(id) ON DELETE CASCADE,
                        author VARCHAR(100) NOT NULL CHECK (author <> ''),
                        content TEXT,
                        content_type VARCHAR(10) DEFAULT 'text',
                        media_id VARCHAR(255),
                        user_id BIGINT,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                        is_root BOOLEAN DEFAULT TRUE 
                    );
                """))
    except ps.Error as e:
        logger.error(f"Ошибка при создании тем {e}")
        raise RuntimeError("Theme initialization failed") from e


def create_themes():
    try:
        with ps.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
        ) as conn:
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

            with conn.cursor() as cursor:
                cursor.execute(sql.SQL("""
                    INSERT INTO themes (title, parent_id)
                    VALUES 
                        ('IT', NULL),
                        ('Спорт', NULL),
                        ('Отношения', NULL),`
                        ('Игры', NULL),
                        ('Фильмы/Книги/Музыка', NULL),
                        ('Мемы', NULL)
                    ON CONFLICT (title, parent_id) DO NOTHING;
                """))
                logger.info("Темы успешно созданы или уже существуют")
    except ps.Error as e:
        logger.error(f"Ошибка при создании тем: {e}")
        raise RuntimeError("Themes initialization failed") from e


def create_subthemes():
    try:
        with ps.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
        ) as conn:
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

            with conn.cursor() as cursor:
                cursor.execute("""
            INSERT INTO themes (title, parent_id)
            VALUES
            ('WEB-программирование', 1),
            ('Кибербезопасность', 1),
             ('Gamedev', 1),
             ('Desktop', 1),
             ('Mobile', 1),
             ('DevOps', 1),
             ('Дизайн', 1),
             ('Прочее', 1),

            ('Велоспорт', 2),
            ('Автоспорт', 2),
            ('Мотоспорт', 2),
            ('Водные виды спорта', 2),
            ('Беговые и прыжковые виды спорта', 2),
            ('Боевые искусства', 2),
            ('Прочее', 2),

            ('Измена', 3),
            ('Сложности в отношениях', 3),
            ('Стоит ли?...', 3),
            ('Развитие отношений', 3),
            ('Друзья', 3),
            ('Прочее', 3),        

            ('Шутеры', 4),
            ('Гоночные', 4),
            ('Симуляторы', 4),
            ('Инди', 4),
            ('AAA', 4),
            ('Хорроры', 4),
            ('Новеллы', 4),
            ('Прочее', 4),

            ('Романтика', 5),
            ('Комедия', 5),
            ('Грустные', 5),
            ('Боевики', 5),
            ('18+', 5),
            ('Классика', 5),
            ('Хоррор', 5),
            ('Прочее', 5),

            ('Анекдоты', 6),
            ('Старые', 6),
            ('Новые', 6),
            ('ВЕБМЫ', 6),
            ('Чёрный юмор', 6),
            ('Прочее', 6)
            """)
        logger.info("Темы успешно созданы или уже существуют")
    except ps.Error as e:
        logger.error(f"Ошибка при создании тем: {e}")
        raise RuntimeError("Themes initialization failed") from e


if __name__ == "__main__":
    create_table()
    create_themes()
    create_subthemes()