import unidecode
import scrapy
import requests
import os
from docx import Document

if os.path.exists("dados_scrapy.docx"):
    doc = Document("dados_scrapy.docx")
else:
    doc = Document()

def extract_price(response):


  price_selectors = [
      '//html/body/main/div[2]/div[5]/div/div[1]/div/div[1]/div/div[@class="ui-pdp-container__row ui-pdp-container__row--price"]/div/div[1]/div[1]/span/span/span[2]/text()',
      '//*[@id="ui-pdp-main-container"]/div[1]/div/div[1]/div[2]/div[3]/div[1]/div[1]/span/span/span[2]/text()',
      '//*[@id="ui-pdp-main-container"]/div[1]/div/div[1]/div[2]/div[2]/div[1]/div[1]/span[1]/span/span[2]/text()'
  ]

  for selector in price_selectors:
    price = response.xpath(selector).get()
    if price:
      # Remove any commas (assuming price uses dots as separators)
      price = price.replace('.', '')
      decimal_selector = selector.replace("span[2]/text()", "") + 'span[@class="andes-money-amount__cents andes-money-amount__cents--superscript-36"]/text()'
      price_decimal = response.xpath(decimal_selector).get()
      
      if price_decimal:
        # Combine price and decimal part (assuming price uses dots)
        return float(f"{price}.{price_decimal}")
      else:
        # Price without decimal, return as float
        try:
          return float(price)
        except ValueError:
          # Handle potential conversion errors (optional)
          pass

  return None  # No price found


def download_image(image_src, download_folder, desired_filename):
    os.makedirs("images", exist_ok=True)  
    desired_filename = desired_filename + 'images' 
    desired_filename = os.path.join('images', desired_filename + '.png')  # Append .png to the filename

    response = requests.get(image_src, stream=True)

    if response.status_code == 200:
        with open(desired_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        print("Image downloaded successfully:", desired_filename)
        return desired_filename  # Return the downloaded file path
    else:
        print(f"Failed to download image: {response.status_code}")
        return None  # Return None on failure


options = ["Storm 40", "Storm 60", "Lite 60","Storm 70", "Lite 70", "Bob 90", "Storm 120", "Lite 120", "Bob 120", "Storm 200", "Storm 200 MONO", "Bob 200", "Lite 200"]
option_selected = value=options[0]



class MlSpider(scrapy.Spider):
    name = 'ml'
    start_urls = ["https://lista.mercadolivre.com.br/fonte-jfa"]
    
    
    def __init__(self, palavra=None, *args, **kwargs):
        super(MlSpider, self).__init__(*args, **kwargs)
        self.palavra = palavra
    
    
    
    def parse(self, response, **kwargs):
        option_selected = "Bob 120"
        search = ""
        if option_selected == "Storm 40":
            search = "fonte storm 40a"
        if option_selected == "Lite 60":
            search = "fonte lite 60a"
        elif option_selected == "Storm 60":
            search = "fonte storm 60a"
        if option_selected == "Lite 70":
            search = "fonte lite 70a"
        elif option_selected == "Storm 70":
            search = "fonte storm 70a"
        elif option_selected == "Bob 90":
            search = "fonte bob 90a"
        elif option_selected == "Storm 120":
            search = "fonte storm 120a"
        elif option_selected == "Lite 120":
            search = "fonte lite 120a"
        elif option_selected == "Bob 120":
            search = "fonte bob 120a"
        elif option_selected == "Storm 200":
            search = "fonte storm 200a"
        elif option_selected == "Lite 200":
            search = "fonte lite 200a"
        elif option_selected == "Bob 200":
            search = "fonte bob 200a"
        elif option_selected == "Storm 200 MONO":
            search = "fonte storm 200a mono"
        search = search.replace(" ", "%20")
        # search = "fonte%2040a%20jfa"
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": "template=template-light; ai_user=EgV55|2024-05-28T11:45:48.501Z; _fbp=fb.1.1716896748573.875911634; lang_nubi=pt_br; hubspotutk=3b227fd6020f103ba35ecca053547573; intercom-id-re8wm274=4a6e9f6a-7d60-4e66-9f7b-3ff7f52b76be; intercom-device-id-re8wm274=76824f0d-e71f-4d6b-8781-c222868a73aa; _ga=GA1.3.836422724.1716896749; _gid=GA1.2.1790036862.1717420819; _ce.clock_event=1; _ce.clock_data=4%2C179.106.99.199%2C1%2Cc92baae71318dc81de51a663df2f8b4f%2CChrome%2CBR; TiPMix=23.136864673971257; x-ms-routing-name=self; ARRAffinity=16cb49e87e2f16be9b1551941d631fc64e2de687dbb3ac1bc864b1e77bb968b3; ARRAffinitySameSite=16cb49e87e2f16be9b1551941d631fc64e2de687dbb3ac1bc864b1e77bb968b3; i18next=pt_br; _ce.irv=returning; cebs=1; _hp2_ses_props.2056355555=%7B%22ts%22%3A1717581527028%2C%22d%22%3A%22app.nubimetrics.com%22%2C%22h%22%3A%22%2Faccount%2Flogin%22%2C%22q%22%3A%22%3FReturnUrl%3D%252fopportunity%252fcategoryDetail%22%2C%22g%22%3A%22%23%3Fcategory%3DMLB271599%22%7D; _clck=1ukw5r7%7C2%7Cfmd%7C0%7C1609; __hstc=154116135.3b227fd6020f103ba35ecca053547573.1716896751921.1717523902919.1717581529520.21; __hssrc=1; _gcl_au=1.1.81739417.1716896749.11480788.1717581556.1717581558; ASP.NET_SessionId=usdinee3vna2nte24ymksotx; .ASPXAUTH=EAC6B31F30CCC410EC4DBFEAEB2D442BB55EEF7B57C5135024E29DD3818EFD56185F486322BEBC49337F4E1F145223C53672657B94B287AB239B950243FBA63FA662E42A23378FFBEB909B7F2A7A02BC1E4161886341EAA1FF03E6FF0B224DD3D44FAB65C033C6F4E1268CCCF746348B13B3AAB2F159ADB2E12548B69F5C32E34366AC54FA310BBD235C4626C89094AF9A9A08FC1FD9947EC84C4BD5DC3DE13711050FC3327CFD873871E4A479900B206C28918AC7781387567BF1DA745DB0C08A744773D0A55D1FBCAB227CBCCE5CA42E0C2AD8CF517FBDB978FDA6EFFC5FB02B3386330FA912E750874DAE8D60A33290C8FF2C624AA6AC0682C32628EC5263; _uetsid=06b9dbb021ac11ef980e8d68404bddbd; _uetvid=d4f1f2b01ce711efb06041a93bf318c4; cebsp_=2; _hp2_id.2056355555=%7B%22userId%22%3A%221540691698154969%22%2C%22pageviewId%22%3A%226163090102658035%22%2C%22sessionId%22%3A%224218103697812068%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D; _clsk=1hx57wl%7C1717581564530%7C2%7C1%7Cy.clarity.ms%2Fcollect; __hssc=154116135.2.1717581529520; intercom-session-re8wm274=bnAyQU1GQ0RDd0xUUnFDcnVGckhLV0psUVV6Uy96eEduUXNUaHU2ZmxXMVlCL0tHTkd4dEdhM0FpOWEwS3hhYi0tR0tNKytqdEhHeVh2WXZVTVA0SWIydz09--3be843af82f6d9822dd440bdccc91b38f5e14935; _ce.s=v~7baa07f6ad267a180f8618e02b13f0b27eb93927~lcw~1717581608095~lva~1717581526076~vpv~9~v11.fhb~1717581563074~v11.lhb~1717581563075~v11.cs~229172~v11.s~32e31da0-2322-11ef-b9ed-211dea611aeb~v11.sla~1717581608706~v11.send~1717581608095~lcw~1717581608707; sc_is_visitor_unique=rx12923916.1717581611.D55E01C3D14F4F03DEB97B398CBAA0C5.18.13.11.9.7.6.3.3.2; _ga_1BD6V1LPWP=GS1.1.1717581525.22.1.1717581612.56.0.0; _ga_X9JW5VPF68=GS1.1.1717581526.10.1.1717581612.56.0.0; _ga=GA1.2.836422724.1716896749; _gat_UA-36655489-3=1; ai_session=ROCgg|1717581526310|1717581613329.7; _ga_26N5SV28FF=GS1.1.1717581526.33.1.1717581613.55.0.0",
            "Host": "app.nubimetrics.com",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "sec-ch-ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }
        
        request = requests.get(
            f"https://app.nubimetrics.com/api/search/items?attributes=results,available_filters,paging,filters&buying_mode=buy_it_now&exportData=false&isControlPrice=false&language=pt_BR&limit=200&offset=0&order=price_asc&pvp=0&search_filters=condition%3Dnew@&seller_id=1242763049&site_id=MLB&to_search={search}&typeSearch=q",
            headers=headers
        )
        
        request.raise_for_status()
        data = request.json()
        paging_data = data.get('data', {}).get('paging', {}) 

        total = paging_data.get('total') 
        offset = paging_data.get('offset') 
        limit = paging_data.get('limit') 
        
        while offset < total:
            request = requests.get(
                f"https://app.nubimetrics.com/api/search/items?attributes=results,available_filters,paging,filters&buying_mode=buy_it_now&exportData=false&isControlPrice=false&language=pt_BR&limit=200&offset={offset}&order=price_asc&pvp=0&search_filters=condition%3Dnew@&seller_id=1242763049&site_id=MLB&to_search={search}&typeSearch=q",
                headers=headers
            )
            request.raise_for_status()
            data = request.json()
            paging_data = data.get('data', {}).get('paging', {}) 

            total = paging_data.get('total') 
            offset = paging_data.get('offset') 
            limit = paging_data.get('limit') 
            offset = offset + limit;
            print(offset)
            
            for item in data.get('data', {}).get('results', []):
                name = item.get('title')
                url = item.get('permalink')
                loja = item.get('sellernickname')
                price = item.get('price')
                new_name = name.lower();
                new_name = unidecode.unidecode(new_name)
                if option_selected == "Storm 40":
                    opcao_selecionada = "Storm 40"
                    if "bob" not in new_name and "lite" not in new_name and "controle" not in new_name and 'jfa' in new_name:
                        if "40a" in new_name or "40" in new_name or "40 amperes" in new_name or "40amperes" in new_name or "36a" in new_name or "36" in new_name or "36 amperes" in new_name or "36amperes" in new_name:
                            yield scrapy.Request(url=url, callback=self.parse_product, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.radicalsom.com.br/fonte-40a-jfa_OrderId_PRICE_NoIndex_True', callback=self.parse_radicalson, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.bestonline.com.br/fonte-jfa-40a_OrderId_PRICE_NoIndex_True', callback=self.parse_bestonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.shoppratico.com.br/fonte-jfa-40a_OrderId_PRICE_NoIndex_True', callback=self.parse_shoppratico, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.renovonline.com.br/fonte-jfa-40a_OrderId_PRICE_NoIndex_True', callback=self.parse_renovonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.lsdistribuidora.com.br/fonte-jfa-40a_OrderId_PRICE_NoIndex_True', callback=self.parse_lsdistribuidora, meta={'name': name, 'loja': loja, 'price':price})
                            
                elif option_selected == "Storm 60":
                    opcao_selecionada = "Storm 60"
                    if "bob" not in new_name and "lite" not in new_name and "controle" not in new_name and 'jfa' in new_name:
                        if "60a" in new_name or "60" in new_name or "60 amperes" in new_name or "60amperes" in new_name or "60 a" in new_name:
                            yield scrapy.Request(url=url, callback=self.parse_product, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.radicalsom.com.br/fonte-60a-jfa_OrderId_PRICE_NoIndex_True', callback=self.parse_radicalson, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.bestonline.com.br/fonte-jfa-60a_OrderId_PRICE_NoIndex_True', callback=self.parse_bestonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.shoppratico.com.br/fonte-jfa-60a_OrderId_PRICE_NoIndex_True', callback=self.parse_shoppratico, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.renovonline.com.br/fonte-jfa-60a_OrderId_PRICE_NoIndex_True', callback=self.parse_renovonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.lsdistribuidora.com.br/fonte-jfa-60a_OrderId_PRICE_NoIndex_True', callback=self.parse_lsdistribuidora, meta={'name': name, 'loja': loja, 'price':price})
                            
                elif option_selected == "Lite 60":
                    opcao_selecionada = "Lite 60"
                    if "bob" not in new_name and "lite" in new_name and "controle" not in new_name and 'jfa' in new_name:
                        if "60a" in new_name or "60" in new_name or "60 amperes" in new_name or "60amperes" in new_name or "60 a" in new_name:
                            yield scrapy.Request(url=url, callback=self.parse_product, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.radicalsom.com.br/fonte-60a-lite-jfa_OrderId_PRICE_NoIndex_True', callback=self.parse_radicalson, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.bestonline.com.br/fonte-jfa-60a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_bestonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.shoppratico.com.br/fonte-jfa-60a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_shoppratico, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.renovonline.com.br/fonte-jfa-60a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_renovonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.lsdistribuidora.com.br/fonte-jfa-60a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_lsdistribuidora, meta={'name': name, 'loja': loja, 'price':price})
                            
                elif option_selected == "Storm 70":
                    opcao_selecionada = "Storm 70"
                    if "bob" not in new_name and "lite" not in new_name and "controle" not in new_name and 'jfa' in new_name:
                        if "70a" in new_name or "70" in new_name or "70 amperes" in new_name or "70amperes" in new_name or "70 a" in new_name:
                            yield scrapy.Request(url=url, callback=self.parse_product, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.radicalsom.com.br/fonte-70a-jfa_OrderId_PRICE_NoIndex_True', callback=self.parse_radicalson, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.bestonline.com.br/fonte-jfa-70a_OrderId_PRICE_NoIndex_True', callback=self.parse_bestonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.shoppratico.com.br/fonte-jfa-70a_OrderId_PRICE_NoIndex_True', callback=self.parse_shoppratico, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.renovonline.com.br/fonte-jfa-70a_OrderId_PRICE_NoIndex_True', callback=self.parse_renovonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.lsdistribuidora.com.br/fonte-jfa-70a_OrderId_PRICE_NoIndex_True', callback=self.parse_lsdistribuidora, meta={'name': name, 'loja': loja, 'price':price})
                            
                            
                elif option_selected == "Lite 70":
                    opcao_selecionada = "Lite 70"
                    if "bob" not in new_name and "lite" in new_name and "controle" not in new_name and 'jfa' in new_name:
                        if "70a" in new_name or "70" in new_name or "70 amperes" in new_name or "70amperes" in new_name or "70 a" in new_name:
                            yield scrapy.Request(url=url, callback=self.parse_product, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.radicalsom.com.br/fonte-70a-lite-jfa_OrderId_PRICE_NoIndex_True', callback=self.parse_radicalson, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.bestonline.com.br/fonte-jfa-70a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_bestonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.shoppratico.com.br/fonte-jfa-70a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_shoppratico, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.renovonline.com.br/fonte-jfa-70a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_renovonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.lsdistribuidora.com.br/fonte-jfa-70a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_lsdistribuidora, meta={'name': name, 'loja': loja, 'price':price})
                            
                            
                elif option_selected == "Bob 90":
                    opcao_selecionada = "Bob 90"
                    if "bob" in new_name and "lite" not in new_name and "controle" not in new_name and 'jfa' in new_name:
                        if "90a" in new_name or "90" in new_name or "90 amperes" in new_name or "90amperes" in new_name or "90 a" in new_name:
                            yield scrapy.Request(url=url, callback=self.parse_product, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.radicalsom.com.br/fonte-90a-bob-jfa_OrderId_PRICE_NoIndex_True', callback=self.parse_radicalson, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.bestonline.com.br/fonte-jfa-90a-bob_OrderId_PRICE_NoIndex_True', callback=self.parse_bestonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.shoppratico.com.br/fonte-jfa-90a-bob_OrderId_PRICE_NoIndex_True', callback=self.parse_shoppratico, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.renovonline.com.br/fonte-jfa-90a-bob_OrderId_PRICE_NoIndex_True', callback=self.parse_renovonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.lsdistribuidora.com.br/fonte-jfa-90a-bob_OrderId_PRICE_NoIndex_True', callback=self.parse_lsdistribuidora, meta={'name': name, 'loja': loja, 'price':price})
                            
                            
                elif option_selected == "Storm 120":
                    opcao_selecionada = "Storm 120"
                    if "bob" not in new_name and "lite" not in new_name and "controle" not in new_name and 'jfa' in new_name:
                        if "120a" in new_name or "120" in new_name or "120 amperes" in new_name or "120amperes" in new_name or "120 a" in new_name:
                            yield scrapy.Request(url=url, callback=self.parse_product, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.radicalsom.com.br/fonte-120a-jfa_OrderId_PRICE_NoIndex_True', callback=self.parse_radicalson, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.bestonline.com.br/fonte-jfa-120a_OrderId_PRICE_NoIndex_True', callback=self.parse_bestonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.shoppratico.com.br/fonte-jfa-120a_OrderId_PRICE_NoIndex_True', callback=self.parse_shoppratico, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.renovonline.com.br/fonte-jfa-120a_OrderId_PRICE_NoIndex_True', callback=self.parse_renovonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.lsdistribuidora.com.br/fonte-jfa-120a_OrderId_PRICE_NoIndex_True', callback=self.parse_lsdistribuidora, meta={'name': name, 'loja': loja, 'price':price})
                            
                            
                elif option_selected == "Lite 120":
                    opcao_selecionada = "Lite 120"
                    if "bob" not in new_name and "lite" in new_name and "controle" not in new_name and 'jfa' in new_name:
                        if "120a" in new_name or "120" in new_name or "120 amperes" in new_name or "120amperes" in new_name or "120 a" in new_name:
                            yield scrapy.Request(url=url, callback=self.parse_product, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.radicalsom.com.br/fonte-120a-lite-jfa_OrderId_PRICE_NoIndex_True', callback=self.parse_radicalson, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.bestonline.com.br/fonte-jfa-120a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_bestonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.shoppratico.com.br/fonte-jfa-120a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_shoppratico, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.renovonline.com.br/fonte-jfa-120a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_renovonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.lsdistribuidora.com.br/fonte-jfa-120a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_lsdistribuidora, meta={'name': name, 'loja': loja, 'price':price})
                            
                            
                elif option_selected == "Bob 120":
                    opcao_selecionada = "Bob 120"
                    if "bob" in new_name and "lite" not in new_name and "controle" not in new_name and 'jfa' in new_name:
                        if "120a" in new_name or "120" in new_name or "120 amperes" in new_name or "120amperes" in new_name or "120 a" in new_name:
                            yield scrapy.Request(url=url, callback=self.parse_product, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.radicalsom.com.br/fonte-120a-bob-jfa_OrderId_PRICE_NoIndex_True', callback=self.parse_radicalson, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.bestonline.com.br/fonte-jfa-120a-bob_OrderId_PRICE_NoIndex_True', callback=self.parse_bestonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.shoppratico.com.br/fonte-jfa-120a-bob_OrderId_PRICE_NoIndex_True', callback=self.parse_shoppratico, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.renovonline.com.br/fonte-jfa-120a-bob_OrderId_PRICE_NoIndex_True', callback=self.parse_renovonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.lsdistribuidora.com.br/fonte-jfa-120a-bob_OrderId_PRICE_NoIndex_True', callback=self.parse_lsdistribuidora, meta={'name': name, 'loja': loja, 'price':price})
                            
                            
                elif option_selected == "Storm 200":
                    opcao_selecionada = "Storm 200"
                    if "bob" not in new_name and "lite" not in new_name and "controle" not in new_name and 'jfa' in new_name and 'mono' not in new_name and 'monovolt' not in new_name:
                        if "200a" in new_name or "200" in new_name or "200 amperes" in new_name or "200amperes" in new_name or "200 a" in new_name:
                            yield scrapy.Request(url=url, callback=self.parse_product, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.radicalsom.com.br/fonte-200a-jfa_OrderId_PRICE_NoIndex_True', callback=self.parse_radicalson, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.bestonline.com.br/fonte-jfa-200a_OrderId_PRICE_NoIndex_True', callback=self.parse_bestonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.shoppratico.com.br/fonte-jfa-200a_OrderId_PRICE_NoIndex_True', callback=self.parse_shoppratico, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.renovonline.com.br/fonte-jfa-200a_OrderId_PRICE_NoIndex_True', callback=self.parse_renovonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.lsdistribuidora.com.br/fonte-jfa-200a_OrderId_PRICE_NoIndex_True', callback=self.parse_lsdistribuidora, meta={'name': name, 'loja': loja, 'price':price})
                            
                            
                elif option_selected == "Storm 200 MONO":
                    opcao_selecionada = "Storm 200 MONO"
                    if "bob" not in new_name and "lite" not in new_name and "controle" not in new_name and 'jfa' in new_name and 'mono' in new_name:
                        if "200a" in new_name or "200" in new_name or "200 amperes" in new_name or "200amperes" in new_name or "200 a" in new_name:
                            yield scrapy.Request(url=url, callback=self.parse_product, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.radicalsom.com.br/fonte-200a-mono-jfa_OrderId_PRICE_NoIndex_True', callback=self.parse_radicalson, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.bestonline.com.br/fonte-jfa-200a-mono_OrderId_PRICE_NoIndex_True', callback=self.parse_bestonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.shoppratico.com.br/fonte-jfa-200a-mono_OrderId_PRICE_NoIndex_True', callback=self.parse_shoppratico, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.renovonline.com.br/fonte-jfa-200a-mono_OrderId_PRICE_NoIndex_True', callback=self.parse_renovonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.lsdistribuidora.com.br/fonte-jfa-200a-mono_OrderId_PRICE_NoIndex_True', callback=self.parse_lsdistribuidora, meta={'name': name, 'loja': loja, 'price':price})
                            
                            
                elif option_selected == "Lite 200":
                    opcao_selecionada = "Lite 200"
                    if "bob" not in new_name and "lite" in new_name and "controle" not in new_name and 'jfa' in new_name:
                        if "200a" in new_name or "200" in new_name or "200 amperes" in new_name or "200amperes" in new_name or "200 a" in new_name:
                            yield scrapy.Request(url=url, callback=self.parse_product, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.radicalsom.com.br/fonte-200a-lite-jfa_OrderId_PRICE_NoIndex_True', callback=self.parse_radicalson, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.bestonline.com.br/fonte-jfa-200a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_bestonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.shoppratico.com.br/fonte-jfa-200a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_shoppratico, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.renovonline.com.br/fonte-jfa-200a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_renovonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.lsdistribuidora.com.br/fonte-jfa-200a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_lsdistribuidora, meta={'name': name, 'loja': loja, 'price':price})
                            
                            
                elif option_selected == "Bob 200":
                    opcao_selecionada = "Bob 200"
                    if "bob" in new_name and "lite" not in new_name and "controle" not in new_name and 'jfa' in new_name and 'mono' not in new_name and 'monovolt' not in new_name:
                        if "200a" in new_name or "200" in new_name or "200 amperes" in new_name or "200amperes" in new_name or "200 a" in new_name:
                            yield scrapy.Request(url=url, callback=self.parse_product, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.radicalsom.com.br/fonte-200a-bob-jfa_OrderId_PRICE_NoIndex_True', callback=self.parse_radicalson, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.bestonline.com.br/fonte-jfa-200a-bo_OrderId_PRICE_NoIndex_True', callback=self.parse_bestonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.shoppratico.com.br/fonte-jfa-200a-bo_OrderId_PRICE_NoIndex_True', callback=self.parse_shoppratico, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.renovonline.com.br/fonte-jfa-200a-bo_OrderId_PRICE_NoIndex_True', callback=self.parse_renovonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.lsdistribuidora.com.br/fonte-jfa-200a-bo_OrderId_PRICE_NoIndex_True', callback=self.parse_lsdistribuidora, meta={'name': name, 'loja': loja, 'price':price})
                
    def parse_product(self, response):
        name = response.meta['name']
        loja = response.meta['loja']
        # price = response.meta['price']
        
        id_anuncio = response.xpath('//*[@id="denounce"]/div/p/span/text()').get().replace("#", "")
        imagem = response.xpath('//*[@id="gallery"]/div/div/span[2]/figure/img/@data-zoom').get()
        if imagem:
            download_image(imagem, option_selected,id_anuncio)
        
        price = extract_price(response)
        new_price_float = price
        if price:
            print("Extracted price:", price)
        else:
            print("Price not found")
           
        
        
            
        parcelado = response.xpath('//*[@id="pricing_price_subtitle"]/text()').get()
        parcelado = int(parcelado.replace("x", "").strip())
        
        other_price = response.xpath('//*[@id="pricing_price_subtitle"]/span[2]/span/span[2]/text()').get()
        other_price_decimal = response.xpath('//*[@id="pricing_price_subtitle"]/span[2]/span/span[4]/text()').get()
        
        if other_price and other_price_decimal:
            new_price_other = f"{other_price},{other_price_decimal}"
        elif other_price:
            new_price_other = other_price
        else:
            new_price_other = '0'

        try:
            new_price_other_float = float(new_price_other.replace('.', '').replace(',', '.'))
            new_price_other_float = round((new_price_other_float * parcelado), 3)
        except ValueError:
            new_price_other_float = 0.0
            

        target_id = response.xpath('//*[@id="denounce"]/div/p/span/text()').get()
        if target_id:
            target_id = target_id.replace("#", "")
    

        isSemJuros = response.xpath('//*[@id="pricing_price_subtitle"]/text()').getall()
        
        if isSemJuros:
            if len(isSemJuros) > 1:
                if "sem juros" in isSemJuros[1].lower():
                    tipo = "Premium"
                else:
                    tipo = "Clássico"
            else:
                tipo = "Clássico"
        else:
            tipo = "Clássico" 
        
            
        if tipo == "Clássico" and new_price_float:
            if option_selected == "Storm 40" and new_price_float >= 402.79:
                return;
            if option_selected == "Storm 60" and new_price_float >= 443.07:
                return;
            if option_selected == "Lite 60" and new_price_float >= 364.95:
                return;
            if option_selected == "Lite 70" and new_price_float >= 408.73:
                return;
            if option_selected == "Storm 70" and new_price_float >= 493.42:
                return;
            if option_selected == "Bob 90" and new_price_float >= 422.93:
                return;
            if option_selected == "Bob 120" and new_price_float >= 499.46:
                return;
            if option_selected == "Lite 120" and new_price_float >= 536.26:
                return;
            if option_selected == "Storm 120" and new_price_float >= 634.40:
                return;
            if option_selected == "Bob 200" and new_price_float >= 624.33:
                return;
            if option_selected == "Lite 200" and new_price_float >= 681.83:
                return;
            if option_selected == "Storm 200 MONO" and new_price_float >= 736.61:
                return;
            if option_selected == "Storm 200" and new_price_float >= 805.59:
                return;
        if tipo == "Premium" and new_price_float:
            if option_selected == "Storm 40" and new_price_float >= 433.00:
                return;
            if option_selected == "Storm 60" and new_price_float >= 390.43:
                return;
            if option_selected == "Lite 60" and new_price_float >= 473.28:
                return;
            if option_selected == "Lite 70" and new_price_float >= 434.42:
                return;
            if option_selected == "Storm 70" and new_price_float >= 523.63:
                return;
            if option_selected == "Bob 90" and new_price_float >= 443.07:
                return;
            if option_selected == "Bob 120" and new_price_float >= 539.74:
                return;
            if option_selected == "Lite 120" and new_price_float >= 573.36:
                return;
            if option_selected == "Storm 120" and new_price_float >= 674.68:
                return;
            if option_selected == "Bob 200" and new_price_float >= 694.82:
                return;
            if option_selected == "Lite 200" and new_price_float >= 716.71:
                return;
            if option_selected == "Storm 200 MONO" and new_price_float >= 774.88:
                return;
            if option_selected == "Storm 200" and new_price_float >= 845.87:
                return;


        location_url = f'https://www.mercadolivre.com.br/perfil/{loja.replace(" ", "+")}'

        yield scrapy.Request(url=location_url, callback=self.parse_location, meta={'url': response.url, 'name': name, 'price': new_price_float, 'qtde_parcelado': parcelado, 'price_parcelado': new_price_other_float, 'loja': loja, 'tipo': tipo })


    def finish(self, total_price, url, nomeFonte, loja, lugar):
        if option_selected == "Storm 40" and total_price >= 352.97:
            return;
        if option_selected == "Lite 60" and total_price >= 321.09:
            return;
        if option_selected == "Storm 60" and total_price >= 391.13:
            return;
        if option_selected == "Lite 70" and total_price >= 362.36:
            return;
        if option_selected == "Storm 70" and total_price >= 438.83:
            return;
        if option_selected == "Bob 90" and total_price >= 372.05:
            return;
        if option_selected == "Bob 120" and total_price >= 444.55:
            return;
        if option_selected == "Lite 120" and total_price >= 484.94:
            return;
        if option_selected == "Storm 120" and total_price >= 572.39:
            return;
        if option_selected == "Bob 200" and total_price >= 562.85:
            return;
        if option_selected == "Lite 200" and total_price >= 624.50:
            return;
        if option_selected == "Storm 200 MONO" and total_price >= 602.61:
            return;
        if option_selected == "Storm 200" and total_price >= 734.57:
            return;
        
        parcelado = self.get_price_previsto("NA")

        doc.add_paragraph(f'URL: {url}')
        doc.add_paragraph(f'Nome: {nomeFonte}')
        doc.add_paragraph(f'Preço: {total_price}')
        doc.add_paragraph(f'Preço Previsto: {parcelado}')
        doc.add_paragraph(f'Loja: {loja}')
        doc.add_paragraph('Tipo: ')
        doc.add_paragraph(f'Lugar: {lugar}')
        doc.add_paragraph("--------------------------------------------------------------------")
        doc.add_paragraph('')
        doc.save("dados_scrapy.docx")
            
            
        yield {
            'url': url,
            'name': nomeFonte,
            'price': total_price,
            'loja': loja,
            'tipo': "",
            'lugar': lugar
        }


    def parse_radicalson(self, response):
        loja = "RADICALSOM"
        lugar = "Artur nogueira, São Paulo."
        for i in response.xpath('//*[@id="root-app"]/div/div[3]/section/ol/li'):
            nomeFonte = i.xpath('.//div/div/div/div/a/h2/text()').get()
            price = i.xpath('.//div/div/div[3]/div/div[1]/div/div/div/div/span/span[2]/text()').get()
            cents = i.xpath('.//div/div/div[3]/div/div[1]/div/div/div/div/span/span[4]/text()').get()
            url = i.xpath('.//div/div/div[3]/div[2]/a/@href').get()
            nomeFonte = nomeFonte.lower()
            nomeFonte = unidecode.unidecode(nomeFonte)
            if not cents:
                cents = 0
            if price:
                price = price.replace('.', '')
                total_price = float(f"{price}.{cents}")
            if option_selected == "Storm 40":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "40a" in nomeFonte or "40" in nomeFonte or "40 amperes" in nomeFonte or "40amperes" in nomeFonte or "36a" in nomeFonte or "36" in nomeFonte or "36 amperes" in nomeFonte or "36amperes" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif option_selected == "Storm 60":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "60a" in nomeFonte or "60" in nomeFonte or "60 amperes" in nomeFonte or "60amperes" in nomeFonte or "60 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif option_selected == "Lite 60":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "60a" in nomeFonte or "60" in nomeFonte or "60 amperes" in nomeFonte or "60amperes" in nomeFonte or "60 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif option_selected == "Storm 70":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "70a" in nomeFonte or "70" in nomeFonte or "70 amperes" in nomeFonte or "70amperes" in nomeFonte or "70 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif option_selected == "Lite 70":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "70a" in nomeFonte or "70" in nomeFonte or "70 amperes" in nomeFonte or "70amperes" in nomeFonte or "70 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif option_selected == "Bob 90":
                if "bob" in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "90a" in nomeFonte or "90" in nomeFonte or "90 amperes" in nomeFonte or "90amperes" in nomeFonte or "90 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif option_selected == "Storm 120":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "120a" in nomeFonte or "120" in nomeFonte or "120 amperes" in nomeFonte or "120amperes" in nomeFonte or "120 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif option_selected == "Lite 120":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "120a" in nomeFonte or "120" in nomeFonte or "120 amperes" in nomeFonte or "120amperes" in nomeFonte or "120 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif option_selected == "Bob 120":
                if "bob" in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "120a" in nomeFonte or "120" in nomeFonte or "120 amperes" in nomeFonte or "120amperes" in nomeFonte or "120 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif option_selected == "Storm 200":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif option_selected == "Storm 200 MONO":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif option_selected == "Lite 200":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif option_selected == "Bob 200":
                if "bob" in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                    
    def parse_lsdistribuidora(self, response):
        loja = "LS DISTRIBUIDORA"
        lugar = "Elísio Medrado, Bahia"
        for i in response.xpath('//*[@id="root-app"]/div/div[3]/section/ol/li'):
            nomeFonte = i.xpath('.//div/div/div/div/a/h2/text()').get()
            price = i.xpath('.//div/div/div[3]/div/div[1]/div/div/div/div/span/span[2]/text()').get()
            cents = i.xpath('.//div/div/div[3]/div/div[1]/div/div/div/div/span/span[4]/text()').get()
            url = i.xpath('.//div/div/div[3]/div[2]/a/@href').get()
            nomeFonte = nomeFonte.lower()
            nomeFonte = unidecode.unidecode(nomeFonte)
            if not cents:
                cents = 0
            if price:
                price = price.replace('.', '')
                total_price = float(f"{price}.{cents}")
            if option_selected == "Storm 40":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "40a" in nomeFonte or "40" in nomeFonte or "40 amperes" in nomeFonte or "40amperes" in nomeFonte or "36a" in nomeFonte or "36" in nomeFonte or "36 amperes" in nomeFonte or "36amperes" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif option_selected == "Storm 60":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "60a" in nomeFonte or "60" in nomeFonte or "60 amperes" in nomeFonte or "60amperes" in nomeFonte or "60 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif option_selected == "Lite 60":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "60a" in nomeFonte or "60" in nomeFonte or "60 amperes" in nomeFonte or "60amperes" in nomeFonte or "60 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif option_selected == "Storm 70":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "70a" in nomeFonte or "70" in nomeFonte or "70 amperes" in nomeFonte or "70amperes" in nomeFonte or "70 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif option_selected == "Lite 70":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "70a" in nomeFonte or "70" in nomeFonte or "70 amperes" in nomeFonte or "70amperes" in nomeFonte or "70 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif option_selected == "Bob 90":
                if "bob" in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "90a" in nomeFonte or "90" in nomeFonte or "90 amperes" in nomeFonte or "90amperes" in nomeFonte or "90 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif option_selected == "Storm 120":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "120a" in nomeFonte or "120" in nomeFonte or "120 amperes" in nomeFonte or "120amperes" in nomeFonte or "120 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif option_selected == "Lite 120":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "120a" in nomeFonte or "120" in nomeFonte or "120 amperes" in nomeFonte or "120amperes" in nomeFonte or "120 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif option_selected == "Bob 120":
                if "bob" in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "120a" in nomeFonte or "120" in nomeFonte or "120 amperes" in nomeFonte or "120amperes" in nomeFonte or "120 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif option_selected == "Storm 200":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif option_selected == "Storm 200 MONO":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif option_selected == "Lite 200":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif option_selected == "Bob 200":
                if "bob" in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)                

    
    def parse_bestonline(self, response):
        loja = "BESTONLINE"
        lugar = "Rosario, Santa Fe."
        for i in response.xpath('//li[@class="ui-search-layout__item shops__layout-item shops__layout-item ui-search-layout__stack"]'):
            nomeFonte = i.xpath('.//div/div/div/div/a/h2/text()').get()
            price = i.xpath('.//div/div/div[3]/div/div[1]/div/div/div/div/span/span[2]/text()').get()
            cents = i.xpath('.//div/div/div[3]/div/div[1]/div/div/div/div/span/span[4]/text()').get()
            url = i.xpath('.//div/div/div[3]/div[2]/a/@href').get()
            nomeFonte = nomeFonte.lower()
            nomeFonte = unidecode.unidecode(nomeFonte)
            if not cents:
                cents = 0
            if price:
                price = price.replace('.', '')
                total_price = float(f"{price}.{cents}")
            if option_selected == "Storm 40":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "40a" in nomeFonte or "40" in nomeFonte or "40 amperes" in nomeFonte or "40amperes" in nomeFonte or "36a" in nomeFonte or "36" in nomeFonte or "36 amperes" in nomeFonte or "36amperes" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif option_selected == "Storm 60":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "60a" in nomeFonte or "60" in nomeFonte or "60 amperes" in nomeFonte or "60amperes" in nomeFonte or "60 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif option_selected == "Lite 60":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "60a" in nomeFonte or "60" in nomeFonte or "60 amperes" in nomeFonte or "60amperes" in nomeFonte or "60 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif option_selected == "Storm 70":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "70a" in nomeFonte or "70" in nomeFonte or "70 amperes" in nomeFonte or "70amperes" in nomeFonte or "70 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif option_selected == "Lite 70":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "70a" in nomeFonte or "70" in nomeFonte or "70 amperes" in nomeFonte or "70amperes" in nomeFonte or "70 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif option_selected == "Bob 90":
                if "bob" in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "90a" in nomeFonte or "90" in nomeFonte or "90 amperes" in nomeFonte or "90amperes" in nomeFonte or "90 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif option_selected == "Storm 120":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "120a" in nomeFonte or "120" in nomeFonte or "120 amperes" in nomeFonte or "120amperes" in nomeFonte or "120 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif option_selected == "Lite 120":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "120a" in nomeFonte or "120" in nomeFonte or "120 amperes" in nomeFonte or "120amperes" in nomeFonte or "120 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif option_selected == "Bob 120":
                if "bob" in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "120a" in nomeFonte or "120" in nomeFonte or "120 amperes" in nomeFonte or "120amperes" in nomeFonte or "120 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif option_selected == "Storm 200":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif option_selected == "Storm 200 MONO":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif option_selected == "Lite 200":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif option_selected == "Bob 200":
                if "bob" in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
            
    
    def parse_renovonline(self, response):
        loja = "RENOV ONLINE"
        lugar = "São João da Boa Vista - SP"
        for i in response.xpath('//li[@class="ui-search-layout__item shops__layout-item shops__layout-item ui-search-layout__stack"]'):
            nomeFonte = i.xpath('.//div/div/div/div/a/h2/text()').get()
            price = i.xpath('.//div/div/div[3]/div/div[1]/div/div/div/div/span/span[2]/text()').get()
            cents = i.xpath('.//div/div/div[3]/div/div[1]/div/div/div/div/span/span[4]/text()').get()
            url = i.xpath('.//div/div/div[3]/div[1]/a/@href').get()
            nomeFonte = nomeFonte.lower()
            nomeFonte = unidecode.unidecode(nomeFonte)
            if not cents:
                cents = 0
            if price:
                price = price.replace('.', '')
                total_price = float(f"{price}.{cents}")
            if option_selected == "Storm 40":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "40a" in nomeFonte or "40" in nomeFonte or "40 amperes" in nomeFonte or "40amperes" in nomeFonte or "36a" in nomeFonte or "36" in nomeFonte or "36 amperes" in nomeFonte or "36amperes" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif option_selected == "Storm 60":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "60a" in nomeFonte or "60" in nomeFonte or "60 amperes" in nomeFonte or "60amperes" in nomeFonte or "60 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif option_selected == "Lite 60":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "60a" in nomeFonte or "60" in nomeFonte or "60 amperes" in nomeFonte or "60amperes" in nomeFonte or "60 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif option_selected == "Storm 70":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "70a" in nomeFonte or "70" in nomeFonte or "70 amperes" in nomeFonte or "70amperes" in nomeFonte or "70 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif option_selected == "Lite 70":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "70a" in nomeFonte or "70" in nomeFonte or "70 amperes" in nomeFonte or "70amperes" in nomeFonte or "70 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif option_selected == "Bob 90":
                if "bob" in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "90a" in nomeFonte or "90" in nomeFonte or "90 amperes" in nomeFonte or "90amperes" in nomeFonte or "90 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif option_selected == "Storm 120":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "120a" in nomeFonte or "120" in nomeFonte or "120 amperes" in nomeFonte or "120amperes" in nomeFonte or "120 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif option_selected == "Lite 120":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "120a" in nomeFonte or "120" in nomeFonte or "120 amperes" in nomeFonte or "120amperes" in nomeFonte or "120 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif option_selected == "Bob 120":
                if "bob" in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "120a" in nomeFonte or "120" in nomeFonte or "120 amperes" in nomeFonte or "120amperes" in nomeFonte or "120 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif option_selected == "Storm 200":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif option_selected == "Storm 200 MONO":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif option_selected == "Lite 200":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif option_selected == "Bob 200":
                if "bob" in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)                
        
    def parse_shoppratico(self, response):
        loja = "SHOPPRATICO"
        lugar = "Sorocaba, São Paulo."
        for i in response.xpath('//li[@class="ui-search-layout__item shops__layout-item shops__layout-item ui-search-layout__stack"]'):
            nomeFonte = i.xpath('.//div/div/div/div/a/h2/text()').get()
            price = i.xpath('.//div/div/div[3]/div/div[1]/div/div/div/div/span/span[2]/text()').get()
            cents = i.xpath('.//div/div/div[3]/div/div[1]/div/div/div/div/span/span[4]/text()').get()
            url = i.xpath('.//div/div/div[3]/div[2]/a/@href').get()
            nomeFonte = nomeFonte.lower()
            nomeFonte = unidecode.unidecode(nomeFonte)
            if not cents:
                cents = 0
            if price:
                price = price.replace('.', '')
                total_price = float(f"{price}.{cents}")
            if option_selected == "Storm 40":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "40a" in nomeFonte or "40" in nomeFonte or "40 amperes" in nomeFonte or "40amperes" in nomeFonte or "36a" in nomeFonte or "36" in nomeFonte or "36 amperes" in nomeFonte or "36amperes" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif option_selected == "Storm 60":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "60a" in nomeFonte or "60" in nomeFonte or "60 amperes" in nomeFonte or "60amperes" in nomeFonte or "60 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif option_selected == "Lite 60":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "60a" in nomeFonte or "60" in nomeFonte or "60 amperes" in nomeFonte or "60amperes" in nomeFonte or "60 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif option_selected == "Storm 70":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "70a" in nomeFonte or "70" in nomeFonte or "70 amperes" in nomeFonte or "70amperes" in nomeFonte or "70 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif option_selected == "Lite 70":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "70a" in nomeFonte or "70" in nomeFonte or "70 amperes" in nomeFonte or "70amperes" in nomeFonte or "70 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif option_selected == "Bob 90":
                if "bob" in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "90a" in nomeFonte or "90" in nomeFonte or "90 amperes" in nomeFonte or "90amperes" in nomeFonte or "90 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif option_selected == "Storm 120":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "120a" in nomeFonte or "120" in nomeFonte or "120 amperes" in nomeFonte or "120amperes" in nomeFonte or "120 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif option_selected == "Lite 120":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "120a" in nomeFonte or "120" in nomeFonte or "120 amperes" in nomeFonte or "120amperes" in nomeFonte or "120 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif option_selected == "Bob 120":
                if "bob" in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "120a" in nomeFonte or "120" in nomeFonte or "120 amperes" in nomeFonte or "120amperes" in nomeFonte or "120 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif option_selected == "Storm 200":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif option_selected == "Storm 200 MONO":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif option_selected == "Lite 200":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif option_selected == "Bob 200":
                if "bob" in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)       
        
    def get_price_previsto(self, tipo):
        if tipo == "Clássico":
            if option_selected == "Storm 40":
                return 402.80;#402.79
            if option_selected == "Lite 60":
                return 443.07;
            if option_selected == "Storm 60":
                return 364.95;
            if option_selected == "Lite 70":
                return 408.73;
            if option_selected == "Storm 70":
                return 493.42;
            if option_selected == "Bob 90":
                return 422.93;
            if option_selected == "Bob 120":
                return 499.46;
            if option_selected == "Lite 120":
                return 536.26;
            if option_selected == "Storm 120":
                return 634.40;
            if option_selected == "Bob 200":
                return 624.33;
            if option_selected == "Lite 200":
                return 681.83;
            if option_selected == "Storm 200 MONO":
                return 736.61;
            if option_selected == "Storm 200":
                return 805.59;
        if tipo == "Premium":
            if option_selected == "Storm 40":
                return 433.00;
            if option_selected == "Lite 60":
                return 390.43;
            if option_selected == "Storm 60":
                return 473.28;
            if option_selected == "Lite 70":
                return 434.42;
            if option_selected == "Storm 70":
                return 523.63;
            if option_selected == "Bob 90":
                return 443.07;
            if option_selected == "Bob 120":
                return 539.74;
            if option_selected == "Lite 120":
                return 573.36;
            if option_selected == "Storm 120":
                return 674.68;
            if option_selected == "Bob 200":
                return 694.82;
            if option_selected == "Lite 200":
                return 716.71;
            if option_selected == "Storm 200 MONO":
                return 774.88;
            if option_selected == "Storm 200":
                return 845.87;
        if tipo == "NA":
            if option_selected == "Storm 40":
                return 352.97;
            if option_selected == "Lite 60":
                return 321.09;
            if option_selected == "Storm 60":
                return 391.13;
            if option_selected == "Lite 70":
                return 362.36;
            if option_selected == "Storm 70":
                return 438.83;
            if option_selected == "Bob 90":
                return 372.05;
            if option_selected == "Bob 120":
                return 444.55;
            if option_selected == "Lite 120":
                return 484.94;
            if option_selected == "Storm 120":
                return 572.39;
            if option_selected == "Bob 200":
                return 562.85;
            if option_selected == "Lite 200":
                return 624.50;
            if option_selected == "Storm 200 MONO":
                return 602.61;
            if option_selected == "Storm 200":
                return 734.57;

    def parse_location(self, response):
        name = response.meta['name']
        url = response.meta['url']
        new_price_float = response.meta['price']
        tipo = response.meta['tipo']
        parcelado = self.get_price_previsto(tipo)
        loja = response.meta['loja']
        lugar = response.xpath('//*[@id="profile"]/div/div[2]/div[1]/div[3]/p/text()').get()


        doc.add_paragraph(f'URL: {url}')
        doc.add_paragraph(f'Nome: {name}')
        doc.add_paragraph(f'Preço: {new_price_float}')
        doc.add_paragraph(f'Preço Previsto: {parcelado}')
        doc.add_paragraph(f'Loja: {loja}')
        doc.add_paragraph(f'Tipo: {tipo}')
        doc.add_paragraph(f'Lugar: {lugar}')
        doc.add_paragraph("--------------------------------------------------------------------")
        doc.add_paragraph('')
        
        yield {
            'url': url,
            'name': name,
            'price': new_price_float,
            'price_previsto': parcelado,
            'loja': loja,
            'tipo': tipo,
            'lugar': lugar
        }
        doc.save("dados_scrapy.docx")

        
        
