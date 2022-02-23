from dotenv import load_dotenv
import os

load_dotenv()

## Example jumpserver, please edit and add yours
jumpserver1 = {}
jumpserver1['address'] = ('10.10.1.1', 22)
jumpserver1['usern'] = os.getenv('USERN')
jumpserver1['passw'] = os.getenv('PASSW')

## Example routers, please edit and add yours
routers_list = [
  dict(address=('sandbox-iosxe-recomm-1.cisco.com', 22),
    usern=os.getenv('USERNXE'),
    passw=os.getenv('PASSWXE'),
    type='IOS-XE',
    asn='65534',
    location='test1',
    jumpserver=jumpserver1
  ),
  dict(address=('sandbox-iosxr-1.cisco.com', 22),
    usern=os.getenv('USERNXR'),
    passw=os.getenv('PASSWXR'),
    type='IOS-XR',
    asn='65533',
    location='Test2',
    jumpserver=jumpserver1
  ),
  dict(address=('sandbox-nxos-1.cisco.com', 22),
    usern=os.getenv('USERNNX'),
    passw=os.getenv('PASSWNX'),
    type='NXOS',
    asn='65532',
    location='Test3',
    jumpserver=False
  )
]