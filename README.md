Please do the following before using our application :D

- In payment.py, there is a variable called success_url which leads to the success.html found under the UI(General)/Payment folder. This will have to be replaced to the absolute link on the grader's computer, because we are using the Stripe API which requires an absolute link to be used. This will depend on where the grader has placed this ESD folder.

There is also another variable called cancel_url which needs to be changed for the same reason. It should lead to the delivery_order.html file in the UI(General)/Customer folder.

- When registering as a new user (both driver & customer), our application will open a new tab to register for Telegram notifications. Please ensure that your browser's pop-up block is disabled. To test this function out, do sign up as a customer/driver using our Telegram bot.

- When choosing a date for the delivery, please choose the dates from 15th April (submission date) - 30th April only. This is because our service uses the 'schedule' microservice which has its own exclusive 'schedule' database. When the user picks a particular date for a delivery, we also have to have data in the schedule database corresponding to this date. Since we have limited storage space on our external RDS database, schedules are created in the month of April 2021 only.

- When testing out the payment function (which uses Stripe API), use credit card number 4242 4242 4242 4242.


Additional Info:
Our simple microservices are tied to their respective databases on an external AWS RDS database hosted on the cloud. We believe that using an external database provides convenience as the grading committee would not have to manually import all the required sql files to test our application. It also makes sense in the context of our application as drivers/customers might need to add or update deliveries at many different locations, making it more suitable to host our database on the cloud rather than locally.