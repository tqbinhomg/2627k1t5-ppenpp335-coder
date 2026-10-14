import streamlit as st
from neo4j_connection import Neo4jConnection
from geometry_service import GeometryService
from pyvis.network import Network
import streamlit.components.v1 as components
import base64
import html



st.set_page_config(
    page_title="Geometry Knowledge Graph",
    page_icon="📐",
    layout="wide"
)


@st.cache_resource
def get_service():
    db = Neo4jConnection()
    db.verify_connection()
    return GeometryService(db)


def svg_data_uri(svg):
    encoded = base64.b64encode(
        svg.encode("utf-8")
    ).decode("utf-8")

    return f"data:image/svg+xml;base64,{encoded}"


def create_shape_svg(shape_name):

    if shape_name == "Hình tứ giác":
        polygon = "45,15 155,15 175,85 25,85"

    elif shape_name == "Hình thang":
        polygon = "55,15 145,15 175,85 25,85"

    elif shape_name == "Hình thang cân":
        polygon = "55,15 145,15 170,85 30,85"

    elif shape_name == "Hình thang vuông":
        polygon = "35,15 145,15 170,85 35,85"

    elif shape_name == "Hình bình hành":
        polygon = "55,15 175,15 145,85 25,85"

    elif shape_name == "Hình chữ nhật":
        polygon = "25,20 175,20 175,80 25,80"

    elif shape_name == "Hình thoi":
        polygon = "100,10 175,50 100,90 25,50"

    elif shape_name == "Hình vuông":
        polygon = "40,10 160,10 160,90 40,90"

    else:
        polygon = "25,15 175,15 175,85 25,85"

    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg"
         width="220"
         height="130"
         viewBox="0 0 220 130">

        <polygon
            points="{polygon}"
            fill="#1e293b"
            stroke="#60a5fa"
            stroke-width="4"
            stroke-linejoin="round"/>

        <text
            x="110"
            y="120"
            text-anchor="middle"
            fill="white"
            font-size="14"
            font-family="Arial">
            {shape_name}
        </text>

    </svg>
    """

    return svg_data_uri(svg)


def create_graph(service):

    relations = service.get_graph()

    net = Network(
        height="700px",
        width="100%",
        directed=True,
        bgcolor="#0b1120",
        font_color="white"
    )

    added_nodes = set()

    for relation in relations:

        from_shape = relation["fromShape"]
        to_shape = relation["toShape"]
        property_added = relation["relation"]

        # Bỏ dữ liệu không hợp lệ
        if not from_shape or not to_shape:
            continue

        # =========================
        # NODE HÌNH BAN ĐẦU
        # =========================

        if from_shape not in added_nodes:

            net.add_node(
                from_shape,
                label="",
                title=from_shape,
                shape="image",
                image=create_shape_svg(from_shape),
                size=45
            )

            added_nodes.add(from_shape)

        # =========================
        # NODE HÌNH ĐƯỢC SUY RA
        # =========================

        if to_shape not in added_nodes:

            net.add_node(
                to_shape,
                label="",
                title=to_shape,
                shape="image",
                image=create_shape_svg(to_shape),
                size=45
            )

            added_nodes.add(to_shape)

        # =========================
        # QUAN HỆ
        # =========================

        net.add_edge(
            from_shape,
            to_shape,
            label=property_added,
            title=property_added,
            arrows="to",
            color="#94a3b8",
            font={
                "color": "white",
                "size": 12,
                "strokeWidth": 0
            }
        )

    # =========================
    # CẤU HÌNH GRAPH
    # =========================

    net.set_options("""
    {
        "layout": {
            "hierarchical": {
                "enabled": true,
                "direction": "LR",
                "sortMethod": "directed",
                "levelSeparation": 250,
                "nodeSpacing": 180,
                "treeSpacing": 250
            }
        },

        "physics": {
            "enabled": false
        },

        "interaction": {
            "hover": true,
            "navigationButtons": true,
            "keyboard": true,
            "zoomView": true,
            "dragView": true
        },

        "edges": {
            "smooth": {
                "type": "cubicBezier",
                "forceDirection": "horizontal",
                "roundness": 0.4
            },

            "arrows": {
                "to": {
                    "enabled": true,
                    "scaleFactor": 0.8
                }
            },

            "font": {
                "color": "white",
                "size": 12,
                "strokeWidth": 0
            }
        }
    }
    """)

    return net
def get_short_property(text, max_sentences=2):
    if not text:
        return ""

    sentences = [
        sentence.strip()
        for sentence in text.split(".")
        if sentence.strip()
    ]

    return ". ".join(sentences[:max_sentences]) + (
        "." if sentences else ""
    )

def main():
    st.title("📐 Geometry Knowledge Graph")
    st.caption("Mô hình hóa Tứ giác trong hình học phẳng với Neo4j")

    try:
        service = get_service()
    except Exception as e:
        st.error("Không thể kết nối Neo4j.")
        st.code(str(e))
        st.info(
            "Kiểm tra Neo4j đang chạy và file .env đã có "
            "NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD."
        )
        return

    st.sidebar.header("Chức năng")

    
    pages = [
        "Danh sách hình",
        "Chi tiết hình",
        "Đồ thị Knowledge Graph",
        "Hình được suy ra",
        "Tìm đường suy luận",
        "Tìm kiếm kiến thức",
        "Quan hệ trong Graph"
    ]

    if "page" not in st.session_state:
        st.session_state["page"] = "Danh sách hình"

    selected_page = st.sidebar.radio(
        "Chọn chức năng",
        pages,
        index=pages.index(st.session_state["page"])
    )

    st.session_state["page"] = selected_page

    option = st.session_state["page"]
    
    st.write("PAGE:", st.session_state.get("page"))
    st.write("OPTION:", option)
    st.write("SHAPE:", st.session_state.get("selected_shape"))

    if option == "Danh sách hình":

        st.caption(
            "Tổng quan các loại tứ giác được mô hình hóa "
            "trong Knowledge Graph với Neo4j."
        )

        # ==========================================
        # LẤY DỮ LIỆU TỪ NEO4J
        # ==========================================

        shapes = service.get_all_shapes()
        relations = service.get_graph()

        # ==========================================
        # THỐNG KÊ TỔNG QUAN
        # ==========================================

        total_shapes = len(shapes)

        total_relations = len([
            x for x in relations
            if x["relation"] is not None
        ])

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "📐 Loại hình",
                total_shapes
            )

        with col2:
            st.metric(
                "🔗 Quan hệ suy luận",
                total_relations
            )

        with col3:
            st.metric(
                "🧠 Knowledge Graph",
                "Neo4j"
            )

        st.markdown("---")

        # ==========================================
        # DANH SÁCH 8 HÌNH
        # ==========================================

        st.subheader("Các hình được mô hình hóa")

        # Hiển thị 4 card / hàng
        for row_start in range(0, len(shapes), 4):

            cols = st.columns(4)

            row_shapes = shapes[row_start:row_start + 4]

            for col, shape in zip(cols, row_shapes):

                with col:

                    name = shape["tenGoi"]

                    # ----------------------------------
                    # HÌNH MINH HỌA
                    # ----------------------------------

                    image_data = create_shape_svg(name)

                    # ----------------------------------
                    # TÍNH CHẤT NGẮN
                    # ----------------------------------

                    short_property = get_short_property(
                        shape["tinhChat"],
                        max_sentences=2
                    )

                    # Escape HTML
                    safe_name = html.escape(name)
                    safe_property = html.escape(short_property)

                    safe_perimeter = html.escape(
                        shape["chuVi"] or ""
                    )

                    safe_area = html.escape(
                        shape["dienTich"] or ""
                    )

                    # ----------------------------------
                    # CARD
                    # ----------------------------------

                    st.html(
                        f"""
                        <div style="
                            background-color: #151922;
                            border: 1px solid #303642;
                            border-radius: 12px;
                            padding: 16px;
                            min-height: 420px;
                            margin-bottom: 12px;
                            box-shadow: 0 4px 12px rgba(0,0,0,0.25);
                        ">

                            <div style="
                                text-align: center;
                                margin-bottom: 10px;
                            ">
                                <img
                                    src="{image_data}"
                                    style="
                                        width: 190px;
                                        height: 120px;
                                        object-fit: contain;
                                    "
                                >
                            </div>

                            <h3 style="
                                text-align: center;
                                margin-top: 5px;
                                margin-bottom: 15px;
                                color: #ffffff;
                                font-size: 20px;
                            ">
                                {safe_name}
                            </h3>

                            <div style="
                                color: #cbd5e1;
                                font-size: 14px;
                                line-height: 1.6;
                                min-height: 75px;
                            ">
                                <b style="color:#ffffff;">
                                    Tính chất
                                </b>

                                <br>

                                {safe_property}
                            </div>

                            <div style="
                                border-top: 1px solid #303642;
                                margin-top: 12px;
                                padding-top: 10px;
                                color: #94a3b8;
                                font-size: 14px;
                            ">

                                <div>
                                    <b style="color:#60a5fa;">
                                        Chu vi:
                                    </b>
                                    {safe_perimeter}
                                </div>

                                <div style="margin-top:5px;">
                                    <b style="color:#60a5fa;">
                                        Diện tích:
                                    </b>
                                    {safe_area}
                                </div>

                            </div>

                        </div>
                        """
                    )

                    # ----------------------------------
                    # NÚT XEM CHI TIẾT
                    # ----------------------------------

                    if st.button(
                        "Xem chi tiết →",
                        key=f"detail_{row_start}_{name}",
                        use_container_width=True
                    ):
                        st.session_state["selected_shape"] = name
                        st.session_state["page"] = "Chi tiết hình"
                        st.rerun()

    elif option == "Chi tiết hình":
        st.header("Thông tin hình")

        shapes = service.get_all_shapes()
        names = [x["tenGoi"] for x in shapes]
        if not names:
            st.warning("Chưa có dữ liệu hình trong Neo4j.")
            st.stop()
        default_shape = st.session_state.get(
            "selected_shape",
            names[0]
        )

        default_index = (
            names.index(default_shape)
            if default_shape in names
            else 0
        )

        selected = st.selectbox(
            "Chọn hình",
            names,
            index=default_index
        )
        shape = service.get_shape(selected)

        if shape:
            # Chia thành 2 cột:
            # bên trái: thông tin
            # bên phải: hình học
            col1, col2 = st.columns([2, 1])

            with col1:
                st.subheader(shape["tenGoi"])

                st.markdown("### Tính chất")
                st.write(shape["tinhChat"])

                st.markdown("### Nhận biết")
                st.write(shape["nhanBiet"])

                st.markdown("### Chu vi")
                st.info(shape["chuVi"])

                st.markdown("### Diện tích")
                st.info(shape["dienTich"])

            with col2:
                st.subheader("Hình minh họa")

                image_data = create_shape_svg(shape["tenGoi"])

                st.image(
                    image_data,
                    width=280
                )

    elif option == "Hình được suy ra":
        st.header("Hình được suy ra từ một hình")

        shapes = service.get_all_shapes()
        names = [x["tenGoi"] for x in shapes]

        selected = st.selectbox("Chọn hình ban đầu", names)
        results = service.get_derived_shapes(selected)

        if results:
            for item in results:
                st.success(
                    f"{selected} + {item['tinhChatThem']} "
                    f"→ **{item['tenGoi']}**"
                )
        else:
            st.info("Không có hình được suy ra trực tiếp.")

    elif option == "Tìm đường suy luận":
        st.header("Tìm đường suy luận trong Knowledge Graph")

        shapes = service.get_all_shapes()
        names = [x["tenGoi"] for x in shapes]

        col1, col2 = st.columns(2)

        with col1:
            start = st.selectbox("Hình bắt đầu", names, index=0)

        with col2:
            default_end = names.index("Hình vuông") if "Hình vuông" in names else 0
            end = st.selectbox("Hình cần tìm", names, index=default_end)

        if st.button("🔎 Tìm đường"):
            paths = service.find_paths(start, end)

            if paths:
                for i, result in enumerate(paths, start=1):
                    st.markdown(f"### Đường {i}")
                    st.write(" → ".join(result["path"]))

                    for j, prop in enumerate(result["properties"]):
                        st.caption(
                            f"{result['path'][j]} + {prop} "
                            f"→ {result['path'][j + 1]}"
                        )
            else:
                st.warning(
                    f"Không tìm thấy đường từ {start} đến {end}."
                )

    elif option == "Tìm kiếm kiến thức":
        st.header("Tìm kiếm kiến thức hình học")

        keyword = st.text_input(
            "Nhập từ khóa",
            placeholder="Ví dụ: vuông, song song, đường chéo..."
        )

        if keyword:
            results = service.search_shapes(keyword)

            if results:
                for item in results:
                    with st.expander(item["tenGoi"]):
                        st.markdown("**Tính chất:**")
                        st.write(item["tinhChat"])

                        st.markdown("**Nhận biết:**")
                        st.write(item["nhanBiet"])
            else:
                st.warning("Không tìm thấy kết quả.")

    elif option == "Quan hệ trong Graph":
        st.header("Các quan hệ trong Knowledge Graph")

        relations = service.get_graph()

        st.dataframe(
            [
                {
                    "Hình ban đầu": x["fromShape"],
                    "Tính chất thêm": x["relation"],
                    "Hình suy ra": x["toShape"]
                }
                for x in relations
                if x["relation"] is not None
            ],
            use_container_width=True,
            hide_index=True
        )

        st.markdown("---")
        st.markdown("### Mô hình quan hệ")

        st.code(
                        """Hình A
            │
            │ + tính chất
            ▼
            Hình B""",
                        language="text"
                    )
    elif option == "Đồ thị Knowledge Graph":

        st.header("🕸️ Knowledge Graph - Tứ giác")

        st.write(
            "Đồ thị biểu diễn mối quan hệ giữa các hình tứ giác "
            "và tính chất được bổ sung để suy ra hình mới."
        )

        net = create_graph(service)

        graph_html = net.generate_html()

        components.html(
            graph_html,
            height=700,
            scrolling=True
        )


if __name__ == "__main__":
    main()
