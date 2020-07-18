##
pip freeze > requirements.txt


##
pip install -r requirements.txt


# TEST1  (client - server)
# cmd 1
pip server.py

# cmd 2
pip post.py


# TEST2  (client - server - database)
# cmd 1
pip dbserver.py

# cmd 2
pip post.py

# TEST3  (client(table) - server - database)
# cmd 1
pip tableserver.py

# cmd 2
pip post.py

# TEST4  (client(graph) - server - database)
# cmd 1
pip graphserver.py

# cmd 2
pip post.py
