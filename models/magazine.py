from database.connection import get_db_connection
class Magazine:
    def __init__(self, id, name, category=None):
        self.id = id
        self.name = name
        self._category = category

    def __repr__(self):
        return f'<Magazine {self.name}>'


    @property
    def id(self):
        return self._id

    @id.setter
    def id(self,id):
        if not isinstance(id,int):
            raise ValueError("id must be a type of integer")
        self._id = id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self,name):
        if not isinstance(name,str) or len(name) < 2 or len(name) > 16:
            raise ValueError("Name must be a string between 2 and 16 characters")
        self._name = name

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self,category):
        if not isinstance(category,str) or len(category) == 0:
            raise ValueError("Category must be a non-empty string")
        self._category = category

    def articles(self):
        conn = get_db_connection()
        CURSOR = conn.cursor()
        sql = """
            SELECT *
            FROM articles
            WHERE margazine_id = ?
        """
        CURSOR.execute(sql,(self.id))
        articles = CURSOR.fetchall()
        conn.close()
        return articles

    def contributors(self):
        conn = get_db_connection()
        CURSOR = conn.cursor()
        sql = """
            SELECT * 
            FROM authors 
            WHERE id IN (
                SELECT author_id 
                FROM articles 
                WHERE magazine_id =?
            )   
        """
        CURSOR.execute(sql,(self.id))
        contributors = CURSOR.fetchall()
        conn.close()
        return contributors

    def article_titles(self):
        conn = get_db_connection()
        CURSOR = conn.cursor()
        sql = """
            SELECT title 
            FROM articles 
            WHERE magazine_id =?
        """
        CURSOR.execute(sql,(self.id))
        titles = CURSOR.fetchall()
        conn.close()
        if titles:
            return [title[0] for title in titles]
        else:
            return None
        

    def contributing_authors(self):
        conn = get_db_connection()
        CURSOR = conn.cursor()
        sql = """
            SELECT author_id, 
            COUNT(*) as count 
            FROM articles 
            WHERE magazine_id =? 
            GROUP BY author_id 
            HAVING count > 2
        """
        CURSOR.execute(sql,(self.id))
        authors = CURSOR.fetchall()
        conn.close()
        if authors:
            return [Author(author[0]) for author in authors]
        else:
            return None
    
    @classmethod
    def find_by_id(cls, id):
        conn = get_db_connection()
        CURSOR = conn.cursor()
        sql = """
            SELECT id, name, category 
            FROM magazines 
            WHERE id =?
        """
        CURSOR.execute(sql, (id,))
        result = CURSOR.fetchone()
        conn.close()
        if result:
            return cls(*result)
        else:
            return None