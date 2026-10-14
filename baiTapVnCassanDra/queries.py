import os
from dotenv import load_dotenv
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from uuid import UUID

# Đọc biến môi trường từ file .env
load_dotenv()


class CassandraQueries:
    """Lớp chứa toàn bộ truy vấn Cassandra, tách riêng khỏi giao diện."""

    def __init__(self):
        cloud_config = {
            "secure_connect_bundle": os.getenv("ASTRA_DB_SECURE_BUNDLE_PATH")
        }

        token = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
        keyspace = os.getenv("ASTRA_DB_KEYSPACE")

        if not cloud_config["secure_connect_bundle"]:
            raise ValueError("Thiếu ASTRA_DB_SECURE_BUNDLE_PATH trong .env")

        if not token:
            raise ValueError("Thiếu ASTRA_DB_APPLICATION_TOKEN trong .env")

        if not keyspace:
            raise ValueError("Thiếu ASTRA_DB_KEYSPACE trong .env")

        self.auth_provider = PlainTextAuthProvider("token", token)
        self.cluster = Cluster(
            cloud=cloud_config,
            auth_provider=self.auth_provider
        )
        self.session = self.cluster.connect(keyspace)

    # Q1 — Thông tin chi tiết một khách sạn
    def get_hotel(self, hotel_id):
        query = """
            SELECT *
            FROM hotels
            WHERE hotel_id = %s
        """
        return list(self.session.execute(query, (hotel_id,)))

    # Q2 — Danh sách phòng của một khách sạn
    def get_rooms(self, hotel_id, available_only=False):
        if available_only:
            query = """
                SELECT room_number, room_type, price_per_night, status
                FROM rooms_by_hotel
                WHERE hotel_id = %s
                  AND status = 'AVAILABLE'
                ALLOW FILTERING
            """
        else:
            query = """
                SELECT room_number, room_type, price_per_night, status
                FROM rooms_by_hotel
                WHERE hotel_id = %s
            """

        return list(self.session.execute(query, (hotel_id,)))

    # Q3 — Lịch sử đặt phòng của khách hàng
    def get_guest_bookings(self, guest_id):
        query = """
            SELECT check_in_date, hotel_name, room_number,
                   check_out, total_amount, status
            FROM booking_by_guest
            WHERE guest_id = %s
        """
        return list(self.session.execute(query, (guest_id,)))

    # Q4 — Đặt phòng của khách sạn trong khoảng ngày
    def get_hotel_bookings_by_date(self, hotel_id, start_date, end_date):
        query = """
            SELECT check_in_date, room_number, guest_name,
                   check_out_date, status
            FROM booking_by_hotel_date
            WHERE hotel_id = %s
              AND check_in_date >= %s
              AND check_in_date <= %s
        """
        return list(
            self.session.execute(
                query,
                (hotel_id, start_date, end_date)
            )
        )

    # Q5 — Tra cứu hóa đơn theo mã đặt phòng
    def get_invoice_by_booking(self, booking_id):
        try:
            booking_uuid = UUID(booking_id)
        except ValueError:
            raise ValueError("Mã booking phải là UUID hợp lệ.")

        query = """
            SELECT *
            FROM invoices_by_booking
            WHERE booking_id = %s
        """
        return list(self.session.execute(query, (booking_uuid,)))

    # Thống kê — COUNT, MAX, MIN
    def get_room_statistics(self, hotel_id):
        count_query = """
            SELECT COUNT(*)
            FROM rooms_by_hotel
            WHERE hotel_id = %s
        """

        price_query = """
            SELECT MAX(price_per_night), MIN(price_per_night)
            FROM rooms_by_hotel
            WHERE hotel_id = %s
        """

        count_row = self.session.execute(
            count_query, (hotel_id,)
        ).one()

        price_row = self.session.execute(
            price_query, (hotel_id,)
        ).one()

        return {
            "room_count": count_row.count,
            "max_price": price_row.system_max_price_per_night,
            "min_price": price_row.system_min_price_per_night,
        }

    def close(self):
        self.cluster.shutdown()
