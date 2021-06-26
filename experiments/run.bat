for /l %%n in (1,1,30) do (
    start python run_server.py -p 8020 -c 2 -r 2 -o score_log.txt
    start python run_client.py -a r -p 8020
    python run_client.py -a m -p 8020
)