# Money Manager
Money Manager to aplikacja webowa, która pomaga użytkownikom nadzorować miesięczny budżet oraz zarządzać wydatkami i oszczędnościami w różnych walutach.

## Funkcjonalności
* **Rejestracja i logowanie:** Użytkownicy mogą zarejestrować się, zalogować oraz zresetować hasło przez email.
* **Zarządzanie wydatkami:** W zakładce "Expenses" można dodawać wydatki (rachunki, codzienne zakupy, wydatki losowe) oraz importować wydatki z pliku CSV.
* **Zarządzanie kontem:** W zakładce "Account" można dodawać wpływy na konto (np. wypłata), przeglądać wpływy z danego miesiąca oraz sprawdzać zaktualizowany bilans.
* **Miesięczny przegląd finansowy:** Zakładka "Manager" pozwala sprawdzić miesięczne wydatki i przychody, generować raporty w formacie PDF lub CSV oraz ocenić, czy użytkownik jest "na plusie" lub "na minusie".
* **Skarbonka:** Zakładka "Money Box" umożliwia użytkownikowi ustalanie celu oszczędnościowego, dokonywanie wpłat oraz śledzenie postępu procentowego w realizacji celu.
* Aplikacja obsługuje trzy waluty i dynamicznie aktualizuje bilans po każdej operacji, korzystając z API do przeliczania walut.

## Technologie
* **Backend:** Python, Django
* **Frontend:** HTML
* **Bazy danych:** PostgreSQL
* **Testowanie:** pytest, unittest.mock
* **Konteneryzacja:** Docker
* **CI/CD:** Github Actions
* **Hosting:** AWS EC2
* **API:** ExchangeRate-API (przeliczanie walut)

## Instalacja
1. Sklonuj repozytorium:
   ```bash
   git clone https://github.com/Bergu1/money-manager-first-project.git
   ```
2. Przejdź do katalogu:
   ```bash
   cd money-manager-first-project
   ```
3. Przejdź do katalogu:
   ```bash
   docker-compose up --build
   ```
4. Aplikacja będzie dostępna pod adresem: http://localhost:8000

## Użycie
1. Zarejestruj się lub zaloguj do aplikacji.
2. Przejdź do zakładki Expenses, aby dodać wydatki lub zaimportować je z pliku CSV.
3. W zakładce Account możesz dodać środki na swoje konto i śledzić swój bilans.
4. Skorzystaj z zakładki Manager, aby śledzić swoją sytuacje finansową oraz wygenerować raporty finansowe z danego miesiąca.
5. W zakładce Money Box ustaw swój cel oszczędnościowy i wpłacaj środki, aby go zrealizować.

## Live Demo 
Aplikację można zobaczyć na żywo pod tym linkiem:
[Money Manager - Live Demo](http://ec2-13-60-82-173.eu-north-1.compute.amazonaws.com/login/)

## Autorzy 
* Konrad Landzberg 
