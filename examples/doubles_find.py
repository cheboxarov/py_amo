import time


async def find_doubles_by_phone_number(session):
    accounts_count = await session.contacts.count()
    accounts = await session.contacts.get_all(limit=accounts_count)
    phones: dict[str, list] = {}
    for account in accounts:
        try:
            for cf in account.custom_fields_values:
                if cf.field_name == "Телефон":
                    phone = cf.values[0].value
                    phone = (
                        phone.replace("+", "")
                        .replace("-", "")
                        .replace(" ", "")
                        .replace("(", "")
                        .replace(")", "")[1:]
                    )
                    if phones.get(phone) is None:
                        phones[phone] = [account]
                    else:
                        phones[phone].append(account)
        except:
            pass
    doubles = {}
    for phone, accounts in phones.items():
        if len(accounts) > 1:
            doubles[phone] = accounts
    return doubles
