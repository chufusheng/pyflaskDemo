port=`pstree -ap|grep gunicorn | head -n 1 |awk '{print $1}'|awk -F "," '{print $2}'`
echo "port is  $port"
kill -9 $port
