from flask import Flask, jsonify, request

app = Flask(__name__)

# Contoh data mock
orders = [
    {
        "id": i,
        "pelabuhan_asal": f"Pelabuhan Asal {i}",
        "pelabuhan_tujuan": f"Pelabuhan Tujuan {i}",
        "kelas": "Ekonomi" if i % 2 == 0 else "Bisnis",
        "jenis_pengguna": "Individu" if i % 2 == 0 else "Kelompok",
        "tanggal_checkin": "2025-02-20",
        "jam_checkin": f"{8 + i % 12}:00",
        "tipe_penumpang": "Dewasa" if i % 2 == 0 else "Anak"
    } for i in range(1, 11)
]

@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify(orders)

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = next((order for order in orders if order["id"] == order_id), None)
    if order:
        return jsonify(order)
    return jsonify({"message": "Order not found"}), 404
    

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    new_order = {
        "id": len(orders) + 1,
        "pelabuhan_asal": data.get("pelabuhan_asal"),
        "pelabuhan_tujuan": data.get("pelabuhan_tujuan"),
        "kelas": data.get("kelas"),
        "jenis_pengguna": data.get("jenis_pengguna"),
        "tanggal_checkin": data.get("tanggal_checkin"),
        "jam_checkin": data.get("jam_checkin"),
        "tipe_penumpang": data.get("tipe_penumpang")
    }
    orders.append(new_order)
    return jsonify(new_order), 201


@app.route("/receive", methods=["POST"])
def receive_payload():
    try:
        data = request.get_json(force=True)  # Paksa parsing JSON
        return jsonify({"status": "success", "received": data}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)