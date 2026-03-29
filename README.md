# Ramdisk Manager v1.0 by d3xt3rr0r

![Ramdisk Manager](assets/icon.png)

Ramdisk Manager to prosty i wydajny menedżer RAMdisków dla Linuxa z CLI i GUI.  
Pozwala tworzyć tymczasowe dyski w RAM, synchronizować dane i zarządzać nimi wygodnie z poziomu graficznego interfejsu lub terminala.

---

## Funkcje

- Tworzenie i usuwanie RAMdisków o wybranym rozmiarze (GB)
- Synchronizacja danych między RAMdisk a katalogiem trwałym (`RAMdisk_data`)
- GUI do kontroli stanu RAMdisk i logów synchronizacji
- Autosynchronizacja w GUI
- Prosty interfejs CLI z obsługą parametrów

---

## Wymagania

- Linux
- Python 3.8+  
- PySide6 (`pip install PySide6`)

---

## Instalacja

1. Sklonuj repozytorium:

git clone https://github.com/d3xt3rr0r/ramdisk-manager.git
cd ramdisk-manager

2. Nadaj uprawnienia do skryptu uruchamiającego:

chmod +x run.sh

3. (Opcjonalnie) Dodaj do PATH, żeby uruchamiać z dowolnego miejsca:

ln -s $(pwd)/run.sh ~/.local/bin/ramdisk-manager

4. Użycie CLI:

ramdisk-manager start [sizeGB]    # tworzy RAMdisk o podanym rozmiarze
ramdisk-manager stop              # synchronizuje dane i usuwa RAMdisk
ramdisk-manager sync              # synchronizacja RAMdisk -> RAMdisk_data
ramdisk-manager gui               # uruchamia GUI

5. Użycie GUI:

ramdisk-manager gui

W GUI możesz:

Ustawić rozmiar RAMdisk (GB)
Ustawić interwał autosynchronizacji (minuty)
Włączyć/wyłączyć RAMdisk
Synchronizować dane ręcznie
Śledzić logi i status RAMdisk

6. Struktura projektu:

ramdisk-manager/
├── ramdisk.py       # główny skrypt CLI
├── gui.py           # GUI
├── run.sh           # wrapper CLI
├── config.json      # przykładowy config
├── README.md        # dokumentacja
├── LICENSE          # licencja MIT
└── assets/
    └── icon.png     # ikona projektu

7. Uwagi:

Autosynchronizacja działa tylko w GUI.
CLI przyjmuje parametr rozmiaru RAMdisk (start [sizeGB]), jeśli nie zostanie podany, używa wartości z config.json.
