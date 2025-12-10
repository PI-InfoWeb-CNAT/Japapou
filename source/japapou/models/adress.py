from django.db import models # type: ignore
from django.conf import settings # type: ignore
import requests


class Endereco(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="enderecos" # Permite usar request.user.enderecos.all()
    )
    logradouro = models.CharField(max_length=255)
    numero = models.CharField(max_length=20)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100,)
    cep = models.CharField(max_length=9) # Formato '00000-000'

    lat_destino = models.FloatField(blank=True, null=True)
    lon_destino = models.FloatField(blank=True, null=True)
    
    # Um "apelido" para o endereço, ex: "Casa", "Trabalho"
    apelido = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"

    def __str__(self):
        # Retorna o endereço formatado
        return f"{self.logradouro}, {self.numero} - {self.bairro}"
    
    def save(self, *args, **kwargs):
        cep_limpo = self.cep.replace('-', '').replace('.', '').strip() # limpa o cep tirando os traços e pontos que o usuario pode vir a colocar

        if cep_limpo and not self.lat_destino:

            try:

                resposta = requests.get(f"https://viacep.com.br/ws/{cep_limpo}/json/")
                dados_cep = resposta.json()

                if "erro" not in dados_cep:
                    logradouro = dados_cep['logradouro']
                    bairro = dados_cep['bairro']
                    cidade_api = dados_cep['localidade']
                    uf = dados_cep['uf']
                
                    TOMTOM_KEY = settings.TOMTOM_KEY

                    print(f"Consultando TomTom para: {logradouro}, {self.numero} - {cidade_api}...")
                    
                    url_tomtom = f"https://api.tomtom.com/search/2/structuredGeocode.json"

                    params = {
                        'key': TOMTOM_KEY,
                        'countryCode': 'BR',
                        'limit': 1,
                        'streetNumber': self.numero,  # O número exato da casa
                        'streetName': logradouro,     # Nome da rua vindo do ViaCEP
                        'municipality': cidade_api,   # Cidade (Natal)
                        'postalCode': cep_limpo,      # CEP
                        'language': 'pt-BR'
                    }

                    try:
                        resp_tomtom = requests.get(url_tomtom, params)

                        if resp_tomtom.status_code == 200:
                            dados_mapa = resp_tomtom.json()
                            resultados = dados_mapa.get('results', [])

                            if len(resultados) > 0:
                                        local = resultados[0]
                                        posicao = local['position']
                                        
                                        # Verifica a qualidade do resultado
                                        tipo_match = local.get('matchType') # Ex: 'Point Address' (Exato) ou 'Street' (Rua)
                                        
                                        self.lat_destino = float(posicao['lat'])
                                        self.lon_destino = float(posicao['lon'])
                                        
                                        print(f"Sucesso TomTom! Tipo de precisão: {tipo_match}")
                                        print(f"Endereço detectado: {local.get('address', {}).get('freeformAddress')}")
                            else:
                                print("A TomTom não encontrou este endereço específico.")
                                # Opcional: Fallback para o centro da rua se não achar o número
                        
                        else:
                            print(f"Erro na API TomTom: {resp_tomtom.status_code} - {resp_tomtom.text}")
                    
                    except Exception as e:
                                print(f"Erro de conexão com TomTom: {e}")
                
                else:
                    print("CEP inválido no ViaCEP.")
            
            except Exception as e:
                    print(f"Erro geral: {e}")
            
        super(Endereco, self).save(*args, **kwargs)
            
        
