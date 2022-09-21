# Simple REST API service
## How to use
Fisrt you need to clone this repo to your computer:
```
git clone https://github.com/L1mple/backend_start.git
```
After that if you have Docker desktop installed you can print in your terminal:
```
docker-compose up
```
And the application will automatically start.
## How to interact
You can go webpage:
```
http://127.0.0.1:800/docs#/
```
to see OpenAPI docs
## Database
Also you can check Postgres database:
```
http://127.0.0.1:5050/
```
You need to enter with login: ```admin@admin.ru``` and password: ```admin```
After that select **Object**>**Register**>**Server** with *name*: ```db```, *hostname/adress*: ```db```, *username*: ```postgres``` and *password*: ```1234```
