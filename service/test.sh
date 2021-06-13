if [ $# -lt 1 ]; then
        echo 'give 1 argument'
else
        if [ $1 = 'login' ]; then
                SESSION=$(curl -H "Content-type: application/json" -X POST -d '{"user_id":"coffe2","passwd":"project"}' http://127.0.0.1:1169/login)
                echo "$SESSION"
                echo "$SESSION" >> ret
        elif [ $1 = 'schedule_add' ]; then
                statement='{"request_type":"add","session_id":"'$2'","schedule":["presentation", "test"], "date":"20210611"}'
                echo "$statement"
                curl -H "Content-type: application/json" -X POST -d "$statement" http://127.0.0.1:1169/calendar >> ret
       elif [ $1 = 'schedule_show' ]; then
                statement='{"request_type":"show","session_id":"'$2'", "date":"20210611"}'
                echo "$statement"
                curl -H "Content-type: application/json" -X POST -d "$statement" http://127.0.0.1:1169/calendar >> ret
        fi
fi
