import smtplib

# create connection
server = smtplib.SMTP(host = 'smtp.gmail.com', 
                    port = 587)

# login to server
username = 'something@gmail.com'
passwd = 'password'
server.ehlo()
server.starttls()

server.login(user = username, password = passwd)

# send mail
msg = 'test header\n \
test python-gmail'
server.sendmail(from_addr = 'something@gmail.com', 
                to_addrs = 'something@gmail.com', 
                msg = msg)
server.quit()

print('finish sendmail')