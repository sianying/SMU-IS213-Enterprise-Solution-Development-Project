Please do the following before using our application :D

- For docker compose to run, please open the .env file and change the value of docker_id accordingly. Once the Kong GUI is running, please use the esd-kong-postgres.json file placed in this same directory to import the services followed by the routes. This will allow our API Gateway to function.

-We have implemented an API gateway which might lead to some cold-start problems. Please be patient and refrain from double-clicking. It might take a while to load at first, but will become a lot faster later. We have also implemented an external RDS database that is based in Singapore to allow for quick retrieval of data. More info is given below.

- Currently, we have 2 customer and 3 driver accounts. 
    customer 1 username, password= jingwei, password
    customer 2 username, password= bernice, password
    driver 1 username, password= zonghan, password
    driver 2 username, password= sianying, password
    driver 3 username, password= liyin, password

You can login as the customer to add new deliveries, or login as the driver to view deliveries/update delivery status. Alternatively, you can also register as a new user (either customer/driver) and our application will open a new tab for you to register for Telegram notifications, using the Telegram bot we have created. Please ensure that your browser's pop-up block is disabled.

- In payment.py, there is a variable called success_url which leads to the success.html found under the UI(General)/Payment folder. This needs to be replaced to the absolute link on the grader's computer, because we are using the Stripe API to process payment, and it requires an absolute link to be used. There is also another variable called cancel_url which also needs to be changed (to an absolute link) for the same reason. It should lead to the delivery_order.html file in the UI(General)/Customer folder.

- When testing out the payment function (which uses Stripe API), use credit card number 4242 4242 4242 4242. The payment will not actually go through as this is a number for testing purposes.

- When choosing a date for the delivery, please choose the dates from 15th April (submission date) - 30th April only. This is because our service uses the 'schedule' microservice which has its own exclusive 'schedule' database. When the user picks a particular date for a delivery, we also need to have data in the schedule database corresponding to this date. Since we have limited storage space on our free-tier RDS database, schedules are created in the month of April 2021 only.



Additional Info:
Our simple microservices are tied to their respective databases on an external AWS RDS database hosted on the cloud. We believe that using an external database provides convenience as the grading committee would not have to manually import all the required sql files to test our application. It also makes sense in the context of our application as drivers/customers might need to add or update deliveries at many different locations, making it more suitable to host our database on the cloud rather than locally.

The SQL files that we have provided in the subfolder for each simple microservice provide a brief overview as to what it actually looks like within our RDS database. However, simply importing them will result in empty databases because we did not add any insertion statements. This is because our login microservice hashes passwords before storing it in the database for enhanced security, and we cannot predict the value of the hashed password. As such, we added all the data through our UI instead.

To see the actual data, you could enter RDS through Ubuntu or Terminal. Here is the command: 
mysql -h esd-database.cjlm2oobbep2.ap-southeast-1.rds.amazonaws.com -P 3306 -u admin -p
Password: Password123
