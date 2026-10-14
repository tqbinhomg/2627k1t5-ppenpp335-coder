// XÓA DỮ LIỆU CŨ
MATCH (n:TuGiac)
DETACH DELETE n;

// =====================
// NODE
// =====================

CREATE (:TuGiac {
    tenGoi: 'Hình tứ giác',
    tinhChat: 'Có 4 cạnh, 4 góc và 4 đỉnh. Tổng số đo bốn góc trong bằng 360°.',
    nhanBiet: 'Một hình có 4 cạnh, 4 góc và 4 đỉnh là hình tứ giác.',
    chuVi: 'P = a + b + c + d',
    dienTich: 'Tùy dạng tứ giác, áp dụng công thức diện tích tương ứng.'
});

CREATE (:TuGiac {
    tenGoi: 'Hình thang',
    tinhChat: 'Có một cặp cạnh đối song song gọi là hai đáy. Hai cạnh còn lại gọi là hai cạnh bên.',
    nhanBiet: 'Nếu một tứ giác có một cặp cạnh đối song song thì đó là hình thang.',
    chuVi: 'P = a + b + c + d',
    dienTich: 'S = (a + b) × h / 2'
});

CREATE (:TuGiac {
    tenGoi: 'Hình thang cân',
    tinhChat: 'Có một cặp cạnh đối song song. Hai cạnh bên bằng nhau. Hai góc kề một đáy bằng nhau. Hai đường chéo bằng nhau.',
    nhanBiet: 'Nếu một hình thang có hai cạnh bên bằng nhau thì là hình thang cân. Hoặc nếu hai góc kề một đáy bằng nhau. Hoặc nếu hai đường chéo bằng nhau.',
    chuVi: 'P = a + b + 2c',
    dienTich: 'S = (a + b) × h / 2'
});

CREATE (:TuGiac {
    tenGoi: 'Hình thang vuông',
    tinhChat: 'Có một cặp cạnh đối song song và có hai góc vuông. Một cạnh bên vuông góc với hai đáy.',
    nhanBiet: 'Nếu một hình thang có một cạnh bên vuông góc với hai đáy thì đó là hình thang vuông.',
    chuVi: 'P = a + b + c + d',
    dienTich: 'S = (a + b) × h / 2'
});

CREATE (:TuGiac {
    tenGoi: 'Hình bình hành',
    tinhChat: 'Có hai cặp cạnh đối song song. Các cạnh đối bằng nhau. Các góc đối bằng nhau. Hai đường chéo cắt nhau tại trung điểm của mỗi đường.',
    nhanBiet: 'Tứ giác có hai cặp cạnh đối song song là hình bình hành. Hoặc hai cặp cạnh đối bằng nhau. Hoặc một cặp cạnh đối vừa song song vừa bằng nhau. Hoặc hai đường chéo cắt nhau tại trung điểm của mỗi đường.',
    chuVi: 'P = 2(a + b)',
    dienTich: 'S = a × h'
});

CREATE (:TuGiac {
    tenGoi: 'Hình chữ nhật',
    tinhChat: 'Có bốn góc vuông. Hai cặp cạnh đối song song và bằng nhau. Hai đường chéo bằng nhau và cắt nhau tại trung điểm của mỗi đường.',
    nhanBiet: 'Tứ giác có bốn góc vuông là hình chữ nhật. Hoặc hình bình hành có một góc vuông. Hoặc hình bình hành có hai đường chéo bằng nhau.',
    chuVi: 'P = 2(a + b)',
    dienTich: 'S = a × b'
});

CREATE (:TuGiac {
    tenGoi: 'Hình thoi',
    tinhChat: 'Có bốn cạnh bằng nhau. Hai cặp cạnh đối song song. Các góc đối bằng nhau. Hai đường chéo vuông góc và cắt nhau tại trung điểm của mỗi đường. Hai đường chéo là các đường phân giác của các góc.',
    nhanBiet: 'Tứ giác có bốn cạnh bằng nhau là hình thoi. Hoặc hình bình hành có hai cạnh kề bằng nhau. Hoặc hình bình hành có hai đường chéo vuông góc.',
    chuVi: 'P = 4a',
    dienTich: 'S = a × h hoặc S = d₁ × d₂ / 2'
});

CREATE (:TuGiac {
    tenGoi: 'Hình vuông',
    tinhChat: 'Có bốn cạnh bằng nhau và bốn góc vuông. Hai cặp cạnh đối song song. Hai đường chéo bằng nhau, vuông góc, cắt nhau tại trung điểm của mỗi đường và là các đường phân giác của các góc.',
    nhanBiet: 'Tứ giác có bốn cạnh bằng nhau và bốn góc vuông là hình vuông. Hoặc hình chữ nhật có hai cạnh kề bằng nhau. Hoặc hình thoi có một góc vuông.',
    chuVi: 'P = 4a',
    dienTich: 'S = a²'
});

// =====================
// RELATIONSHIP
// =====================

MATCH (a:TuGiac {tenGoi:'Hình tứ giác'}),
      (b:TuGiac {tenGoi:'Hình thang'})
CREATE (a)-[:THEM_TINH_CHAT {
    tinhChatThem:'Có một cặp cạnh đối song song'
}]->(b);

MATCH (a:TuGiac {tenGoi:'Hình thang'}),
      (b:TuGiac {tenGoi:'Hình thang cân'})
CREATE (a)-[:THEM_TINH_CHAT {
    tinhChatThem:'Có hai cạnh bên bằng nhau'
}]->(b);

MATCH (a:TuGiac {tenGoi:'Hình thang'}),
      (b:TuGiac {tenGoi:'Hình thang vuông'})
CREATE (a)-[:THEM_TINH_CHAT {
    tinhChatThem:'Có hai góc vuông'
}]->(b);

MATCH (a:TuGiac {tenGoi:'Hình thang'}),
      (b:TuGiac {tenGoi:'Hình bình hành'})
CREATE (a)-[:THEM_TINH_CHAT {
    tinhChatThem:'Có thêm một cặp cạnh đối song song'
}]->(b);

MATCH (a:TuGiac {tenGoi:'Hình bình hành'}),
      (b:TuGiac {tenGoi:'Hình chữ nhật'})
CREATE (a)-[:THEM_TINH_CHAT {
    tinhChatThem:'Có bốn góc vuông'
}]->(b);

MATCH (a:TuGiac {tenGoi:'Hình bình hành'}),
      (b:TuGiac {tenGoi:'Hình thoi'})
CREATE (a)-[:THEM_TINH_CHAT {
    tinhChatThem:'Có bốn cạnh bằng nhau'
}]->(b);

MATCH (a:TuGiac {tenGoi:'Hình chữ nhật'}),
      (b:TuGiac {tenGoi:'Hình vuông'})
CREATE (a)-[:THEM_TINH_CHAT {
    tinhChatThem:'Có bốn cạnh bằng nhau'
}]->(b);

MATCH (a:TuGiac {tenGoi:'Hình thoi'}),
      (b:TuGiac {tenGoi:'Hình vuông'})
CREATE (a)-[:THEM_TINH_CHAT {
    tinhChatThem:'Có bốn góc vuông'
}]->(b);
