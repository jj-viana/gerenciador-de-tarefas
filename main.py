from sistema import Aplicacao
from interface import InterfaceGrafica

if __name__ == "__main__":
    sistema = Aplicacao()
    InterfaceGrafica(sistema).root.mainloop()