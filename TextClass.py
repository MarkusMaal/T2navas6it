import pygame
pygame.font.init()

class TextClass:

    def __init__ (self, fontfamily = "Arial", textsize = 18, textlocation = [0, 0], text = "", textcolor = [255, 255, 255]):
        self.fontfamily = fontfamily
        self.textsize = textsize
        self.textlocation = textlocation
        self.text = text
        self.textcolor = textcolor

    def BlitText(self, screen):
        txtfont = pygame.font.SysFont(self.fontfamily, self.textsize)
        txt = txtfont.render(self.text, True, self.textcolor)
        screen.blit(txt, self.textlocation)
