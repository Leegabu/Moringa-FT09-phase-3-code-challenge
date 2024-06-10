from database.connection import get_db_connection
class Author:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return f'<Author {self.name}>'

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self,id):
        if not isinstance(id,int):
            raise TypeError("id must be of type int")
        self._id = id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self,name):
        if not isinstance(name,str) or len(name) == 0:
            raise ValueError("Name must be a non-empty string")
        if hasattr(self,'_name'):
            raise AttributeError("Name cannot be changed after initialization")
        self._name = name

    def articles(self):
        conn = get_db_connection()
        CURSOR = conn.cursor()
        sql = """
            SELECT *
            FROM articles
            WHERE author_id = ?
        """
        CURSOR.execute(sql,(self.id))
        return CURSOR.fetchall()

    def magazines(self):
        conn = get_db_connection()
        CURSOR = conn.cursor()
        sql = """
            SELECT *
            FROM magazines
            WHERE id IN (
                SELECT magazine_id
                FROM articles
                WHERE author_id =?
            )
        """
        CURSOR.execute(sql, (self.id,))
        return CURSOR.fetchall()