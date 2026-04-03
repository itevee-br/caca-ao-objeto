import cv2
import numpy as np
import pygame
import sys
import os
import time

print("=== Jogo: Caca ao Objeto (Versao Otimizada) ===\n")

# ===== INICIALIZAR PYGAME PRIMEIRO =====
pygame.init()

# Configurar tela
largura_camera = 320
altura_camera = 240
largura_interface = 350
largura_total = largura_camera + largura_interface
altura_total = 600

tela = pygame.display.set_mode((largura_total, altura_total))
pygame.display.set_caption("Caca ao Objeto - Carregando...")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)
CINZA = (128, 128, 128)

fonte = pygame.font.Font(None, 36)
fonte_pequena = pygame.font.Font(None, 24)

def mostrar_carregamento(mensagem, progresso=0):
    """Mostra tela de carregamento com mensagem e barra (centralizado)"""
    tela.fill(PRETO)
    
    # Tudo centralizado na tela inteira
    centro_x = largura_total // 2
    
    # Titulo
    titulo = fonte.render("CARREGANDO...", True, AMARELO)
    tela.blit(titulo, (centro_x - titulo.get_width() // 2, 200))
    
    # Mensagem
    texto = fonte_pequena.render(mensagem, True, BRANCO)
    tela.blit(texto, (centro_x - texto.get_width() // 2, 280))
    
    # Barra de progresso
    barra_largura = 400
    barra_altura = 20
    barra_x = centro_x - barra_largura // 2
    barra_y = 330
    
    # Fundo da barra
    pygame.draw.rect(tela, CINZA, (barra_x, barra_y, barra_largura, barra_altura))
    # Progresso
    pygame.draw.rect(tela, VERDE, (barra_x, barra_y, int(barra_largura * progresso), barra_altura))
    
    # Percentual
    percentual = fonte_pequena.render(f"{int(progresso * 100)}%", True, BRANCO)
    tela.blit(percentual, (centro_x - percentual.get_width() // 2, barra_y + barra_altura + 5))
    
    pygame.display.flip()

# ===== TELA DE CARREGAMENTO =====
mostrar_carregamento("Inicializando...", 0.05)
pygame.time.wait(100)

# ===== CARREGAR YOLO =====
mostrar_carregamento("Carregando YOLO...", 0.2)
pygame.time.wait(100)

# Caminho relativo (funciona em qualquer computador)
base_path = os.path.join(os.path.dirname(__file__), "YOLO")
# ou se a pasta se chamar "yolo" (minusculo)
# base_path = os.path.join(os.path.dirname(__file__), "yolo")

coco_names = os.path.join(base_path, "coco.names")
yolo_cfg = os.path.join(base_path, "yolov3.cfg")
yolo_weights = os.path.join(base_path, "yolov3.weights")

# Carregar nomes
mostrar_carregamento("Carregando lista de objetos...", 0.35)
with open(coco_names, "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Carregar rede YOLO
mostrar_carregamento("Carregando rede neural (pode levar alguns segundos)...", 0.5)
net = cv2.dnn.readNet(yolo_weights, yolo_cfg)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

mostrar_carregamento("Configurando camadas da rede...", 0.7)
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# ===== ABRIR WEBCAM =====
mostrar_carregamento("Abrindo webcam...", 0.85)
webcam = cv2.VideoCapture(0)
webcam.set(cv2.CAP_PROP_FRAME_WIDTH, largura_camera)
webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, altura_camera)

if not webcam.isOpened():
    mostrar_carregamento("ERRO: Webcam nao encontrada!", 1.0)
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

# ===== CONFIGURACOES DO JOGO =====
mostrar_carregamento("Preparando o jogo...", 0.95)

# Objetos do jogo
OBJETIVOS = {
    "cell phone": "📱 Celular",
    "tvmonitor": "📺 Televisao",
    "book": "📖 Livro",
    "bottle": "🍶 Garrafa",
    "mouse": "🖱️ Mouse",
    "keyboard": "⌨️ Teclado"
}

# Objetos para encontrar
objetos_para_encontrar = ["cell phone","mouse","tvmonitor"]
objetos_encontrados = set()
pontuacao = 0
objetivo_atual = objetos_para_encontrar[0]

pygame.display.set_caption("Jogo - teste yolo e cv2")

# Controle de tempo para deteccao
ultima_deteccao = 0
intervalo_deteccao = 0.2  # 200ms
objetos_detectados = []

# Loop do jogo
clock = pygame.time.Clock()
rodando = True
ultimo_aviso = ""
tempo_aviso = 0

def mostrar_mensagem(msg, cor, tempo=2):
    global ultimo_aviso, tempo_aviso
    ultimo_aviso = msg
    tempo_aviso = pygame.time.get_ticks() + (tempo * 1000)

# Tela de inicio (opcional)
tela.fill(PRETO)
texto_inicio = fonte.render("PRESSIONE QUALQUER TECLA PARA COMECAR", True, VERDE)
tela.blit(texto_inicio, (largura_total // 2 - texto_inicio.get_width() // 2, altura_total // 2))
pygame.display.flip()

esperando = True
while esperando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            esperando = False

print("Jogo iniciado!")
print(f"Objetivo: Encontre {OBJETIVOS.get(objetivo_atual, objetivo_atual)}")
print("Pressione ESC para sair\n")

while rodando:
    # Capturar frame da webcam
    ret, frame = webcam.read()
    if not ret:
        break
    
    # Redimensionar frame
    frame_redimensionado = cv2.resize(frame, (largura_camera, altura_camera))
    
    tempo_atual = time.time()
    
    # Detectar objetos apenas no intervalo definido
    if tempo_atual - ultima_deteccao >= intervalo_deteccao:
        ultima_deteccao = tempo_atual
        objetos_detectados = []
        
        # Processar frame com YOLO
        height, width, _ = frame_redimensionado.shape
        blob = cv2.dnn.blobFromImage(frame_redimensionado, 0.00392, (320, 320), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outputs = net.forward(output_layers)
        
        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                
                if confidence > 0.5:
                    label = classes[class_id]
                    objetos_detectados.append(label)
                    
                    # Se detectou o objetivo atual
                    if label == objetivo_atual and label not in objetos_encontrados:
                        objetos_encontrados.add(label)
                        pontuacao += 10
                        mostrar_mensagem(f"✅ +10 pontos! Encontrou {OBJETIVOS.get(label, label)}!", VERDE)
                        
                        # Proximo objetivo
                        if len(objetos_encontrados) < len(objetos_para_encontrar):
                            objetivo_atual = objetos_para_encontrar[len(objetos_encontrados)]
                            mostrar_mensagem(f"🎯 Novo objetivo: {OBJETIVOS.get(objetivo_atual, objetivo_atual)}!", AMARELO)
                        else:
                            mostrar_mensagem("🏆 PARABENS! VOCE VENCEU! 🏆", AMARELO, 3)
    
    # Converter frame para Pygame
    frame_rgb = cv2.cvtColor(frame_redimensionado, cv2.COLOR_BGR2RGB)
    frame_surface = pygame.surfarray.make_surface(np.rot90(frame_rgb))
    
    # ===== DESENHAR TELA PYGAME =====
    tela.fill(PRETO)
    
    # Mostrar a webcam
    tela.blit(frame_surface, (0, 0))
    
    # Interface do jogo
    x_interface = largura_camera + 10
    
    # Titulo
    titulo = pygame.font.Font(None, 36).render("Encontre os objetos!", True, BRANCO)
    tela.blit(titulo, (x_interface, 20))
    
    # Objetivo atual
    texto_objetivo = pygame.font.Font(None, 24).render(f"Objetivo:", True, AMARELO)
    tela.blit(texto_objetivo, (x_interface, 70))
    texto_objeto = pygame.font.Font(None, 24).render(f"{OBJETIVOS.get(objetivo_atual, objetivo_atual)}", True, AMARELO)
    tela.blit(texto_objeto, (x_interface, 95))
    
    # Pontuacao
    texto_pontos = pygame.font.Font(None, 24).render(f"Pontos: {pontuacao}", True, VERDE)
    tela.blit(texto_pontos, (x_interface, 140))
    
    # Progresso
    texto_progresso = pygame.font.Font(None, 24).render(f"Progresso: {len(objetos_encontrados)}/{len(objetos_para_encontrar)}", True, BRANCO)
    tela.blit(texto_progresso, (x_interface, 180))
    
    # Objetos encontrados
    y = 230
    for obj in objetos_encontrados:
        texto = pygame.font.Font(None, 24).render(f"✓ {OBJETIVOS.get(obj, obj)}", True, VERDE)
        tela.blit(texto, (x_interface, y))
        y += 28
    
    # Objetos restantes
    for obj in objetos_para_encontrar:
        if obj not in objetos_encontrados:
            texto = pygame.font.Font(None, 24).render(f"❌ {OBJETIVOS.get(obj, obj)}", True, VERMELHO)
            tela.blit(texto, (x_interface, y))
            y += 28
    
    # Objetos detectados
    y = 380
    texto_detectados = pygame.font.Font(None, 24).render("Detectados agora:", True, AZUL)
    tela.blit(texto_detectados, (x_interface, y))
    y += 25
    
    objetos_unicos = list(set(objetos_detectados))
    for obj in objetos_unicos[:4]:
        if obj in OBJETIVOS:
            texto = pygame.font.Font(None, 22).render(f"• {OBJETIVOS[obj]}", True, AZUL)
            tela.blit(texto, (x_interface, y))
            y += 22
    
    # Mensagem de feedback
    if ultimo_aviso and pygame.time.get_ticks() < tempo_aviso:
        texto_aviso = pygame.font.Font(None, 24).render(ultimo_aviso, True, VERDE)
        tela.blit(texto_aviso, (x_interface, altura_total - 80))
    
    # Instrucao
    instrucao = pygame.font.Font(None, 24).render("Mostre o objeto na camera!", True, BRANCO)
    tela.blit(instrucao, (x_interface, altura_total - 45))
    instrucao2 = pygame.font.Font(None, 24).render("ESQ para fechar", True, VERMELHO)
    tela.blit(instrucao2, (x_interface, altura_total - 25))
    
    pygame.display.flip()
    
    # Verificar vitoria
    if len(objetos_encontrados) >= len(objetos_para_encontrar):
        texto_vitoria = pygame.font.Font(None, 36).render("VOCE VENCEU!", True, AMARELO)
        tela.blit(texto_vitoria, (x_interface, altura_total // 2 - 100))
        pygame.display.flip()
        pygame.time.wait(3000)
        break
    
    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                rodando = False
    
    clock.tick(60)

# Finalizar
webcam.release()
cv2.destroyAllWindows()
pygame.quit()

print("\n=== FIM DO JOGO ===")
print(f"Pontuacao final: {pontuacao}")
print("Objetos encontrados:")
for obj in objetos_encontrados:
    print(f"  - {OBJETIVOS.get(obj, obj)}")