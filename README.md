# Projekt: Dateisuche und Statistik mit Python und SQL

## 🎓 Projektbeschreibung
Dieses Projekt wurde im Rahmen des Abschlussmoduls der Programmierschule **ICH** entwickelt (Modul: Python und SQL).

Ziel des Projekts ist es, eine Anwendung zu erstellen, die:
- nach Dateien anhand von Parametern sucht,
- grundlegende Statistiken über die gefundenen Daten liefert,
- die Verbindung zu einer Datenbank herstellt und Protokolle speichert.

## 🔄 Hauptdatei
Die Hauptlogik und Ausführung befindet sich in:

```
DIL_Final_main.ipynb
```

Diese Datei führt alle Module zusammen und ermöglicht die Interaktion mit der Benutzeroberfläche (z. B. Eingabe von Suchparametern).

## 📂 Projektstruktur
| Datei | Beschreibung |
|-------|--------------|
| `DIL_Final_main.ipynb` | Haupt-Notebook für das Projekt |
| `search.py` | Enthält die Suchlogik und Dateifilterung |
| `utils.py` | Hilfsfunktionen zur Datenverarbeitung |
| `logger.py` | Logging-Mechanismus zur Nachverfolgung |
| `db_main_config.py` | Konfigurationsdatei für Hauptdatenbank (Passwort/Name hier anpassbar) |
| `db_log_config.py` | Konfigurationsdatei für Log-Datenbank |

## 🔐 Datenbankverbindung
Das Projekt stellt eine Verbindung zu einer oder mehreren Datenbanken her. Die Zugangsdaten (z. B. Passwort und Datenbankname) können in folgenden Dateien angepasst werden:

- `db_main_config.py`
- `db_log_config.py`

## 📅 Autor & Lizenz
Dieses Projekt wurde im Rahmen des Kurses an der ICH-Schule erstellt.

> Nur zu Schulungszwecken. Keine kommerzielle Nutzung.
