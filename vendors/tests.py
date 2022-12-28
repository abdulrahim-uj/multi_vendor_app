from django.test import TestCase
from opencage.geocoder import OpenCageGeocode


key = '2c29ded9f6b7477b95ba72421c06f4b0'
geocoder = OpenCageGeocode(key)

query = "koppam"
result = geocoder.geocode(query)

print(type(result))

print(result[0]['geometry']['lat'])
print(result[0]['geometry']['lng'])
print(result[0]['formatted'])
print(result[0]['components']['country_code'])
print(result[0]['annotations']['timezone']['name'])
print(result[0]['annotations']['currency']['name'])  # + ['symbol', 'iso_code']
print(result[0]['components']['_type'])  # continent, country, country_code, county, postcode, state, state_code, state_district, village

print(result[-1]['annotations']['roadinfo']['road'])
print(result[-1]['components']['neighbourhood'])
