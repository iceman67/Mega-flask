import time
import glob

class DS1820:
    device_file = []
    num_devices = 0
    temp_str_list = []
    device_folder_ds18s20 = []
    device_folder_ds18b20 = []
    device_folder_MAX31850K = []

    def __init__(self, base_dir='/sys/bus/w1/devices/'):
        self.base_dir = base_dir

        print ("base_dir={}".format(base_dir))
        DS1820.device_folder_ds18s20 = glob.glob(base_dir + '10*')
        DS1820.device_folder_ds18b20 = glob.glob(base_dir + '28*')
        DS1820.device_folder_MAX31850K = glob.glob(base_dir + '3b*')
        self.append_device_family(DS1820.device_folder_ds18s20)
        self.append_device_family(DS1820.device_folder_ds18b20)
        self.append_device_family(DS1820.device_folder_MAX31850K)

    def get_num_devices(self):
        # DS1820.num_devices = len(DS1820.device_file)
        DS1820.num_devices = len(DS1820.device_file)
        return DS1820.num_devices

    @staticmethod
    def append_device_family(family_name):
        for dev_f in family_name:
            DS1820.device_file.append(dev_f + '/w1_slave')

    def read_temp_raw(self, df):
        # lines = []
        f = open(df, 'r')
        lines = f.readlines()
        #lines += l
        f.close()
        return lines

    def reset_temp_list(self):
        DS1820.temp_str_list = []

    def get_temp_list(self):
        return DS1820.temp_str_list

    def get_celcius_temp(self, temp_str):
        temp_c = float(temp_str) / 1000.0
        return temp_c

    def read_temp_str(self, df):
        lines = self.read_temp_raw(df)
        # get a temperature when a condition is YES
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_temp_raw(df)  # read a temperature from a file with df
        temp_output_status = lines[1].find('t=')
        if temp_output_status != -1:
            # temperature string
            temperature_value_string = lines[1].strip()[temp_output_status + 2:]

            # [N/A]self.add_temp_to_list(temperature_value_string)
            # replace it with the following
            # build a temp_str_ist from  a  temperature converted with float type
            DS1820.temp_str_list.append(self.get_celcius_temp(temperature_value_string))
        return temperature_value_string

    """
    # [N/A] append a temperature to  DS1820.temp_str_list
    def add_temp_to_list(self, temp_string):
        DS1820.temp_str_list.append(self.get_celcius_temp(temp_string))

    def read_temp(self, temp_string):
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f
    """


if __name__ == "__main__":
    import re

    temperature_dev = DS1820()
    print("# of devices : {}".format(temperature_dev.get_num_devices()))
    length = '0' + str(temperature_dev.get_num_devices())
    time.sleep(2)

    device_map = dict() 
    while True:
        for df in temperature_dev.device_file:
            temp_str = temperature_dev.read_temp_str(df)
            fileList = df.split('/')
            device_map[fileList[5]] = temperature_dev.get_celcius_temp(temp_str)
             
        collected = temperature_dev.get_temp_list()
        # build a temperature string
        temp_string = ','.join(map(str, collected))

        for k, v in device_map.items():
           print("({0}, {1})".format(k, v))

        
        # reset the collected temperature list
        temperature_dev.reset_temp_list()
        time.sleep(1)
