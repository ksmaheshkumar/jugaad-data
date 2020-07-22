export PYTHONWARNINGS="ignore:Unverified HTTPS request"

while true; do 
	OUTPUT=$(inotifywait jugaad_data/ tests/ -q -e create -e close_write -e attrib -e move )
	clear
	env/bin/python -m unittest discover
done

