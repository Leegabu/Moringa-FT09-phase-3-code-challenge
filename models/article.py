from database.connection import get_db_connection
class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id


    def __repr__(self):
        return f'<Article {self.title}>'

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self,title):
        if not isinstance(title,str) or len(title) < 5 or len(title) > 50:
            raise ValueError("Title must be a string between 5 and 50 characters")
        if hasattr(self,'_title'):
            raise AttributeError("Title cannot be changed after initialization")
        self._title = title

    @property 
    def content(self):
        return self._content

    @content.setter
    def content(self,content):
        if not isinstance(content,str) or len(content) == 0:
            raise ValueError("Content must be a non-empty string")
        self._content = content
    

    def author(self):
        conn = get_db_connection()
        CURSOR = conn.cursor()
        sql = """
            SELECT *
            FROM authors
            WHERE id = ?
        """
        CURSOR.execute(sql,(self.id))
        author = CURSOR.fetchone()
        conn.close()
        return author
        

    def magazine(self):
        conn = get_db_connection()
        CURSOR = conn.cursor()
        sql = """
            SELECT *
            FROM magazines
            WHERE id = ?
        """
        CURSOR.execute(sql,(self.id))
        magazine = CURSOR.fetchone()
        conn.close()
        return magazine

    

