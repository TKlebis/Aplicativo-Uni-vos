# Aplicativo-Uni-vos
Sistema de Gestão de Contatos

# 🚀 APP Uni-vos - Sistema de Gestão
  
  [![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
  [![Kivy](https://img.shields.io/badge/Kivy-2.1+-green.svg)](https://kivy.org)
  [![Firebase](https://img.shields.io/badge/Firebase-Admin-orange.svg)](https://firebase.google.com)
  [![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)
</div>

## 📌 Visão Geral

O **PoliticApp** é uma solução completa para gestão de contatos e campanhas políticas, desenvolvida em Python com:

- Interface moderna com Kivy/KivyMD
- Banco de dados em tempo real com Firebase
- Análise de dados com gráficos interativos
- Integração com WhatsApp para disparos em massa
- Mapeamento geográfico de apoiadores

## ✨ Recursos Principais

✅ **Gestão de Contatos** - Cadastro completo de apoiadores com dados demográficos  
✅ **Análise de Dados** - Gráficos interativos de gênero e faixa etária  
✅ **Mapa Inteligente** - Visualização geográfica de apoiadores  
✅ **Disparo de Mensagens** - Integração com WhatsApp para campanhas  
✅ **Multi-nível de Acesso** - Diferentes perfis de usuário (Admin, Líder, Apoiador)  

## 🖼️ Screenshots

| Login Screen |
|--------------
![Login](https://github.com/user-attachments/assets/34f90397-4a30-4f0a-acd1-15a827a341b9)

| Dashboard   |
|--------------

![image](https://github.com/user-attachments/assets/c997ba91-4842-4a4b-9a11-998c5c6b050a)

| MAPA 
|--------------
![image](https://github.com/user-attachments/assets/6cd236e3-d984-4350-8fb8-ee18273a9edf)


## 🛠️ Tecnologias Utilizadas

- **Frontend**: Kivy + KivyMD (Interface multiplataforma)
- **Backend**: Python 3.8+
- **Banco de Dados**: Firebase Firestore (Tempo real)
- **Mapas**: MapView + OpenStreetMap
- **Gráficos**: Matplotlib integrado ao Kivy
- **WhatsApp**: API Oficial do Meta

## 🚀 Como Executar

## Pré-requisitos
- **Python 3.8 ou superior**

- **Conta no Firebase (gratuita)**

- **Dispositivo Windows ou Linux**


## Configure o ambiente virtual (recomendado):

```python
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
```

## Instale as dependências:
```python
pip install -r requirements.txt
```

## Configure o Firebase:

- **Crie um projeto no Firebase Console**

- **Gere uma chave de serviço (service-account-key.json)**

- **Coloque o arquivo na raiz do projeto**

## Execute o aplicativo:

```python
python main.py
```

# 💻 Trecho do Código: Integração com Firebase
```python
class FirebaseManager:
    """Singleton para gerenciar conexão com o Firebase"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            try:
                current_dir = os.path.dirname(os.path.abspath(__file__))
                cred_path = os.path.join(current_dir, "service-account-key.json")
                
                if not os.path.exists(cred_path):
                    raise FileNotFoundError(f"Arquivo de credenciais não encontrado em: {cred_path}")
                
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
                self._db = firestore.client()
                self._initialized = True
            except Exception as e:
                Logger.error(f"Firebase: Erro na inicialização - {str(e)}")

    @property
    def db(self):
        if not hasattr(self, '_db'):
            raise AttributeError("Banco de dados não inicializado")
        return self._db
```

# 🧠 Partes Complexas do Projeto

## 1. Gráficos Dinâmicos com Matplotlib no Kivy
**Desafio:** Integrar visualizações do Matplotlib no Kivy, que normalmente trabalha com OpenGL.

**Solução:** Conversão da figura para textura Kivy:

```python
def _criar_grafico(self, categorias, valores, cores):
    # Configura figura com fundo transparente
    fig = plt.figure(facecolor='none', dpi=100)
    fig.patch.set_alpha(0)
    ax = fig.add_subplot(111)
    ax.patch.set_alpha(0)
    
    # Cria gráfico de barras
    bars = ax.bar(categorias, valores, color=cores, width=0.5)
    
    # Converte para textura Kivy
    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    buf = canvas.buffer_rgba()
    img_array = np.frombuffer(buf, dtype=np.uint8)
    
    # Cria e retorna textura
    texture = Texture.create(size=canvas.get_width_height())
    texture.blit_buffer(img_array, colorfmt='rgba')
    plt.close(fig)
    return texture
```

## 2. Mapeamento Geográfico com Clusterização

**Desafio:** Exibir centenas de marcadores no mapa sem sobrecarga.

**Solução:** Clusterização dinâmica e ajuste de zoom:

```python
def ajustar_visao_do_mapa(self, pontos):
    """Ajusta zoom para englobar todos os marcadores"""
    lats = [p[0] for p in pontos]
    lons = [p[1] for p in pontos]
    
    # Calcula área de cobertura
    min_lat, max_lat = min(lats), max(lats)
    min_lon, max_lon = min(lons), max(lons)
    
    # Fórmula empírica para zoom ideal
    max_diff = max(max_lat - min_lat, max_lon - min_lon)
    zoom = max(10, min(18, round(15 - (max_diff * 8))))
    
    self.mapview.zoom = zoom
    self.mapview.center_on(
        min_lat + (max_lat - min_lat) / 2,
        min_lon + (max_lon - min_lon) / 2
    )
```

## 3. Disparo de Mensagens em Massa para WhatsApp

**Desafio:** Enviar mensagens para milhares de contatos sem bloquear a interface.

**Solução:** Thread paralela com feedback em tempo real:

```python
def enviar_mensagens(self, token, phone_id, template, genero, idade, cidade):
    def enviar():
        try:
            contatos_filtrados = self._filtrar_contatos(genero, idade, cidade)
            enviados = 0
            
            for contato in contatos_filtrados:
                response = requests.post(
                    f"https://graph.facebook.com/v17.0/{phone_id}/messages",
                    headers={"Authorization": f"Bearer {token}"},
                    json={
                        "messaging_product": "whatsapp",
                        "to": self._formatar_numero(contato['celular']),
                        "type": "template",
                        "template": {"name": template, "language": {"code": "pt_BR"}}
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    enviados += 1
                    Logger.info(f"Mensagem enviada para {contato['celular']}")
                
            Clock.schedule_once(lambda dt: self.mostrar_popup(
                f"Envio concluído!\nTotal: {len(contatos_filtrados)}\nEnviados: {enviados}"
            ))
            
        except Exception as e:
            Logger.error(f"Erro no envio: {str(e)}")
            Clock.schedule_once(lambda dt: self.mostrar_popup(f"Erro: {str(e)}"))

    # Inicia thread paralela
    Thread(target=enviar, daemon=True).start()
```

# 🏁 Conclusão

Este projeto demonstra habilidades avançadas em:

- **Integração multiplataforma com Kivy**

- **Banco de dados em tempo real com Firebase**

- **Visualização de dados profissional**

- **APIs complexas (WhatsApp Business)**

- **Padrões de arquitetura (Singleton, MVC)**
