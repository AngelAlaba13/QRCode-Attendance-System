import qrcode

design = qrcode.QRCode(version = 1, box_size = 40, border = 3)
student_id = str(input("Student ID: "))
name = str(input("Name: "))
year_and_block = str(input("Year and Block: "))

design.add_data(f"ID: {student_id} Name: {name} Year and Block: {year_and_block}")
design.make(fit=True)

img = design.make_image(fill_color = "black", back_color = "white")
img.save("D:/VS Code Python/TKinter/QRCode Generator/qrcodes/image2.png")
