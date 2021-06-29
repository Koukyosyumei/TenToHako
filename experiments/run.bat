for /l %%n in (1,1,1) do (
    start cmd /k python run_server.py -p 8020 -c 3 -r 3 --lo score_log.txt --go result.gif
    start python run_client.py -a r -p 8020
    start python run_client.py -a r -p 8020
)