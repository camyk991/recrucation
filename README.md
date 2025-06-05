# Projekt Rekrutacja Django

## Opis
Prosty system rekrutacyjny Django z backendem i frontendem na bazie klasycznych widoków i szablonów Django.  
Baza danych: MySQL.

## Konfiguracja MySQL
1. Zainstaluj MySQL (np. na Ubuntu: `sudo apt install mysql-server`)
2. Utwórz bazę danych i użytkownika:

```sql
CREATE DATABASE rekrutacja_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'dbuser'@'localhost' IDENTIFIED BY 'dbpassword';
GRANT ALL PRIVILEGES ON rekrutacja_db.* TO 'dbuser'@'localhost';
FLUSH PRIVILEGES;
```

## Instalacja i uruchomienie
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Funkcjonalności
- Logowanie / wylogowanie
- Zarządzanie kandydatami (lista, szczegóły, dodawanie)
- Modele zgodne z projektem bazy danych
- Prosta kontrola dostępu (logowanie wymagane)

---

Kod jest w katalogach:

- `rekrutacja_project/` - konfiguracja Django  
- `recruitment_app/` - aplikacja z modelami, widokami, szablonami  
- `templates/` - szablony HTML  
- `static/` - pliki statyczne

---

## Rozwój
Można rozszerzyć o: upload dokumentów, archiwizację, raporty PDF, API REST itp.
