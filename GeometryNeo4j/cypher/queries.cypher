// 1. Xem toàn bộ node
MATCH (n:TuGiac)
RETURN n;

// 2. Xem toàn bộ graph
MATCH (a:TuGiac)-[r:THEM_TINH_CHAT]->(b:TuGiac)
RETURN a, r, b;

// 3. Danh sách hình
MATCH (n:TuGiac)
RETURN n.tenGoi, n.chuVi, n.dienTich
ORDER BY n.tenGoi;

// 4. Chi tiết hình vuông
MATCH (n:TuGiac {tenGoi:'Hình vuông'})
RETURN n;

// 5. Các hình suy ra trực tiếp từ Hình thang
MATCH (a:TuGiac {tenGoi:'Hình thang'})
      -[r:THEM_TINH_CHAT]->
      (b:TuGiac)
RETURN
    a.tenGoi AS HinhBanDau,
    r.tinhChatThem AS TinhChatThem,
    b.tenGoi AS HinhSuyRa;

// 6. Tìm đường từ Tứ giác đến Hình vuông
MATCH p =
    (a:TuGiac {tenGoi:'Hình tứ giác'})
    -[:THEM_TINH_CHAT*]->
    (b:TuGiac {tenGoi:'Hình vuông'})
RETURN p;

// 7. Tên các node trên đường suy luận
MATCH p =
    (a:TuGiac {tenGoi:'Hình tứ giác'})
    -[:THEM_TINH_CHAT*]->
    (b:TuGiac {tenGoi:'Hình vuông'})
RETURN [n IN nodes(p) | n.tenGoi] AS DuongSuyLuan;

// 8. Tìm hình có tính chất về đường chéo
MATCH (n:TuGiac)
WHERE toLower(n.tinhChat) CONTAINS 'đường chéo'
   OR toLower(n.nhanBiet) CONTAINS 'đường chéo'
RETURN n.tenGoi, n.tinhChat, n.nhanBiet;

// 9. Đếm node và relationship
MATCH (n:TuGiac)
WITH count(n) AS soHinh
MATCH ()-[r:THEM_TINH_CHAT]->()
RETURN soHinh, count(r) AS soQuanHe;
