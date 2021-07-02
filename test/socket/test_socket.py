import subprocess

name = "localhost"
port = 8020
gif_path = "test/socket/test.gif"
log_path = "test/socket/log.txt"

command_client_base = "python test/socket/client_test.py"
command_client_args = f" -n {name} -p {port}"
command_server_base = "python test/socket/server_test.py"
command_server_args = f" -n {name} -p {port} -c 2 -r 2 --gp {gif_path} --lp {log_path}"


def test_socket():
    subprocess.Popen(command_client_base + command_client_args)
    subprocess.Popen(command_client_base + command_client_args)
    subprocess.Popen(command_server_base + command_server_args)
