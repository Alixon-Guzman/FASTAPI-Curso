class TestAuthAcademiaMusica:

    def test_register_and_login(self, client):
        data = {"username": "user_music_test", "password": "User123!", "role": "instructor"}
        r = client.post("/auth/register", json=data)
        assert r.status_code == 201

        login = client.post("/auth/login", data={"username": data["username"], "password": data["password"]})
        assert login.status_code == 200
        assert "access_token" in login.json()

    def test_only_admin_can_delete_clase(self, client, sample_clase_data):
        client.post("/auth/register", json={"username": "admin_del_test", "password": "Admin123!", "role": "admin_academia"})
        admin_login = client.post("/auth/login", data={"username": "admin_del_test", "password": "Admin123!"})
        admin_token = admin_login.json().get("access_token")
        admin_headers = {"Authorization": f"Bearer {admin_token}"}

        client.post("/auth/register", json={"username": "user_nopriv", "password": "User123!", "role": "estudiante"})
        user_login = client.post("/auth/login", data={"username": "user_nopriv", "password": "User123!"})
        user_token = user_login.json().get("access_token")
        user_headers = {"Authorization": f"Bearer {user_token}"}

        create = client.post("/music/clases/", json=sample_clase_data, headers=admin_headers)
        clase_id = create.json()["id"]

        res_user_delete = client.delete(f"/music/clases/{clase_id}", headers=user_headers)
        assert res_user_delete.status_code in (401, 403)

        res_admin_delete = client.delete(f"/music/clases/{clase_id}", headers=admin_headers)
        assert res_admin_delete.status_code == 200
