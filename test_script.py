# This example show how to execute a command concurrently in the devices
# Using multithreads

# Change import settings
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)


def send_command(dev: dict, cmd_list: list) -> dict:
    """
    Send command to device using Netmiko
    :param dev: device info
    :param cmd: command to execute
    :return: Command output from device
    """
    # remove key hostname from dictionary since it is not expected/valid for netmiko

    try:
        # Use context manager to open and close the SSH session
        out_dict = dict()
        with ConnectHandler(**dev) as ssh:
            ssh.enable()
            status = "Success"
            for index, cmd in enumerate(cmd_list):
                output = ssh.send_command(cmd)
                tempkey = "cmd" + str(index + 1)
                out_dict[tempkey] = output

    except (NetmikoTimeoutException, NetmikoAuthenticationException):
        output = "Connection to device failed"
        status = "Failed:" + output
        # print(output)

    finally:
        out_dict = {"device": (dev["ip"]), "status": status, "result": out_dict}

    return out_dict


def netmiko_executor(credentials: dict, raw_data: list) -> list:
    try:
        response_list = []
        # loop to run command in context manager. Using 6 as max Threads to start and wait
        with ThreadPoolExecutor(max_workers=6) as executor:
            future_list = []
            for ip in raw_data[1]:
                # update the device dictionary with the credentials and send command
                device = {"ip": ip, "device_type": raw_data[0]}
                device.update(credentials)
                print(device)
                # Add the task to the pool of threads and run
                future = executor.submit(send_command, device, raw_data[2])
                future_list.append(future)
            # force to wait until the future_list has been executed
            for f in as_completed(future_list):
                # print(f.result())
                response_list.append(f.result())
            return response_list
        # Get and print finishing time

    except Exception as err:
        print(err)


if __name__ == "__main__":
    execution_start_timer = time.perf_counter()
    credentials = {"username": "test", "password": "test"}
    raw_data = [
        "cisco_xr",
        ["172.30.1.100", "172.30.1.103"],
        ["sh version", "sh ip interface brief"],
    ]
    elapsed_time = time.perf_counter() - execution_start_timer
    print(elapsed_time)

    output = netmiko_executor(credentials, raw_data)
    print(output)
    # print(type(output))
