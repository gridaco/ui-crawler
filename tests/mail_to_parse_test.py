import re
import urllib
from urllib.parse import urlparse, parse_qs
# //a[@class='sc-dxgOiQ dtyrSn']
email_to_url = "mailto:?body=https://mobbin.design/apps/mucho/v/2.3.0%23J2diwa9w9xBeFWViSmJH&amp;subject=Mucho iOS UI Pattern - Mobbin"
subject = re.search(r'body=(.*?)&amp;subject=', email_to_url).group(1)
print(subject)
a = urllib.parse.unquote(subject)
print(a)


