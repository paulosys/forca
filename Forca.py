class ForcaException(Exception):
    def __init__(self, mensagem, metodo=''):
        super().__init__(mensagem)
        self.metodo = metodo

class Forca:
    def __init__(self, palavra: str, dica: str) -> None:
        self.__palavra = palavra
        self.__dica = dica
        self.__letrasAchadas = []
        self.__letrasDigitadas = []
        self.__descobriuPalavra = False
        self.__qntErros = 0
    
      
    def getQntdErros(self):
        return self.__qntErros
    
    def getDica(self):
        return self.__dica
    
    def descobriuPalavra(self):
        return self.__descobriuPalavra != False
    
    def verificarLetra(self, letra: str):
        if letra in self.__letrasDigitadas or letra in self.__letrasAchadas:
            raise ForcaException("A letra já foi jogada!", "verificarLetra")
        
        if len(letra) != 1:
            raise ForcaException("A letra deve ter apenas um caracter!", "verificarLetra")
        
        if not letra in self.__palavra:
            self.__letrasDigitadas.append(letra)
            self.__qntErros += 1
            raise ValueError("A letra não existe na palavra!", "verificarLetra")
    
    def __adicionarLetra(self, letra: str):

        if not letra in self.__letrasDigitadas:
            self.__letrasDigitadas.append(letra)

        self.__letrasAchadas.append(letra)
            
        if len(self.__letrasAchadas) == len(self.__palavra):
            self.__descobriuPalavra = True

    def __getForcaLetras(self) -> str:
        s = '\nPalavra: '
        for letra in self.__palavra:
            if letra in self.__letrasAchadas:
                s += f'{letra}, '
            else:
                s += f'_, '
        s += '\n'
        return s
    
    def __getLetrasDigitadas(self) -> str:
        s = '\nLetras Jogadas: ['
        for letra in self.__letrasDigitadas:
            s += f'{letra}, '
        s += ']\n'
            
        return s
    
    def __getLetrasAcharadas(self) -> str:
        s = '\nLetras Acertadas: ['
        for letra in self.__letrasAchadas:
            s += f'{letra}, '
        s += ']\n'
        return s
        
    def getForca(self) -> str:
        
        s = '\n'
        s += self.desenhar()
        s += self.__getLetrasDigitadas()
        s += self.__getLetrasAcharadas()
        s += 'Dica = ' + self.getDica()
        s += self.__getForcaLetras()
        
        return s
    
    def rodada(self, letra: str):
        
        self.__adicionarLetra(letra)
        print(self.getForca())
        
    def resetar(self):
        self.__letrasAchadas = []
        self.__letrasDigitadas = []
        self.__descobriuPalavra = False
        self.__qntErros = 0
        self.__palavra = input("Digite a palavra a ser descoberta: ")
        self.__dica = input("Digite a dica da palavra: ")

    def desenhar(self):
        
        s = '\n'
        
        s += '  ________\n'
        s += '  |/      |\n'

        if self.__qntErros == 0:
            s += '  |\n'
            s += '  |\n'
            s += '  |\n'

        if self.__qntErros == 1:
            s += '  |      (_)\n'
            s += '  |         \n'
            s += '  |         \n'
            
        elif self.__qntErros == 2:
            s += '  |      (_)\n'
            s += '  |       | \n'
            s += '  |         \n'

        elif self.__qntErros == 3:
            s += '  |      (_)\n'
            s += '  |      /| \n'
            s += '  |         \n'

        elif self.__qntErros == 4:
            s += '  |      (_)\n'
            s += '  |      /|\\\n'
            s += '  |         \n'
            
        elif self.__qntErros == 5:
            s += '  |      (_)\n'
            s += '  |      /|\\\n'
            s += '  |      /  \n'
            
        elif self.__qntErros == 6:
            s += '  |      (_)\n'
            s += '  |      /|\\\n'
            s += '  |      / \\\n'
            
        s += ' ----\n'
        
        return s

if __name__ == "__main__":
    forca = Forca("pao", "comida")
    forca.draw()