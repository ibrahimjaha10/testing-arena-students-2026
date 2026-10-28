# Testplan 

## 1. parse_time
- Normale Zeiten wie 12:00
- Zeiten, die nicht gehen: 24:00, 12:60 (zu hoch) oder -1:00 (negativ)
- Quatsch-Eingaben wie "12" ohne Doppelpunkt oder Buchstaben

## 2. parse_measurement
- Leerzeichen vor und nach der Stadt/Uhrzeit (schauen ob strip klappt)
- Falsche Formate (z.B. nur zwei Spalten oder Stadt fehlt ganz)
- Falscher Datentyp (Zahl statt String)

## 3. filter_by_temperature
- Was passiert, wenn die Temperatur genau dem Grenzwert entspricht? (sollte im Ergebnis bleiben)
- Falsche Parameter (lower ist größer als upper)

## 4. average_temperature
- Normaler Durchschnitt
- Wenn die Stadt gar nicht in der Liste ist (darf nicht durch 0 teilen)

## 5. hottest_measurement
- Wenn zwei Städte genau gleich warm sind, muss die frühere Uhrzeit gewinnen.
- Leere Liste abfangen