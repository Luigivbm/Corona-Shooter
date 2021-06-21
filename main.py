import pygame
import math
import random

pygame.init()


sw = 800
sh = 800

#define as imagens do jogo
bg = pygame.image.load('img/Fundo.png')
introbg = pygame.image.load('img/intro.png')
iconeimg = pygame.image.load('img/icone.png')
covidcariocaimg = pygame.image.load('img/covid38.png')
osmosisjones = pygame.image.load('img/osmosisjones.png')
curaimg = pygame.image.load('img/cura.png')
covidpequeno = pygame.image.load('img/covid19-50.png')
covidmedio = pygame.image.load('img/covid19-100.png')
covidgrande = pygame.image.load('img/covid19-150.png')
tirodois = pygame.image.load('img/tirocovid.png')
tiroum = pygame.image.load('img/tiro.png')

# Define a Fonte
	
font = pygame.font.Font('fonts/font.otf', 30)

#define os sons do jogo
tirosom = pygame.mixer.Sound('sons/tirosom.wav')
boomalto = pygame.mixer.Sound('sons/boomalto.wav')
boomsom = pygame.mixer.Sound('sons/boomsom.wav')
aifizdodoi = pygame.mixer.Sound('sons/AiFizDodoi.wav')
shhhesegredo = pygame.mixer.Sound('sons/enfieiumeastereggnojogo.wav')
trilhasonora = pygame.mixer.music.load('sons/somzin.wav')


#diminui o som do jogo pra não surdo
tirosom.set_volume(.25)
boomalto.set_volume(.25)
boomsom.set_volume(.25)

#define icone,nome e o tamanho da janela , alem de chamar o clock q vai ser usado pra definir o fps mais tarde
pygame.display.set_icon(iconeimg)
pygame.display.set_caption('Osmosis Jones contra  o Covid-19')
win = pygame.display.set_mode((sw, sh))
clock = pygame.time.Clock()
clock.tick(75)

# define  parâmetros inicias  
morreu = False
vidas = 0
pontuacao = 0
metralha = False
badumtiss = -1
somligado = True
maiorpontuacao = 0




# define a classe jogador e cria as funções de movimento
class Player(object):
    def __init__(self):
        self.img = osmosisjones
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.x = sw//2
        self.y = sh//2
        self.angle = 0
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (((self.x-2) + self.cosine * self.h // 2), (self.y - self.sine * self.h // 2))

    def draw(self, win):

        win.blit(self.rotatedSurf, self.rotatedRect)

    def vaiprolado(self):
        self.angle += 5
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (((self.x-2) + self.cosine * self.h // 2), (self.y - self.sine * self.h // 2))

    def vaiprooutrolado(self):
        self.angle -= 5
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (((self.x-2) + self.cosine * self.h // 2), (self.y - self.sine * self.h // 2))

    def vaipratras(self):
        self.x -= self.cosine * 6
        self.y += self.sine * 6
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (((self.x-2) + self.cosine * self.h // 2), (self.y - self.sine * self.h // 2))

    def vaiprafrente(self):
        self.x += self.cosine * 6
        self.y -= self.sine * 6
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (((self.x-2) + self.cosine * self.h // 2), (self.y - self.sine * self.h // 2))

    def epamudeidelocal(self):
        if self.x > sw + 50:
            self.x = 0
        elif self.x < 0 - self.w:
            self.x = sw
        elif self.y < -50:
            self.y = sh
        elif self.y > sh + 50:
            self.y = 0

# define o tiro do player e faz com q ele siga na direção q o player esta olhando
class Tiro(object):
    def __init__(self):
        self.point = player.head
        self.x, self.y = self.point
        self.w = 4
        self.h = 4
        self.c = player.cosine
        self.s = player.sine
        self.xv = self.c * 10
        self.yv = self.s * 10

    def move(self):
        self.x += self.xv
        self.y -= self.yv

    def draw(self, win):
        pygame.draw.rect(win, (255, 213, 0),[self.x, self.y, self.w, self.h])
        #win.blit(tiroum,[self.x, self.y, self.w, self.h])

    def checkOffScreen(self):
        if self.x < -50 or self.x > 2*sw or self.y > 2*sh or self.y < -50:
            return True

# cria o Covid e faz com q ele va em uma direção aleatoria alem de determinar um dos 3 tamanhos de covid  
class Covid(object):
    def __init__(self, rank):
        self.rank = rank
        if self.rank == 1:
            self.image = covidpequeno
        elif self.rank == 2:
            self.image = covidmedio
        else:
            self.image = covidgrande
        self.w = 50 * rank
        self.h = 50 * rank
        self.ranPoint = random.choice([(random.randrange(0, sw-self.w), random.choice([-1*self.h - 5, sh + 5])), (random.choice([-1*self.w - 5, sw + 5]), random.randrange(0, sh - self.h))])
        self.x, self.y = self.ranPoint
        if self.x < sw//2:
            self.xdir = 1
        else:
            self.xdir = -1
        if self.y < sh//2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xv = self.xdir * random.randrange(1,3)
        self.yv = self.ydir * random.randrange(1,3)

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

# cria um power-up q faz q a arma do player vire uma metralhadora
class Cura(object):
    def __init__(self):
        self.img = curaimg
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.ranPoint = random.choice([(random.randrange(0, sw - self.w), random.choice([-1 * self.h - 5, sh + 5])),
                                       (random.choice([-1 * self.w - 5, sw + 5]), random.randrange(0, sh - self.h))])
        self.x, self.y = self.ranPoint
        if self.x < sw//2:
            self.xdir = 1
        else:
            self.xdir = -1
        if self.y < sh//2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xv = self.xdir * 2
        self.yv = self.ydir * 2

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

# Cria um covid verde e faz com q ele va em uma direção aleatoria (diferentemente do covid normal esse só vem em um tamanho)
class CovidCarioca(object):
    def __init__(self):
        self.img = covidcariocaimg
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.ranPoint = random.choice([(random.randrange(0, sw - self.w), random.choice([-1 * self.h - 5, sh + 5])),
                                       (random.choice([-1 * self.w - 5, sw + 5]), random.randrange(0, sh - self.h))])
        self.x, self.y = self.ranPoint
        if self.x < sw//2:
            self.xdir = 1
        else:
            self.xdir = -1
        if self.y < sh//2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xv = self.xdir * 2
        self.yv = self.ydir * 2

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

# já q é carioca o q não pode faltar é tiro , então essa classe faz com q o covid verde tenha a abilidade de atirar
class TiroCovid(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 4
        self.h = 4
		#                                      ↓ Esse player esta com o Y por 2 pq senão o covid carioca fica muito apelão, dessa forma (às vezes) ele n atira diretamente em vc
        self.dx, self.dy = player.x - self.x, player.y//2 - self.y
        self.dist = math.hypot(self.dx, self.dy)
        self.dx, self.dy = self.dx / self.dist, self.dy / self.dist
        self.xv = self.dx * 5
        self.yv = self.dy * 5


    def draw(self, win):
        pygame.draw.rect(win, (132, 255, 0), [self.x, self.y, self.w, self.h])
        #win.blit(tirodois,[self.x, self.y, self.w, self.h])



def atualizatela():
    win.blit(bg, (0,0))
    numerodevidas = font.render('Vidas: ' + str(vidas), 1, (60,0,0))
    textopontuacao = font.render('Pontuação: ' + str(pontuacao), 1, (60,0,0))
    highScoreText = font.render('Recorde de Pontuação: ' + str(maiorpontuacao), 1, (60,0,0))

    player.draw(win)
    for a in covid:
        a.draw(win)
    for b in tiroplayer:
        b.draw(win)
    for s in cura:
        s.draw(win)
    for a in covidcarioca:
        a.draw(win)
    for b in tirocovid:
        b.draw(win)
    # faz a barra do tempo do power up
    if metralha:
        pygame.draw.rect(win, (241, 158, 54), [sw//2 - 51, 19, 102, 22])
        pygame.draw.rect(win, (251, 230, 78), [sw//2 - 50, 20, 100 - 100*(count - badumtiss)/500, 20])

    if morreu:
        win.blit(introbg, (0,0))
        
    else:
        win.blit(textopontuacao, (sw- textopontuacao.get_width() - 25, 25))
        win.blit(numerodevidas, (25, 25))
        win.blit(highScoreText, (sw - highScoreText.get_width() -25, 35 + textopontuacao.get_height()))
    pygame.display.update()



player = Player()
tiroplayer = []
covid = []
count = 0
cura = []
covidcarioca = []
tirocovid = []
rodando = True
while rodando:

    if vidas >= 1:
        pygame.mixer.music.stop()
    
    clock.tick(75)
    count += 1
    if not morreu:
        # define a chance do spawn dos tipos de covid e do power up
        if count % 50 == 0:
            ran = random.choice([1,1,1,2,2,3])
            covid.append(Covid(ran))
        if count % 1000 == 0:
            cura.append(Cura())
        if count % 750 == 0:
            covidcarioca.append(CovidCarioca())
        for i, a in enumerate(covidcarioca):
            a.x += a.xv
            a.y += a.yv
            if a.x > sw + 150 or a.x + a.w < -100 or a.y > sh + 150 or a.y + a.h < -100:
                covidcarioca.pop(i)
            if count % 60 == 0:
                tirocovid.append(TiroCovid(a.x + a.w//2, a.y + a.h//2))

            for b in tiroplayer:
                if (b.x >= a.x and b.x <= a.x + a.w) or b.x + b.w >= a.x and b.x + b.w <= a.x + a.w:
                    if (b.y >= a.y and b.y <= a.y + a.h) or b.y + b.h >= a.y and b.y + b.h <= a.y + a.h:
                        covidcarioca.pop(i)
                        if somligado:
                            boomalto.play()
                        pontuacao += 50
                        break

        for i, b in enumerate(tirocovid):
            b.x += b.xv
            b.y += b.yv
            # comfere se o tiro e atingiu o player
            if (b.x >= player.x - player.w//2 and b.x <= player.x + player.w//2) or b.x + b.w >= player.x - player.w//2 and b.x + b.w <= player.x + player.w//2:
                if (b.y >= player.y-player.h//2 and b.y <= player.y + player.h//2) or b.y + b.h >= player.y - player.h//2 and b.y + b.h <= player.y + player.h//2:
                    if vidas ==1:
                        shhhesegredo.play()
                    vidas -= 1
                    aifizdodoi.play()
                    tirocovid.pop(i)
                    
                    break

        player.epamudeidelocal()
        for b in tiroplayer:
            b.move()
            if b.checkOffScreen():
                tiroplayer.pop(tiroplayer.index(b))


        for a in covid:
            a.x += a.xv
            a.y += a.yv
            # comfere se o tiro e atingiu o covid
            if (a.x >= player.x - player.w//2 and a.x <= player.x + player.w//2) or (a.x + a.w <= player.x + player.w//2 and a.x + a.w >= player.x - player.w//2):
                if(a.y >= player.y - player.h//2 and a.y <= player.y + player.h//2) or (a.y  +a.h >= player.y - player.h//2 and a.y + a.h <= player.y + player.h//2):
                    vidas -= 1
                    covid.pop(covid.index(a))
                    if somligado:
                        aifizdodoi.play()
                    break

            # bullet collision
            for b in tiroplayer:
                            # comfere se o tiro e atingiu o covid
                if (b.x >= a.x and b.x <= a.x + a.w) or b.x + b.w >= a.x and b.x + b.w <= a.x + a.w:
                    if (b.y >= a.y and b.y <= a.y + a.h) or b.y + b.h >= a.y and b.y + b.h <= a.y + a.h:
                        if a.rank == 3:
                            if somligado:
                                boomalto.play()
                            pontuacao += 10
                            na1 = Covid(2)
                            na2 = Covid(2)
                            na1.x = a.x
                            na2.x = a.x
                            na1.y = a.y
                            na2.y = a.y
                            covid.append(na1)
                            covid.append(na2)
                        elif a.rank == 2:
                            if somligado:
                                boomsom.play()
                            pontuacao += 20
                            na1 = Covid(1)
                            na2 = Covid(1)
                            na1.x = a.x
                            na2.x = a.x
                            na1.y = a.y
                            na2.y = a.y
                            covid.append(na1)
                            covid.append(na2)
                        else:
                            pontuacao += 30
                            if somligado:
                                boomsom.play()
                        covid.pop(covid.index(a))
                        tiroplayer.pop(tiroplayer.index(b))
                        break

        for s in cura:
            s.x += s.xv
            s.y += s.yv
            if s.x < -100 - s.w or s.x > sw + 100 or s.y > sh + 100 or s.y < -100 - s.h:
                cura.pop(cura.index(s))
                break
            for b in tiroplayer:
                if (b.x >= s.x and b.x <= s.x + s.w) or b.x + b.w >= s.x and b.x + b.w <= s.x + s.w:
                    if (b.y >= s.y and b.y <= s.y + s.h) or b.y + b.h >= s.y and b.y + b.h <= s.y + s.h:
                        metralha = True
                        badumtiss = count
                        cura.pop(cura.index(s))
                        tiroplayer.pop(tiroplayer.index(b))
                        break

        if vidas <= 0:
            morreu = True
            metralha = False
            pygame.mixer.music.play(loops = -1)
        
        # tempo da metralha (n sei pq usei esse nome pra variavel mas fiquei com Preguiça de mudar)
        if badumtiss != -1:
            if count - badumtiss > 500:
                metralha = False
                badumtiss = -1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.vaiprolado()
        if keys[pygame.K_RIGHT]:
            player.vaiprooutrolado()
        if keys[pygame.K_UP]:
            player.vaiprafrente()
        if keys[pygame.K_DOWN]:
            player.vaipratras()
        if keys[pygame.K_SPACE]:
            if metralha:
                tiroplayer.append(Tiro())
                if somligado:
                    tirosom.play()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not morreu:
                    if not metralha:
                        tiroplayer.append(Tiro())
                        if somligado:
                            tirosom.play()
            if event.key == pygame.K_m:
                somligado = not somligado
                
            if event.key == pygame.K_TAB:
                if morreu:

                    morreu = False
                    vidas = 5
                    covid.clear()
                    covidcarioca.clear()
                    tirocovid.clear()
                    cura.clear()
                    if pontuacao > maiorpontuacao:
                        maiorpontuacao = pontuacao
                    pontuacao = 0


    atualizatela()
pygame.quit()
