## **Instrukcja uruchomienia**

Aby uruchomić grę, odpalamy plik game.py - wybieramy opcję New Server, wpisujemy nick (opcjonalnie można zmienić IP) i Start Server. Inni gracze mogą teraz dołączyć do naszej gry łącząc się prze opcję Join Game i wpisując IP.

  
## **Opis**

Gra napisana w języku Python przy użyciu biblioteki *pygame*. Wykorzystuje protokół TCP/IP do komunikacji z serwerem. Kod używa asymetrycznego szyfrowania RSA do bezpiecznej wymiany klucza symetrycznego AES między serwerem a klientem. Następnie wszystkie wiadomości między serwerem a klientem są szyfrowane za pomocą szyfrowania symetrycznego AES.