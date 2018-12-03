import pytest
from process_sensor import ProcessSensor
from mock import Mock, patch
from datetime import datetime

def test_input():
    sensor = ProcessSensor(1, 1, "log.txt")
    assert sensor.seconds == 1 * 24 * 60 * 60
    assert sensor.iterations == 1 * 24 * 60 * 60 / 1

def test_get_added_pid_empty_past_list():
    sensor = ProcessSensor(1, 1, "log.txt")
    sensor.past_list = []
    cur_list = ["1", "2", "3"]
    res = sensor.get_added_pid(cur_list)
    assert res == ["1", "2", "3"]

def test_get_added_pid_not_empty_past_list():
    sensor = ProcessSensor(1, 1, "log.txt")
    sensor.past_list = ["1", "2"]
    cur_list = ["2", "3"]
    res = sensor.get_added_pid(cur_list)
    assert res == ["3"]

def test_get_removed_pid():
    sensor = ProcessSensor(1, 1, "log.txt")
    sensor.past_list = ["1", "2"]
    cur_list = ["2", "3"]
    res = sensor.get_removed_pid(cur_list)
    assert res == ["1"]

def test_update_store(mocker):
    sensor = ProcessSensor(1, 1, "log.txt")
    sensor.store = {}
    proc = Mock(info = {'ppid': 1, 'create_time': 1541544443.585618, 'pid': 1011, 'exe': '/Mockexe'})
    mocker.patch('psutil.process_iter', return_value = [proc])
    sensor.update_store()
    assert sensor.store == {1011: {'ppid': 1, 'create_time': 1541544443.585618, 'exe': '/Mockexe'}}

def test_generateLogTuples():
    with patch.object(ProcessSensor, "getTime") as getTime_mocked:
        getTime_mocked.return_value = 'Mocktime'
        sensor = ProcessSensor(1, 1, "log.txt")
        sensor.store = {1011: {'ppid': 1, 'create_time': 1541544443.585618, 'exe': '/Mockexe'}}
        # mocker.patch('process_sensor.getTime', return_value = "Mocktime")
        generated = sensor.generateLogTuples([1011], True)
        assert generated == [('Mocktime', 'process', 'create', '/Mockexe')]
