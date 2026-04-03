# - AVISO -

O arquivo \`yolov3.weights\` (~240MB) é muito grande para o GitHub.
Baixe manualmente em: https://pjreddie.com/media/files/yolov3.weights
Coloque o arquivo na pasta \`yolo/\` antes de executar o jogo.
---
#
# 🎮 Caca ao Objeto - Visao Computacional com YOLO

Um jogo interativo que utiliza visao computacional para detectar objetos em tempo real atraves da webcam. O jogador deve mostrar os objetos solicitados para ganhar pontos e avancar de fase.

---

## 📚 Tecnologias Utilizadas

| Tecnologia | Funcao no Projeto |
|------------|-------------------|
| OpenCV (cv2) | Captura a imagem da webcam e processa os frames em tempo real |
| YOLOv3 | Rede neural responsavel por identificar e classificar os objetos (80 classes diferentes) |
| Pygame | Cria a interface grafica do jogo, menus, pontuacao e feedback visual |
| NumPy | Manipula arrays de pixels e dados matematicos do YOLO |

## 🎯 Como Funciona

1. OpenCV acessa a webcam e captura cada frame
2. YOLO analisa o frame e identifica objetos (ex: celular, livro, garrafa)
3. Pygame exibe a interface do jogo com:
   - Objetivo atual
   - Pontuacao
   - Progresso
   - Feedback em tempo real

---

## 🎮 Como Jogar

| Comando | Acao |
|---------|------|
| Qualquer tecla | Iniciar o jogo (tela inicial) |
| ESC | Sair do jogo |

### Regras:
1. Mostre o objeto solicitado na webcam
2. Aguarde o YOLO detectar e confirmar
3. Ganhe 10 pontos por objeto encontrado
4. Complete todos os objetos para vencer!

---

## 📦 Instalacao

### 1. Clone o repositorio
git clone https://github.com/seu-usuario/caca-ao-objeto.git
cd caca-ao-objeto

### 2. Instale as dependencias
pip install -r requirements.txt

### 3. Baixe os modelos YOLO

Os arquivos do YOLO precisam estar na pasta YOLO/:

- coco.names - Lista dos 80 objetos detectaveis
- yolov3.cfg - Configuracao da rede neural
- yolov3.weights - Pesos da rede (arquivo grande, ~240MB)

Download dos arquivos:
cd YOLO
curl -O https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names
curl -O https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg
curl -O https://pjreddie.com/media/files/yolov3.weights

### 4. Execute o jogo
python jogo.py

---

## 🧠 Objetos que o YOLO Detecta

O YOLO consegue detectar 80 tipos diferentes de objetos, incluindo:

pessoa, celular, televisao, livro, garrafa, mouse, teclado,
cadeira, mesa, copo, garfo, faca, colher, tigela, banana,
maca, sanduiche, pizza, donut, bolo, cachorro, gato, passaro,
carro, bicicleta, moto, onibus, trem, aviao, e muito mais...

O jogo pode ser facilmente adaptado para buscar qualquer um desses objetos!

---

## ⚙️ Configuracoes Tecnicas

| Configuracao | Valor | Motivo |
|--------------|-------|--------|
| Resolucao da camera | 320x240 | Melhor performance |
| Deteccao por segundo | 5x (a cada 0.2s) | Balanceamento entre precisao e fluidez |
| FPS do jogo | 60 | Interface suave |
| Confianca minima YOLO | 0.5 | Evita falsos positivos |

---

## 🔧 Personalizando o Jogo

Para mudar os objetos que o jogador precisa encontrar, edite a linha:

objetos_para_encontrar = ["cell phone", "book", "bottle"]

Para adicionar mais objetos:

objetos_para_encontrar = ["cell phone", "book", "bottle", "mouse", "keyboard"]

---

## 🐛 Solucao de Problemas

### Webcam nao encontrada
- Verifique se a webcam esta conectada
- Teste com outro aplicativo (Zoom, Teams)
- No codigo, tente trocar cv2.VideoCapture(0) para cv2.VideoCapture(1)

### YOLO nao carrega
- Verifique se os arquivos estao na pasta YOLO/
- Confirme se o arquivo yolov3.weights foi baixado completamente (~240MB)

### Jogo esta lento
- Reduza a resolucao da camera (ja esta em 320x240)
- Aumente o intervalo_deteccao para 0.3 ou 0.4

---

## 📝 Licenca

Este projeto esta sob a licenca MIT. Sinta-se livre para usar, modificar e distribuir.

---
