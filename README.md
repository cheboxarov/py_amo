Хорошо, внесу корректировки. Вот обновленный пример документации с учетом использования только `ContactSchema`, `LeadSchema` и других подобных классов для всех операций:

---

# Документация для AmoCRM Python API Библиотеки

## Использованные технологии
- **Python** — язык программирования для написания кода библиотеки.
- **Pydantic** — для строгой валидации данных, получения и обновления сущностей.
- **requests** — для выполнения HTTP-запросов к API AmoCRM.

## Примеры использования

### Начало работы

Перед началом использования библиотеки создайте экземпляр `AmoSession`, указав свой `token` и `subdomain`. Затем можете обращаться к необходимым репозиториям:

```python
from py_amo.session import AmoSession

# Создайте сессию
session = AmoSession(token="ваш_токен", subdomain="ваш_субдомен")
```

### Работа с Контактами

#### Получение списка контактов

Используйте метод `get_all`, чтобы получить список всех контактов. Поддерживается передача параметров для фильтрации:

```python
# Получение контактов с фильтром по лимиту
contacts = session.contacts.get_all(limit=50)
for contact in contacts:
    print(contact.name, contact.id)
```

#### Получение контакта по ID

Чтобы получить определенный контакт по `ID`:

```python
contact = session.contacts.get_by_id(12345)
if contact:
    print(contact.name)
else:
    print("Контакт не найден")
```

#### Создание контактов

Для создания контакта создайте объект `ContactSchema` и передайте его в метод `create`:

```python
from py_amo.schemas import ContactSchema

# Новый контакт
new_contact = ContactSchema(name="Новый клиент")
created_contacts = session.contacts.create([new_contact])
for contact in created_contacts:
    print(contact.id, contact.link)
```

### Работа с Сделками

#### Получение всех сделок

Используйте `session.leads.get_all` для получения списка сделок:

```python
# Получение всех сделок с оффсетом
leads = session.leads.get_all(limit=20, offset=40)
for lead in leads:
    print(lead.name, lead.price)
```

#### Обновление сделки

Для обновления сделки создайте объект `LeadSchema` с нужным ID и обновленными данными, затем вызовите `update`:

```python
from py_amo.schemas import LeadSchema

# Изменение цены сделки
lead = LeadSchema(id=12345, price=10000)
updated_lead = session.leads.update(lead)
print(updated_lead.price)
```

### Работа с воронками и статусами

#### Получение воронок

```python
pipelines = session.pipelines.get_all()
for pipeline in pipelines:
    print(pipeline.name)
```

#### Получение статусов воронки

Для получения статусов конкретной воронки используйте `pipeline_statuses`:

```python
pipeline_statuses = session.pipeline_statuses(pipeline_id=123).get_all()
for status in pipeline_statuses:
    print(status.name, status.color)
```

### Работа с Источниками

#### Получение всех источников

```python
sources = session.sources.get_all()
for source in sources:
    print(source.name, source.origin_code)
```