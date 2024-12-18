### Setup Instructions
1. Fork my repository using GitHub to create your testing repo in your account 

2. Clone fork locally to your machine using   
`git clone git@github.com:your_user/your_repo.git`

3. Configure `production.yml` for your dockerhub then create a `.env` file with this structure to add your http://mailtrap.io account inbox. Be sure to populate the username and password:    
`smtp_server=sandbox.smtp.mailtrap.io`  
`smtp_port=2525`  
`smtp_username=`  
`smtp_password=`

4. Start and build a multi-container application with this command:  
`docker compose up --build`

5. Goto http://localhost/docs to view openapi spec documentation
- Click `Authorize`   
- Input username: `admin@example.com` 
- Input password: `secret`

6. Goto http://localhost:5050 to connect and manage the database.
The following information must match the ones in the docker-compose.yml file.    
- Login:  
Email address / Username: `admin@example.com`  
Password: `adminpassword`  

- Add new server:  
Host name/address: `postgres`  
Port: `5432`  
Maintenance database: `myappdb`  
Username: `user`  
Password: `password` 
 
7. Test API and cross reference DB
***
### Pytest Note (PLEASE READ THIS SECTION FULLY BEFORE TESTING)
- When running pytests inside the containers you can use this command to run all tests:  
`docker compose exec fastapi pytest`
- You can also run a single test file with this command:  
`docker compose exec fastapi pytest tests/test_email.py`

###  Keep in mind that the user data in the DB will be dropped. To ensure you can use the application again without running into Internal Error on openapi, do this:
1. Go to http://localhost:5050 and delete the `alembic_version` table in your DB server

2. Run the container  
`docker compose up --build`

3. While the container is running, apply database migrations in a split terminal using this command:  
`docker compose exec fastapi alembic upgrade head`

- Now you will be able to Authorize your login to connect your DB with your openapi http://localhost/docs