apartment_link1 = 'https://www.propertyfinder.ae/en/plp/rent/apartment-for-rent-dubai-dubai-marina-marina-terrace-12348855.html'
apartment_link2 = 'https://www.propertyfinder.ae/en/plp/rent/apartment-for-rent-dubai-dubai-marina-continental-tower-12090495.html'
output1 = ['Sea and Marina View | Upgraded | Chiller free', 'Nirali Ganatra', '+97145560345', apartment_link1]
output2 = ['Marina View | Furnished | Flexible Terms', ':(', '+447897033205', apartment_link2]

BASE_URL = 'https://www.propertyfinder.ae/en/search?l=50&c=2&fu=0&rp=y&ob=mr'

INPUT_DATA = [('mock_input', BASE_URL+'&page=12', '1'), ('mock_bad_input', BASE_URL, '2')]

GET_PAGES_DATA = [(BASE_URL, 1, '1'), (BASE_URL + '&page=6', 12, '17')]

GET_NAME_DATA = [(apartment_link1, 'Nirali Ganatra'), (apartment_link2, ':(')]

GET_ADV_DATA = [(['https://www.propertyfinder.ae/en/search?l=50&c=2&fu=0&rp=y&ob=mr'], 27),
                (['https://www.propertyfinder.ae/en/search?l=50&c=2&fu=0&rp=y&ob=mr&page=1',
                  'https://wwwdgg.propertyfinder.ae/en/search?l=50&c=2&fu=0&rp=y&ob',
                  'https://www.propertyfinder.ae/en/search?l=50&c=2&fu=0&rp=y&ob=mr&page=2'], 52)]

PARSE_ADV_DATA = [([apartment_link1], output1), ([apartment_link2], output2)]

EXPORT_DATA = [([output1], 'arab1.xlsx'), ([output2], 'arab2.xlsx')]