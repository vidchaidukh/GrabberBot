from datetime import datetime

tt = datetime.now()
x = datetime(2022, 5, 17, 22, 30)
print(tt.strftime("%d/%m/%Y %H:%M"))
print(x.strftime("%d/%m/%Y %H:%M"))
print(tt > x)