from prompt_toolkit import prompt
import pyotp, qrcode,os

user="wave@sky.net"
issuer="2fa"
print( "[DEBUG] Generate base32secret for user: %s" % user )
key=pyotp.random_base32()
print("[DEBUG] Generate url from ({0},{1},{2})".format(key,user,issuer))
totp =pyotp.TOTP(key)
uri=pyotp.totp.TOTP(key).provisioning_uri(user, issuer)
print( "[DEBUG] Generate two-factor authentication QRcode from url %s" % uri )
print ("*" * 50 )
print ("Two factor Authentication")
print ("*" * 50 )
print ("Please scan the QRcode with your two-factor authentication app")

qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
qr.add_data(uri)
qr.print_ascii(tty=True)
verify = input("continue (y/n)").lower()


while verify:
    try:
        otp=totp.now()
        print("[DEBUG] current OTP now is :{}".format("_".join(map("".join, zip(*[iter(otp)] * 3)))))
        guess= prompt(u'Enter six digits:', is_password=True)
        print("[DEBUG] Comparing {0} with {1}".format(guess,otp))
        if totp.verify(guess)==True:
            print("[DEBUG] OTP is correct")
            print("Login successful".format(user))
            break
        else:
            print("[DEBUG] OTP is incorrect")
            print("Please try again").format(user)
            continue
    except:
        print("[DEBUG] Something went wrong")
        break

# Generate a new secret and save it to a file

