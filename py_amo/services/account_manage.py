from py_amo.schemas import AccountShema


class AccountManager:

    def get_me(self):
        params = {"with": "amojo_id"}
        response = self.get_requests_session().get(
            self.get_url() + "/api/v4/account", params=params
        )
        response.raise_for_status()
        data = response.json()
        return AccountShema(**data)
