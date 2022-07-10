from distutils.errors import PreprocessError
import time
import subprocess
import random
import os
from bluetooth import *

is_service_enabled = 0 # Servis varsayılan olarak pasif.
delay_min = 180000 # Minimum Gecikme
delay_max = 220000 # Maksimum Gecikme

def jammer():
    global delay_max, delay_min # Gecikme değerleri global olarak atandı
    global is_service_enabled # Servis değeri global olarak atandı.
    global alsa_process # alsa_process'e ulaşmak için global olarak atandı
    random.seed() # Rasgele sayı türeten program

    while True: 
        try:
            if is_service_enabled == 0: # Servis pasif ise servisi kullanıcı girdisi ile aktifleştirebilirsiniz ya da uygulamadan çıkış yapabilirsiniz.
                os.system('clear')
                user_input = input("Input 's' to enable Speech Jammer or 'q' to quit.\n")

            if is_service_enabled == 1: # Servis aktif ise servisi kullanıcı girdisi ile pasifleştirebilirsiniz ya da uygulamadan çıkış yapabilirsiniz.
                os.system('clear')
                user_input = input("Input 's' to disable Speech Jammer or 'q' to quit.\n")

            if user_input == "s" and is_service_enabled == 0: # Girdi s ve servis pasifse programı aktifleştirir.  
                os.system('clear')
                print("Program state changed to 'ENABLED'.")
                random_delay = random.randint(delay_min, delay_max) # delay'i min ve max arasında rasgele bir değer döndürür.
                print("Delay: ", random_delay)
                alsa_process = subprocess.Popen(["alsaloop","-C","default","-P","default","-t",str(random_delay)]) # subprocess ile linux üzerindeki programı çalıştırır.
                user_input = "" # Kullanıcı girdisini siler.
                is_service_enabled = 1 # Servisi başlatır.

            if user_input == "s" and is_service_enabled == 1: # Girdi s ve servis aktifse program devre dışı bırakılır.
                alsa_process.terminate() # Servisi pasif hale getirir.
                os.system('clear')
                print("Program state changed to 'DISABLED'.")   
                user_input = "" # Kullanıcı girdisini siler.
                is_service_enabled = 0 # Servisi durdurur.

            if user_input == "q" and is_service_enabled == 0: # Girdi q ve servis pasifse program sonlandırılır.
                os.system('clear')
                print("Program stopped via user input, terminating the program.")
                time.sleep(2)
                os.system('clear')
                break

            if user_input == "q" and is_service_enabled == 1: # Girdi q ve servis aktifse program sonlandırılır.
                os.system('clear')
                alsa_process.terminate()
                print("Program stopped via user input, terminating the program.")
                time.sleep(2)
                os.system('clear')
                break

        except KeyboardInterrupt: # CTRL-C tuşuna basıldığında programdan çıkar.
            os.system('clear')
            alsa_process.terminate() # Program çalışıyorsa programı sonlandırır.
            print("Program stopped via keyboard interrupt, terminating the program.")
            time.sleep(2)
            os.system('clear')
            break

def main():
    print("Welcome to our speech jammer program.")
    time.sleep(3)
    os.system('clear')
    jammer()

main()