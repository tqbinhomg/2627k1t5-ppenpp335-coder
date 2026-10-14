class GeometryService:
    def __init__(self, db):
        self.db = db

    def get_all_shapes(self):
        query = """
        MATCH (n:TuGiac)
        RETURN
            n.tenGoi AS tenGoi,
            n.tinhChat AS tinhChat,
            n.nhanBiet AS nhanBiet,
            n.chuVi AS chuVi,
            n.dienTich AS dienTich
        ORDER BY n.tenGoi
        """
        return self.db.execute_query(query)

    def get_shape(self, name):
        query = """
        MATCH (n:TuGiac {tenGoi: $name})
        RETURN
            n.tenGoi AS tenGoi,
            n.tinhChat AS tinhChat,
            n.nhanBiet AS nhanBiet,
            n.chuVi AS chuVi,
            n.dienTich AS dienTich
        """
        rows = self.db.execute_query(query, {"name": name})
        return rows[0] if rows else None

    def get_derived_shapes(self, name):
        query = """
        MATCH (a:TuGiac {tenGoi: $name})
              -[r:THEM_TINH_CHAT]->
              (b:TuGiac)
        RETURN
            b.tenGoi AS tenGoi,
            r.tinhChatThem AS tinhChatThem
        ORDER BY b.tenGoi
        """
        return self.db.execute_query(query, {"name": name})

    def find_paths(self, start, end):
        query = """
        MATCH p =
            (a:TuGiac {tenGoi: $start})
            -[:THEM_TINH_CHAT*1..6]->
            (b:TuGiac {tenGoi: $end})
        RETURN
            [node IN nodes(p) | node.tenGoi] AS path,
            [rel IN relationships(p) | rel.tinhChatThem] AS properties
        LIMIT 10
        """
        return self.db.execute_query(query, {"start": start, "end": end})

    def get_graph(self):
        query = """
        MATCH (a:TuGiac)-[r:THEM_TINH_CHAT]->(b:TuGiac)
        RETURN
            a.tenGoi AS fromShape,
            r.tinhChatThem AS relation,
            b.tenGoi AS toShape
        ORDER BY fromShape, toShape
        """

        return self.db.execute_query(query)

    def search_shapes(self, keyword):
        query = """
        MATCH (n:TuGiac)
        WHERE toLower(n.tenGoi) CONTAINS toLower($keyword)
           OR toLower(n.tinhChat) CONTAINS toLower($keyword)
           OR toLower(n.nhanBiet) CONTAINS toLower($keyword)
        RETURN
            n.tenGoi AS tenGoi,
            n.tinhChat AS tinhChat,
            n.nhanBiet AS nhanBiet
        ORDER BY n.tenGoi
        """
        return self.db.execute_query(query, {"keyword": keyword})
