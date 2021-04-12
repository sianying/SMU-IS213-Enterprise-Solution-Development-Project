# ESD (22 March 2021)

Our simple microservices are tied to their respective databases on an external AWS RDS database hosted on the cloud. Multiple complex microservices use the database named 'schedule'. If the user picks a particular date, we also have to have data in the schedule database corresponding to this date.

Since we are using free tier for RDS, there are limitations in storage space. As such, we only created schedules in the month of April 2021 to avoid taking up too much storage space.

Have to replace the success html in payment.py to the success.html file which can be found in the payment folder as we are using absolute link as Stripe requires absolute link to be used.

Have to replace the cancel html in payment.py to the delivery_order.html file in the customer folder.

To test the telegram notification, sign up as a customer/driver using our bot.

To ensure payment is successful, use credit card number 4242 4242 4242 4242 

