import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from src.spcs_instruments.instruments.test_instrument import Fake_daq
from src.spcs_instruments.spcs_instruments_utils import Experiment

file_name = ".exp_output.log"
def test_fake_experiment():
    def a_measurement(config) -> dict:
        daq = Fake_daq(config)
        for i in range(5):
            val = daq.measure()
            print(val)

        data = {daq.name: daq.data}
        return data

    dir_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(dir_path, "..", "templates", "config1.toml")
    config_path = os.path.abspath(config_path)

    experiment = Experiment(a_measurement, config_path)
    experiment.start()

    with open(file_name, "r") as f:
        log_contents = f.read()
    assert "[experiment]" in log_contents
    assert "start_time" in log_contents
    assert "[device.Test_DAQ.data]" in log_contents
    assert "current =" in log_contents


    try:
        os.remove(file_name)
        print(f"File '{file_name}' deleted successfully")
    except FileNotFoundError:
        print(f"File '{file_name}' not found")
    except Exception as e:
        print(f"Failed to delete file '{file_name}': {e}")


def test_fake_experiment_2devices():
    
    def a_measurement(config) -> dict:
        # Initialize both DAQ devices with their respective configurations
        daq1 = Fake_daq(config, name="Test_DAQ_1")
        daq2 = Fake_daq(config, name="Test_DAQ_2")

        for i in range(5):
            daq1.measure()
            daq2.measure()

        # Collect the data from both devices
        data = {
            daq1.name: daq1.data,
            daq2.name: daq2.data
        }

        return data
    
    dir_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(dir_path, "..", "templates", "config2.toml")
    config_path = os.path.abspath(config_path)   
    experiment = Experiment(a_measurement, config_path)
    experiment.start()


    
    with open(file_name, "r") as f:
        log_contents = f.read()
    assert "[experiment]" in log_contents
    assert "start_time" in log_contents
    assert "[device.Test_DAQ_1.data]" in log_contents
    
    assert "[device.Test_DAQ_2.data]" in log_contents
    assert "current =" in log_contents

    try:
        os.remove(file_name)
        print(f"File '{file_name}' deleted successfully")
    except FileNotFoundError:
        print(f"File '{file_name}' not found")
    except Exception as e:
        print(f"Failed to delete file '{file_name}': {e}")
