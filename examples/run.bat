for /l %%n in (1,1,10) do (
    start python run_client.py -a r -p 8020
    start python run_client.py -a q -p 8020
    python run_server.py -p 8020 -c 3 -r 3 --lo score_log_qlearning.txt -v 1 --go %%n.gif
)