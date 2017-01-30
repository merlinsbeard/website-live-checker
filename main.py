import os, time, requests
import argparse

class SiteCheck:
    """
    Checks a specific website object if its up or down.

    """

    def __init__(self, site):
        self.site = site

    def get_status_code(self):
        # Returns Status Code with description

        status_codes = {
                0:['HOST IS DOWN', False], 
                200: ['HOST IS UP', True],
                502: ['WEB APP SERVER IS DOWN', False],
                }

        try:
            r = requests.get(self.site)
            return status_codes[r.status_code]
        except:
            return status_codes[0]


    def send_mail(subject, to):
        # SEND MAIL SETTINGS
        EMAIL_TO = os.environ['EMAIL_TO']
        EMAIL_FROM = os.environ['EMAIL_FROM']
        EMAIL_HOST = os.environ['EMAIL_HOST']
        EMAIL_HOST_PORT = os.environ['EMAIL_PORT']

        subject = subject

        s = smtplib.SMTP(EMAIL_HOST, EMAIL_HOST_PORT)
        s.ehlo()
        s.starttls()
        s.login(EMAIL_FROM, EMAIL_PASSWORD)
        #s.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
        s.quit


    def check_site(self):
        #Returns the code description
        status = self.get_status_code()
        if status[1] == False:
            print(status[0])
            return status[0]
            # send_mail(description)
        else:
            print(status[0])
            return "Site is up and running"


    def check_site_interval(self, seconds=1):
        # Check site for status every x seconds
        while True:
            print("start checking")
            self.check_site()
            time.sleep(seconds)

#site = "https://google.com"
#a = SiteCheck(site)
#a.check_site_interval()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("website", type=str, help="Website url")
    parser.add_argument("-i","--interval", action="store",
            help="Interval in seconds")
    args = parser.parse_args()
    website = args.website
    site_checker = SiteCheck(website)
    if args.interval:
        site_checker.check_site_interval(seconds=int(args.interval))
    else:
        site_checker.check_site()

if __name__=='__main__':
    main()
