for /l %%n in (1,1,1) do (
    start cmd /k python run_server.py -p 8020 -c 3 -r 3 -o score_log.txt
    start python run_client.py -a r -p 8020
    start python run_client.py -a r -p 8020
)