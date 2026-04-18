def test_create_device(client):
    response = client.post("/devices/", json={"name": "Sensor 1"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Sensor 1"
    assert "id" in data

def test_add_measurement(client):
    # Создаём устройство
    dev_resp = client.post("/devices/", json={"name": "Sensor A"})
    device_id = dev_resp.json()["id"]

    # Добавляем измерение
    payload = {"x": 1.2, "y": -3.4, "z": 5.0}
    resp = client.post(f"/devices/{device_id}/stats", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["x"] == 1.2
    assert data["device_id"] == device_id

def test_analysis(client):
    dev_resp = client.post("/devices/", json={"name": "Sensor B"})
    device_id = dev_resp.json()["id"]
    for v in [1.0, 2.0, 3.0]:
        client.post(f"/devices/{device_id}/stats", json={"x": v, "y": v, "z": v})
    resp = client.get(f"/analysis/devices/{device_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["x"]["min"] == 1.0
    assert data["x"]["max"] == 3.0
    assert data["x"]["median"] == 2.0
    assert data["x"]["count"] == 3