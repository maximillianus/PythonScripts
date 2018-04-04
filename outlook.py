
import os

os.chdir('C:\\NotBackedUp\\codes')
print('Current Dir:', os.getcwd())

import win32com.client as win32
outlook = win32.Dispatch('outlook.application')
mail = outlook.CreateItem(0)
mail.To = 'aditya.pradana@anz.com'
mail.Subject = 'test python email with attachment'
mail.Body = 'test only'
# mail.HTMLBody = '<h2>HTML Message body</h2>' #this field is optional

# To attach a file to the email (optional):
attachment  = "C:\\NotBackedUp\\codes\\Pyscript\\test.pptx"
mail.Attachments.Add(attachment)

mail.Send()

print('end')