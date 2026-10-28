# Spezifikation: Weather Utilities

Dieses Dokument beschreibt das **erwartete Verhalten** von `weather.py`.
Die Aufgabe im Praktikum besteht nicht darin, die Implementierung umzuschreiben,
sondern eine Testsuite zu entwickeln, die überprüft, ob eine Implementierung diese
Spezifikation tatsächlich erfüllt.

Wenn hier nichts anderes steht, dürfen Sie davon ausgehen, dass Argumente den in den
Beispielen gezeigten Grundtyp besitzen. Es geht in diesem Praktikum nicht darum,
für jede denkbare falsche Python-Datenstruktur defensive Prüfungen zu ergänzen.

## Datenmodell

Eine bereits eingelesene Wettermessung wird als Tupel dargestellt:

```python
(city, time, temperature)
```

Beispiel:

```python
("Köln", 861, 21.7)
```

Dabei gilt:

- `city` ist ein String.
- `time` ist die Anzahl der Minuten seit Mitternacht.
- `temperature` ist die Temperatur in Grad Celsius als `float`.

Die Reihenfolge von Messungen ist grundsätzlich relevant und darf von den Funktionen
nicht ohne ausdrückliche Anforderung verändert werden.

---

## `parse_time(time_text)`

Konvertiert eine Uhrzeit mit einem Doppelpunkt in Minuten seit Mitternacht.

```python
parse_time("14:21") == 861
parse_time("00:00") == 0
parse_time("23:59") == 1439
```

### Vertrag

- Der Text muss aus **zwei numerischen Bestandteilen** bestehen, getrennt durch genau
  einen Doppelpunkt `:`.
- Führende Nullen sind optional. Beispielsweise sind `"9:05"`, `"09:05"` und
  `"9:5"` gültige Schreibweisen.
- Die Stunde muss zwischen **0 und 23 einschließlich** liegen.
- Die Minute muss zwischen **0 und 59 einschließlich** liegen.
- Bei ungültigem Format, nicht-numerischen Bestandteilen oder ungültigen Werten wird
  `ValueError` ausgelöst.

---

## `parse_measurement(line)`

Liest genau eine Wetter-Messung im Format

```text
Stadt;Uhrzeit;Temperatur
```

Beispiel:

```python
parse_measurement("Köln;14:21;21.7")
# ("Köln", 861, 21.7)
```

### Vertrag

- `line` muss ein String sein. Für einen anderen Typ wird `ValueError` ausgelöst.
- Die Zeile muss aus **genau drei** durch `;` getrennten Feldern bestehen.
- Führende und nachfolgende Leerzeichen der drei Felder werden entfernt.
- Der Stadtname darf nach dem Entfernen von Leerzeichen nicht leer sein.
- Die Uhrzeit wird nach den Regeln von `parse_time()` verarbeitet.
- Die Temperatur wird mit `float(...)` in eine Fließkommazahl umgewandelt.
- Kann die Temperatur nicht als `float` interpretiert werden, wird `ValueError`
  ausgelöst.
- Es findet keine zusätzliche meteorologische Plausibilitätsprüfung der Temperatur
  statt.

Beispiel mit zusätzlichem Whitespace:

```python
parse_measurement(" Köln ; 14:21 ; 21.7 ")
# ("Köln", 861, 21.7)
```

---

## `filter_by_temperature(measurements, lower, upper)`

Gibt alle Messungen zurück, deren Temperatur im gewünschten Bereich liegt.

### Vertrag

- Die Grenzen sind **inklusive**: `lower <= temperature <= upper`.
- Die Reihenfolge der Messungen bleibt erhalten.
- Doppelte bzw. identische Messungen bleiben doppelt vorhanden.
- Die übergebene Liste wird nicht verändert.
- Ist `lower > upper`, wird `ValueError` ausgelöst.
- Das Ergebnis ist eine neue Liste.

---

## `average_temperature(measurements, city)`

Berechnet die mittlere Temperatur aller Messungen einer Stadt.

### Vertrag

- Es werden ausschließlich Messungen berücksichtigt, deren Stadtname exakt `city`
  entspricht.
- Städtenamen werden **case-sensitive** verglichen. `"Köln"` und `"köln"` sind also
  unterschiedliche Namen.
- Der Mittelwert wird über alle passenden Messungen gebildet.
- Gibt es keine Messung für die angegebene Stadt, wird `ValueError` ausgelöst.
- Die Eingabedaten werden nicht verändert.

---

## `hottest_measurement(measurements)`

Gibt die Messung mit der höchsten Temperatur zurück.

### Vertrag

- Gibt es nur eine eindeutige höchste Temperatur, wird diese Messung zurückgegeben.
- Haben mehrere Messungen dieselbe höchste Temperatur, wird die Messung mit der
  **frühesten Uhrzeit** zurückgegeben.
- Haben mehrere Messungen sowohl dieselbe höchste Temperatur als auch dieselbe
  Uhrzeit, bleibt die zuerst vorkommende dieser Messungen maßgeblich.
- Für eine leere Sequenz wird `ValueError` ausgelöst.
- Die Eingabedaten werden nicht verändert.
