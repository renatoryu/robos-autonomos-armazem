# Importações e inicializações
import time
import heapq # usado para a fila de prioridade do algoritmo A*
import os
from typing import List, Tuple, Optional, Dict
from colorama import Fore, Style, init # cores no terminal
from enum import Enum, auto # enumeração para status do robô

# Inicializa colorama para colorir o terminal
init(autoreset=True)

# Constantes e tipos
ROBOS_ID = ['R', 'S']
ITEM = 'I'
ENTREGA = 'E'
PAREDE = '#'
CAMINHO = '.'

DELAY_INICIAL = 5.0
DELAY_PASSO = 1.0

CORES = {
    'R': Fore.GREEN,
    'S': Fore.MAGENTA,
    ITEM: Fore.YELLOW,
    ENTREGA: Fore.CYAN,
    PAREDE: Fore.LIGHTBLACK_EX,
    CAMINHO: Fore.WHITE,
    'TRILHA_R': Fore.GREEN,
    'TRILHA_S': Fore.MAGENTA,
}

# Mapa da simulação
MAPA_LAYOUT = [
    "#R.......S#",
    "#.........#",
    "#.........#",
    "#I.......I#",
    "#####.#####",
    "#....E....#",
    "###########"
]

# Inicializar posição e caminho
Posicao = Tuple[int, int]
Caminho = List[Posicao]

# Status do Robô
class StatusRobo(Enum):
    OCIOSO = auto()
    INDO_PARA_ITEM = auto()
    INDO_PARA_ENTREGA = auto()
    CONCLUIDO = auto()

# Funções Auxiliares
def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

def mostrar_banner():
    limpar_tela()
    print(f" ╔════════════════════════════════════════════════╗ ")
    print(" ║          SIMULADOR DE ARMAZÉM DINÂMICO         ║ ")
    print(f" ╚════════════════════════════════════════════════╝ {Style.RESET_ALL}\n")
    
    legenda = [
        f"{CORES['R']}R/S{Style.RESET_ALL}: Robôs",
        f"{CORES[ITEM]}I{Style.RESET_ALL}: Item",
        f"{CORES[ENTREGA]}E{Style.RESET_ALL}: Entrega",
        f"{CORES[PAREDE]}#{Style.RESET_ALL}: Parede"
    ]
    print("Legenda: " + " | ".join(legenda) + "\n")
    time.sleep(DELAY_INICIAL)

# Função heurística para A* (Algoritmo para Busca de Caminho)
def heuristica(a: Posicao, b: Posicao) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) # retorna a distância estimada entre duas posições (usada no A*).

# Classe Mapa
class Mapa: 
    def __init__(self, layout: List[str]):
        self.layout = [list(linha) for linha in layout]
        self.altura = len(self.layout)
        self.largura = len(self.layout[0])

    def imprimir(self, robos: List['Robo'], itens: List[Posicao], entregas: List[Posicao]):
        grid = [linha[:] for linha in self.layout]
        
        # Desenha itens e entregas 
        for x, y in itens:
            grid[y][x] = ITEM
        for x, y in entregas:
            grid[y][x] = ENTREGA
        
        # Desenha robôs ativos
        for robo in robos:
            if robo.status != StatusRobo.CONCLUIDO:
                x, y = robo.pos
                grid[y][x] = robo.nome
        
        # Formata e imprime cada célula com a cor correta
        for linha in grid:
            linha_formatada = []
            for celula in linha:
                if isinstance(celula, tuple):
                    char, cor = celula
                    linha_formatada.append(f"{cor}{char}{Style.RESET_ALL}")
                else:
                    linha_formatada.append(f"{CORES.get(celula, Fore.WHITE)}{celula}{Style.RESET_ALL}")
            print("  ".join(linha_formatada))
        print("-" * (self.largura * 3))

    # Verifica se a posição está dentro do mapa e não é parede.
    def eh_valida(self, pos: Posicao) -> bool:
        x, y = pos
        return 0 <= y < self.altura and 0 <= x < self.largura and self.layout[y][x] != PAREDE

    # Retorna todas as posições de um caractere específico no mapa.
    def achar_posicoes(self, char: str) -> List[Posicao]:
        posicoes = []
        for y, linha in enumerate(self.layout):
            for x, c in enumerate(linha):
                if c == char:
                    posicoes.append((x, y))
        return posicoes

# Classe Robô
class Robo:
    def __init__(self, nome: str, pos_inicial: Posicao):
        self.nome = nome
        self.pos = pos_inicial
        self.caminho: Caminho = []
        self.status = StatusRobo.OCIOSO
        self.item_alvo: Optional[Posicao] = None

    def mover(self):
        if self.caminho:
            self.pos = self.caminho.pop(0)

    def pegar_item(self, log_eventos: List[str]):
        log_eventos.append(f"✅ {CORES[self.nome]}{self.nome}{Style.RESET_ALL} coletou o item em {self.item_alvo}!")
        self.item_alvo = None
        self.status = StatusRobo.INDO_PARA_ENTREGA

    def entregar_item(self, log_eventos: List[str]):
        log_eventos.append(f"🏆 {CORES[self.nome]}{self.nome}{Style.RESET_ALL} concluiu a entrega em {self.pos}!")
        self.status = StatusRobo.CONCLUIDO

# Algoritmo A*
def achar_caminho(mapa: Mapa, inicio: Posicao, fim: Posicao) -> Optional[Caminho]: # caminho mais curto usando o algoritmo A*
    aberto = [(0, inicio)] # fila de prioridade com (f_score, posição)
    veio_de: Dict[Posicao, Posicao] = {} # para reconstruir o caminho
    g_score = {inicio: 0} # custo do caminho percorrido
    f_score = {inicio: heuristica(inicio, fim)} # custo total estimado (g + heurística)

    while aberto:
        _, atual = heapq.heappop(aberto)
        if atual == fim: # chegou no destino
            caminho = []
            while atual in veio_de:
                caminho.append(atual)
                atual = veio_de[atual]
            return caminho[::-1] # caminho invertido do início ao fim

        # explora vizinhos (cima, baixo, direita, esquerda)
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            vizinho = (atual[0] + dx, atual[1] + dy)
            if not mapa.eh_valida(vizinho):
                continue
            
            g_temp = g_score[atual] + 1
            if g_temp < g_score.get(vizinho, float('inf')):
                veio_de[vizinho] = atual
                g_score[vizinho] = g_temp
                f_score[vizinho] = g_temp + heuristica(vizinho, fim)
                heapq.heappush(aberto, (f_score[vizinho], vizinho))
    return None

# Classe Simulação
class Simulacao:
    def __init__(self, layout: List[str]):
        self.mapa = Mapa(layout)
        self.robos: List[Robo] = []
        self.log_eventos = []
        
        for nome_robo in ROBOS_ID:
            pos_inicial = self.mapa.achar_posicoes(nome_robo)
            if pos_inicial:
                self.robos.append(Robo(nome_robo, pos_inicial[0]))
                # Limpa a posição inicial do mapa para que o robô se mova livremente
                self.mapa.layout[pos_inicial[0][1]][pos_inicial[0][0]] = CAMINHO

        # Identifica itens e pontos de entrega disponíveis no mapa
        self.itens_disponiveis = self.mapa.achar_posicoes(ITEM)
        self.pontos_entrega = self.mapa.achar_posicoes(ENTREGA)
        
        # Remove itens e entregas do mapa para que sejam desenhados dinamicamente
        for pos in self.itens_disponiveis + self.pontos_entrega:
            self.mapa.layout[pos[1]][pos[0]] = CAMINHO

    def _atribuir_tarefas(self): #Atribui tarefas aos robôs ociosos -> cada robô recebe o item mais próximo
        robos_ociosos = [r for r in self.robos if r.status == StatusRobo.OCIOSO]
        itens_ja_designados = {r.item_alvo for r in self.robos if r.item_alvo is not None}
        
        for robo in robos_ociosos:
            # Filtra itens ainda não designados
            itens_para_atribuir = [item for item in self.itens_disponiveis if item not in itens_ja_designados]
            if not itens_para_atribuir:
                break

            # Seleciona o item mais próximo usando heurística
            melhor_item = min(itens_para_atribuir, key=lambda item: heuristica(robo.pos, item))
            caminho_para_item = achar_caminho(self.mapa, robo.pos, melhor_item)
            if caminho_para_item:
                robo.caminho = caminho_para_item
                robo.status = StatusRobo.INDO_PARA_ITEM
                robo.item_alvo = melhor_item
                itens_ja_designados.add(melhor_item)
                self.log_eventos.append(f"📝 {CORES[robo.nome]}{robo.nome}{Style.RESET_ALL} recebeu tarefa: buscar item em {melhor_item}.")

    def _atualizar_estados(self):
        for robo in self.robos:
            if not robo.caminho and robo.status not in [StatusRobo.OCIOSO, StatusRobo.CONCLUIDO]:
                if robo.status == StatusRobo.INDO_PARA_ITEM:

                    # Remove o item do estoque se chegou lá
                    if robo.pos in self.itens_disponiveis:
                        self.itens_disponiveis.remove(robo.pos)
                    robo.pegar_item(self.log_eventos)
                    
                    # Define o destino de entrega e calcula o caminho
                    destino_entrega = self.pontos_entrega[0]
                    caminho_para_entrega = achar_caminho(self.mapa, robo.pos, destino_entrega)
                    if caminho_para_entrega:
                        robo.caminho = caminho_para_entrega
                elif robo.status == StatusRobo.INDO_PARA_ENTREGA:
                    # Robô concluiu entrega
                    robo.entregar_item(self.log_eventos)

    def _mover_robos(self):
        # Dicionário com a próxima posição desejada de cada robô
        planos = {
            robo.nome: robo.caminho[0]
            for robo in self.robos
            if robo.caminho and robo.status != StatusRobo.CONCLUIDO
        }
        movimentos_finais = {} # armazena movimentos válidos
        posicoes_reservadas = set() # evita que dois robôs ocupem a mesma célula

        # Resolve prioridade por ordem alfabética (R > S)
        for nome in sorted(planos.keys()):
            pos_desejada = planos[nome]
            robo_atual = next(r for r in self.robos if r.nome == nome)

            # Se a posição já está reservada, o robô aguarda
            if pos_desejada in posicoes_reservadas:
                self.log_eventos.append(f"⚠️  {CORES[nome]}{nome}{Style.RESET_ALL} aguarda: Posição {pos_desejada} reservada por robô de maior prioridade.")
                continue

            bloqueado = False
            # Verifica se algum robô está parado na posição desejada
            for outro_robo in self.robos:
                if robo_atual == outro_robo or outro_robo.status == StatusRobo.CONCLUIDO:
                    continue 
                
                if outro_robo.pos == pos_desejada and outro_robo.nome not in planos:
                    bloqueado = True
                    self.log_eventos.append(f"⚠️  {CORES[nome]}{nome}{Style.RESET_ALL} aguarda: {CORES[outro_robo.nome]}{outro_robo.nome}{Style.RESET_ALL} está parado em {pos_desejada}.")
                    break
            
            if not bloqueado:
                movimentos_finais[nome] = pos_desejada
                posicoes_reservadas.add(pos_desejada)

        # Caso nenhum robô consiga se mover
        if planos and not movimentos_finais:
             self.log_eventos.append(f"{Fore.RED}🛑 ALERTA DE IMPASSE: Nenhum robô conseguiu se mover!{Style.RESET_ALL}")

        # Executa os movimentos válidos
        for nome, nova_pos in movimentos_finais.items():
            robo = next(r for r in self.robos if r.nome == nome)
            pos_anterior = robo.pos
            robo.mover()
            self.log_eventos.append(f"⚙️  {CORES[nome]}{nome}{Style.RESET_ALL} moveu-se de {pos_anterior} para {nova_pos}.")

    #Executa a simulação completa passo a passo. -> mapa, status dos robôs e log de eventos a cada passo
    def executar(self):
        mostrar_banner()
        passo = 0
        
        while self.itens_disponiveis or any(r.status not in [StatusRobo.OCIOSO, StatusRobo.CONCLUIDO] for r in self.robos):
            limpar_tela()
            print(f"{Fore.CYAN}PASSO DE SIMULAÇÃO: {passo}{Style.RESET_ALL}")
            self.log_eventos.clear()

            self._atribuir_tarefas() # atribui tarefas a robôs ociosos
            self._mover_robos() # move os robôs de acordo com seus caminhos planejados
            self._atualizar_estados() # atualiza estados após movimentos (coleta ou entrega)
            
            # Exibe mapa atualizado
            self.mapa.imprimir(self.robos, self.itens_disponiveis, self.pontos_entrega)

            # Status detalhado de cada robô
            print("="*20 + " STATUS DOS ROBÔS " + "="*20)
            for r in self.robos:
                status_str = f"● {CORES[r.nome]}{r.nome}{Style.RESET_ALL} | Posição: {str(r.pos):<10} | Status: {r.status.name:<18}"
                if r.status == StatusRobo.INDO_PARA_ITEM:
                    status_str += f" | Alvo: 📦 {r.item_alvo}"
                elif r.status == StatusRobo.INDO_PARA_ENTREGA:
                    destino = self.pontos_entrega[0]
                    status_str += f" | Alvo: 🎯 {destino}"
                if r.caminho:
                    status_str += f" | "
                print(status_str)

            # Log de eventos do passo
            print("\n" + "="*20 + " LOG DE EVENTOS DO PASSO " + "="*17)
            if self.log_eventos:
                for evento in self.log_eventos:
                    print(evento)
            else:
                print("Nenhum evento significativo neste passo.")
            
            time.sleep(DELAY_PASSO)
            passo += 1

        # Fim
        print(f"\n{Fore.GREEN}🎉 SIMULAÇÃO CONCLUÍDA! TODOS OS ITENS FORAM ENTREGUES EM {passo} PASSOS. 🎉{Style.RESET_ALL}")

# Execução
if __name__ == "__main__":
    try:
        sim = Simulacao(MAPA_LAYOUT)
        sim.executar()
    except Exception as e:
        print(f"{Fore.RED}ERRO INESPERADO: {e}{Style.RESET_ALL}")