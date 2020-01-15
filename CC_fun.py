#15/01/2020
#This file ws written by Henry Oldroyd

def write_json(dir, dict):
    import json
    #dict = json_functions.check_excess_slashes(dict)
    with open(dir, "w") as file:
        json_data = json.dumps(dict, ensure_ascii=False).encode("utf8")
        # excess back slashes solution    https://stackoverflow.com/questions/54876010/python-3-when-writing-json-file-double-backslash-problem
        json_data = json_data.decode('UTF-8')
        #json_data = str(json_data)[2:-1]
        file.write(json_data)

def read_json(dir):
    import json
    with open(dir, "r") as file:
        dict = json.load(file)
    return dict


def encrypt_file(dir, key):
    with open(dir, "r", encoding='utf-8') as file:
        content = file.readlines()

        new_content = []
        for line in content:
            new_line = ""
            for character in line:
                new_character = chr( ord(character)^key )
                new_line = new_line + new_character
            new_content = new_content + [new_line]

        with open(dir, "w", encoding='utf-8') as file:
            file.writelines(new_content)



def send_email(recipinet_email_addresses, sender_email_address, password, subject, main_message):
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    import sys

    
    HTML_template_code = """
        <html>
            <head>
        		<title>Styled HTML Email Template 1</title>
        	</head>

        	<body style="background-color:  #b3d9ff">
        		<h1 style="font-size: 36; font-family: Verdana; color: #ff8000; text-align: center; text-decoration: bold; text-transform: uppercase; padding: 5px; margin: 10px">___subject___</h1>
        		<br/>
        		<!--<h2 style="font-size: 30; font-family: Verdana; color: #ff8000; text-align: left; padding: 5px; margin: 10px">Dear ___reciever___:</h2>-->

        		<p style="font-size: 28; color: #ff3333; font-family: Comic Sans MS; padding: 5px; margin: 5px">
        			___message___
        			<br/><br/>
        		</p>
        		<!-- h2 with text-align: center; -->
        		<h2 style="font-family: Verdana; color: #ff8000; text-align: center; padding: 5px; margin: 10px">
        			Yours Sincerely:<br/>
        			Henry Oldroyd (10E)
        			<br/><br/>
        		</h2>
        		<!-- p with font-size: 20 -->
        		<p style="font-size: 20; font-size: 30; color: #ff3333; font-family: Comic Sans MS; padding: 5px; margin: 5px">
        			This Email Was Generated and sent from a HTML and Python Program I created myself.
        		</p>


            </body>
        </html>
    """
    
    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = subject


        message["From"] = sender_email_address
        message["To"] = ",".join(recipinet_email_addresses)


        #HTML_template = input("Enter number of Template to use (eg.1):   ")
        #with open("sample_HTML_ emails\\Sample_"+str(HTML_template)+".html","r") as TXT_file:
            #html = TXT_file.read()

        local_main_message_multi = main_message
        local_main_message = ""

        for i in range(len(str(local_main_message_multi))):
            if(ord(local_main_message_multi[i]) == 10):
                local_main_message = local_main_message+"<br/>"
            else:
                local_main_message = local_main_message + local_main_message_multi[i]

        if(html.find("___subject___")!= -1):
            html = html.replace("___subject___", message["Subject"])
        if(html.find("___message___")!= -1):
            html = html.replace("___message___", local_main_message)


        message.attach(MIMEText(html, "html"))
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email_address, password)
            server.sendmail(sender_email_address, recipinet_email_addresses, message.as_string())

        return "EMAIL SENT SUCCESSFULLY"

    except Exception as e:

        exc_obj = str(sys.exc_info()[1])

        if(exc_obj.find("Cannot Decode response") != -1)or(exc_obj.find("Username and Password not accepted") != -1):
            return "EMAIL FAILED TO SEND:   Password Incorrect"

        elif(exc_obj.find("The recipient address <") != -1)and(exc_obj.find("> is not a valid") != -1):
            return "EMAIL FAILED TO SEND:   Recipient Addresses Incorrect"

        else:
            return "EMAIL FAILED TO SEND   error unknown"
main_message = """
    Hello Henry

    How Are You?
"""
print(send_email(["henryoldroyd10@gmail.com"], "henryoldroyd5@gmail.com", "9j9x7zb4ad", "testing testing", main_message))
