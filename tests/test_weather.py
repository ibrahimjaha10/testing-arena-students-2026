import pytest
from weather import (
    parse_time,
    parse_measurement,
    filter_by_temperature,
    average_temperature,
    hottest_measurement,
)

# parse_time
def test_parse_time_normal():
    assert parse_time("00:00") == 0
    assert parse_time("23:59") == 1439
    assert parse_time("12:00") == 720

def test_parse_time_leading_zeros():
    # auch einstellige zahlen sind ok
    assert parse_time("9:5") == 545
    assert parse_time("09:05") == 545

@pytest.mark.parametrize("invalid_time", [
    "24:00", "12:60", "-1:00", "12:-1", "12", "12:30:15", "ab:cd"
])
def test_parse_time_errors(invalid_time):
    # check auf value errors bei falschem format
    with pytest.raises(ValueError):
        parse_time(invalid_time)

# parse_measurement
def test_parse_measurement_spaces():
    # leerzeichen sollen ignoriert werden
    city, time, temp = parse_measurement("  Düsseldorf  ;  09:05  ;  18.3  ")
    assert city == "Düsseldorf"
    assert time == 545
    assert temp == 18.3

def test_parse_measurement_negative_temp():
    # minusgrade müssen klappen
    city, time, temp = parse_measurement("Berlin;12:00;-5.5")
    assert temp == -5.5

def test_parse_measurement_bad_input():
    with pytest.raises(ValueError):
        parse_measurement(123) 
    with pytest.raises(ValueError):
        parse_measurement("Köln;14:21")  # feld fehlt
    with pytest.raises(ValueError):
        parse_measurement(" ;14:21;21.7")  # stadt leer
    with pytest.raises(ValueError):
        parse_measurement("Köln;14:21;kalt")  # falscher typ

# filter_by_temperature
def test_filter_by_temperature_exact_limits():
    # grenzen sind inklusiv
    measurements = [
        ("A", 100, 10.0), ("B", 200, 15.0), ("C", 300, 20.0)
    ]
    res = filter_by_temperature(measurements, 10.0, 20.0)
    assert len(res) == 3

def test_filter_by_temperature_wrong_params():
    # fehler wenn lower > upper
    with pytest.raises(ValueError):
        filter_by_temperature([], 20.0, 10.0)

def test_filter_by_temperature_duplicates():
    # doppelte einträge müssen doppelt im ergebnis bleiben
    m = [("Köln", 100, 15.0), ("Köln", 100, 15.0)]
    res = filter_by_temperature(m, 10.0, 20.0)
    assert len(res) == 2

def test_filter_exact_same_limits():
    # filter mit identischer unter- und obergrenze (lower == upper)
    m = [("A", 100, 15.0), ("B", 200, 20.0)]
    res = filter_by_temperature(m, 15.0, 15.0)
    assert len(res) == 1
    assert res[0] == ("A", 100, 15.0)

# average_temperature
def test_average_temperature_calc():
    m = [("Köln", 100, 10.0), ("Köln", 200, 20.0), ("Bonn", 300, 50.0)]
    assert average_temperature(m, "Köln") == 15.0

def test_average_temperature_case_sensitive():
    # groß und kleinschreibung ist wichtig
    m = [("Köln", 100, 10.0), ("köln", 200, 20.0)]
    assert average_temperature(m, "Köln") == 10.0

def test_average_temperature_missing_city():
    with pytest.raises(ValueError):
        average_temperature([("Bonn", 100, 10.0)], "Köln")

# hottest_measurement
def test_hottest_measurement_normal():
    m = [("A", 100, 10.0), ("B", 200, 20.0)]
    assert hottest_measurement(m) == ("B", 200, 20.0)

def test_hottest_measurement_same_temp():
    # bei gleicher temperatur entscheidet die uhrzeit
    m1 = ("A", 100, 30.0)
    m2 = ("B", 200, 30.0)
    assert hottest_measurement([m1, m2]) == m1
    assert hottest_measurement([m2, m1]) == m1

def test_hottest_measurement_exact_tie():
    # gleiche temp und uhrzeit -> reihenfolge entscheidet
    m1 = ("A", 100, 30.0)
    m2 = ("B", 100, 30.0)
    assert hottest_measurement([m1, m2]) == m1
    assert hottest_measurement([m2, m1]) == m2

def test_hottest_measurement_empty_list():
    with pytest.raises(ValueError):
        hottest_measurement([])

def test_hottest_measurement_all_negative():
    # hitzerekord muss auch mit reinen minusgraden klappen
    m = [("A", 100, -20.0), ("B", 200, -5.0), ("C", 300, -15.0)]
    assert hottest_measurement(m) == ("B", 200, -5.0)

# mutation check und typen-kontrolle
def test_no_mutation_of_input_lists():
    # die liste darf von den funktionen nicht verändert werden
    original_list = [("A", 200, 10.0), ("B", 100, 30.0), ("C", 300, 20.0)]
    list_copy = original_list.copy()
    
    filter_by_temperature(original_list, 0.0, 40.0)
    average_temperature(original_list, "A")
    hottest_measurement(original_list)
    
    assert original_list == list_copy

def test_strict_return_types_and_identities():
    # 1. parse_measurement MUSS zwingend ein Tupel sein (keine Liste!)
    result = parse_measurement("Köln;14:21;21.7")
    assert isinstance(result, tuple)
    
    # 2. filter_by_temperature MUSS zwingend eine Liste sein
    m = [("Köln", 100, 15.0)]
    res = filter_by_temperature(m, 10.0, 20.0)
    assert isinstance(res, list)
    
    # 3. filter_by_temperature muss eine NEUE Liste im Speicher sein (is not)
    assert res is not m