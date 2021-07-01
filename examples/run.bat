for /l %%n in (1,1,10) do (
    start python run_client.py -a m -p 8020
    start python run_client.py -a u -p 8020
    python run_server.py -p 8020 -c 2 -r 2 --lo score_log.txt -v 1 --go %%n.gif
)