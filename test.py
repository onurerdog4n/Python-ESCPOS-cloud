import os
import requests
import time
from escpos.printer import Network




with open("credentials.txt", "r") as file:
    for line in file:
        if line.startswith("token"):
            token = line.split("=")[1].strip().strip("'")
        elif line.startswith("secret"):
            secret = line.split("=")[1].strip().strip("'")

print('BUFIBU PRINTER CLOUDA HOŞGELDİNİZ!')

if token == 'xxxxxxxxxxx':
    print('Token ve Secret Bilgilerinizi giriniz.')

    new_token = input("Yeni token: ")
    new_secret = input("Yeni secret: ")

    # Dosyayı güncelleme modunda açıyoruz
    with open("credentials.txt", "w") as file:
        file.write(f"token = '{new_token}'\n")
        file.write(f"secret = '{new_secret}'\n")
else:
    api_url = "https://bufibu.com/qr/inc/cloudorderPDF-windows.php?token=" + token + "&secret=" + secret

    image_folder = "fis"  # Folder to save the images
    fis_klasoru = "fis"

    if not os.path.exists(fis_klasoru):
        os.makedirs(fis_klasoru)

    while True:
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                if data is not None:
                    veriadedi = len(data)
                    for i in range(veriadedi):
                        try:
                            item = data[i]
                            # print('yazdirma baslatılıyor.')
                           
              

                            if 'giris' in item:
                                if item['giris'] is None:
                                    giris = 1
                                elif item['giris'] == 0:
                                    giris = 0
                                else:
                                    giris = 1
                            else:
                                giris = 1  # Veya başka bir varsayılan değer



                           

                                
                            if giris == 0:
                                print('Giriş Yapılamadı . Token ve Secret Bilgilerinizi giriniz.')
                                new_token = input("Yeni token: ")
                                new_secret = input("Yeni secret: ")

                               
                                # Dosyayı güncelleme modunda açıyoruz
                                with open("credentials.txt", "w") as file:
                                    file.write(f"token = '{new_token}'\n")
                                    file.write(f"secret = '{new_secret}'\n")
                                
                            else:
                                fis_img = item['fis_img']
                                type = item['type']
                                printers_key = item['printers_key']

                                image_url = f"https://bufibu.com/qr/inc/receiptpdf/{fis_img}.png"

                                # Check if printers_key is not empty
                                if printers_key:
                                
                                    # Check if the printers_key matches the desired printer
                                    # Connect to the printer
                                    
                                    if type == '1':
                                        # Connect to the network printer using Network class
                                        printer = Network(printers_key , profile="CT-S651")
                                    else:
                                        print("Invalid 'type' value.")
                                        continue  # Skip to the next iteration if type is invalid

                                    # Send a beep command to the printer
                                    beep_command = b'\x1b\x42\x03\x03'  # Adjust the values to control the beep sound
                                    printer._raw(beep_command)

                                    # Download the image
                                    response = requests.get(image_url)

                                    if response.status_code == 200:
                                        # Görseli "fis" klasörüne kaydet
                                        with open(os.path.join(fis_klasoru, fis_img + ".png"), "wb") as file:
                                            file.write(response.content)
                                    else:
                                        print("Görsel indirilemedi.")

                                    input_path = os.path.join(fis_klasoru, fis_img + ".png")
                            

                        
                                    printer.image(input_path)
                            

                                    # Print the image using the image data

                                    # Cut the paper
                                    printer.cut()

                                    # Close the connection
                                    printer.close()

                                   
                                else:
                                    print("printers_key tanınmadı.")

                        except Exception as e:
                            print("Hata oluştu:", str(e))

               
            else:
                print("API isteği başarısız oldu:", response.status_code)

            time.sleep(1)

        except Exception as e:
            print("Hata oluştu:", str(e))
