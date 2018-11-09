import pytest
from process_sensor import ProcessSensor
# import mock 
from mock import Mock

def test_default_init_list():
    sensor = ProcessSensor()
    assert sensor.past_list == []

def test_get_added_pid_empty_past_list():
    sensor = ProcessSensor()
    cur_list = ["1", "2", "3"]
    res = sensor.get_added_pid(cur_list)
    assert res == ["1", "2", "3"]

def test_get_added_pid_not_empty_past_list():
    sensor = ProcessSensor()
    sensor.past_list = ["1", "2"]
    cur_list = ["2", "3"]
    res = sensor.get_added_pid(cur_list)
    assert res == ["3"]

def test_get_removed_pid():
    sensor = ProcessSensor()
    sensor.past_list = ["1", "2"]
    cur_list = ["2", "3"]
    res = sensor.get_removed_pid(cur_list)
    assert res == ["1"]

def test_generate_store(mocker):
    proc = Mock(info = {'ppid': 1, 'create_time': 1541544443.585618, 'pid': 1011, 'exe': '/Library/Input Methods/SogouInput.app/Contents/SogouServices'})
    mocker.patch('psutil.process_iter', return_value = [proc])
    sensor = ProcessSensor()
    store = sensor.generate_store()
    assert store == {1011: {'ppid': 1, 'create_time': 1541544443.585618, 'exe': '/Library/Input Methods/SogouInput.app/Contents/SogouServices'}}
