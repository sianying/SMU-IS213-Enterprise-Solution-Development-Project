# ESD (22 March 2021)

Have to replace the success html in payment.py to the success.html file which can be found in the payment folder as we are using absolute link as Stripe requires absolute link to be used.

Have to replace the cancel html in payment.py to the delivery_order.html file in the customer folder.

To test the telegram notification, sign up as a customer/driver using our bot.

To ensure payment is successful, use credit card number 4242 4242 4242 4242. 

When registering as a new user, our application will open a new tab to register for Telegram notifications. Please ensure that your browser's pop-up block is disabled.


Multiple complex microservices use the database named 'schedule'. If the user picks a particular date for a delivery, we also have to have data in the schedule database corresponding to this date. Since we cannot possibly create schedules for every date, schedules are created in the month of April 2021 only.

