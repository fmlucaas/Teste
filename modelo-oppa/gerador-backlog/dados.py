# -*- coding: utf-8 -*-
"""Avaliacao dos 40 PBIs. Notas de 1 a 5.

DEP nao e digitado: e calculado a partir do grafo de dependencias.
"""

# id: (VU, OBR, MON, ESF, [pre-requisitos], justificativa)
AVAL = {
"PBI-01": (3, 4, 3, 2, [], "Porta de entrada. Sem autenticação não existe produto, e dado de saúde exige acesso seguro. Login por SMS é padrão de mercado e barato de implementar."),
"PBI-02": (3, 1, 3, 1, ["PBI-01"], "Define quem é Cuidador e quem é Cuidado — a escolha que determina todo o comportamento do app. Barato e destrava quase tudo."),
"PBI-03": (2, 5, 2, 1, ["PBI-02"], "Dado de saúde é dado sensível (LGPD art. 11): exige consentimento específico e destacado. Sem aceite registrado não se publica nas lojas nem se opera legalmente."),
"PBI-04": (2, 1, 2, 3, ["PBI-02"], "O médico é ator secundário: não participa do ciclo diário do cuidador. Valioso para credibilidade, não para retenção."),
"PBI-05": (5, 1, 4, 4, ["PBI-02", "PBI-06", "PBI-13", "PBI-26"], "É a tela do momento mágico: abrir o app e ver que está tudo bem, e a vitrine que antecede a decisão de pagar. Agrega dados de outros itens, por isso vem depois deles. Se quiserem uma versão esqueleto antes, fatiem em estrutura e dados: a estrutura sobe para a primeira onda."),
"PBI-06": (3, 1, 1, 1, ["PBI-01"], "Esqueleto de navegação. Barato, e todas as telas dependem dele para existir em algum lugar."),
"PBI-07": (2, 1, 1, 5, ["PBI-24", "PBI-30"], "Front-end web inteiro e separado, para o ator de menor frequência de uso. Alto custo, baixo alcance."),
"PBI-08": (3, 1, 1, 1, ["PBI-06"], "Feedback de sistema é higiene de usabilidade: barato, e sua ausência faz o usuário duvidar se a ação funcionou."),
"PBI-09": (2, 1, 5, 2, ["PBI-02", "PBI-29", "PBI-05"], "Define a fronteira do funil: o que o usuário ganha de graça determina o que ele aceita pagar."),
"PBI-10": (1, 1, 4, 2, ["PBI-09"], "Primeiro degrau pago. Hoje o salto de valor sobre o Free (2 para 3 cuidadores) é pequeno demais — ver observações."),
"PBI-11": (1, 1, 4, 2, ["PBI-10", "PBI-32"], "Concentra os Avisos Inteligentes. Atenção ao que fica atrás do paywall — ver observações."),
"PBI-12": (1, 1, 3, 3, ["PBI-11"], "Multi-idoso é decisão de modelo de dados, não de tela. A modelagem tem de ser feita cedo mesmo que a venda venha depois."),
"PBI-13": (5, 1, 5, 4, ["PBI-02", "PBI-26"], "É a razão de ser do produto: saber que a mãe está bem sem ligar para ela. E o histórico desses dados é justamente a funcionalidade que o modelo financeiro vende."),
"PBI-14": (3, 1, 2, 2, ["PBI-13"], "Passos são sinal de rotina preservada. Complementa, não sustenta sozinho."),
"PBI-15": (2, 1, 1, 2, ["PBI-13"], "Hidratação depende de registro manual do idoso — a adesão tende a ser baixa no público-alvo."),
"PBI-16": (2, 1, 1, 2, ["PBI-14"], "Gamificação é retenção de segunda ordem: só importa depois que o uso diário estiver estabelecido."),
"PBI-17": (5, 1, 5, 3, ["PBI-13"], "Mesmo valor do iOS, para a maior fatia do mercado brasileiro. Vem depois porque reaproveita o contrato de ingestão definido no iOS."),
"PBI-18": (3, 1, 2, 2, ["PBI-17", "PBI-14"], "Espelho do PBI-14. Se a regra de negócio ficar no servidor, custa uma fração do primeiro."),
"PBI-19": (2, 1, 1, 2, ["PBI-17", "PBI-15"], "Espelho do PBI-15."),
"PBI-20": (2, 1, 1, 2, ["PBI-18", "PBI-16"], "Espelho do PBI-16."),
"PBI-21": (1, 1, 2, 5, [], "Depende de aprovação do Google nas Home APIs, com processo e restrições próprias. Risco de viabilidade a validar antes de entrar em roadmap."),
"PBI-22": (2, 1, 2, 3, ["PBI-21"], "Painel informativo sem ação remota entrega pouco sozinho: saber que a luz está acesa não muda nada."),
"PBI-23": (4, 1, 3, 4, ["PBI-22"], "Aqui sim há valor real: fogão ligado é um dos medos mais citados por quem cuida de idoso. É o item que justifica toda a integração de casa."),
"PBI-24": (3, 1, 3, 3, ["PBI-02", "PBI-06"], "Organiza o passado clínico. Valor alto na consulta médica, baixo no uso diário."),
"PBI-25": (3, 1, 3, 3, ["PBI-24"], "Anexar laudo é o gesto concreto que dá utilidade ao histórico clínico."),
"PBI-26": (2, 1, 3, 4, [], "Invisível ao usuário e sustenta tudo: sem ingestão confiável, nenhuma métrica e nenhum alerta funcionam."),
"PBI-27": (1, 5, 1, 2, ["PBI-01"], "Trilha de auditoria de acesso a dado sensível. Não gera valor percebido, mas é o que se apresenta numa fiscalização ou incidente."),
"PBI-28": (4, 3, 2, 2, ["PBI-02"], "Define o que o idoso pode fazer no próprio app — inclusive apertar o SOS. É pré-requisito de dignidade e de funcionalidade."),
"PBI-29": (4, 1, 4, 2, ["PBI-02"], "Cuidado compartilhado entre irmãos é o padrão real das famílias. E é exatamente o que os planos vendem: número de cuidadores."),
"PBI-30": (2, 4, 1, 2, ["PBI-04", "PBI-29"], "Escopo mínimo de acesso para terceiro que vê dado de saúde — obrigação, mais que funcionalidade."),
"PBI-31": (2, 4, 1, 2, ["PBI-01"], "Encerrar sessão em aparelho perdido é controle básico de segurança de conta com dado sensível."),
"PBI-32": (5, 1, 5, 3, ["PBI-13", "PBI-26"], "O alerta que justifica o produto existir. Também o de maior risco: promessa de detecção cria expectativa de confiabilidade e exposição regulatória."),
"PBI-33": (5, 1, 5, 3, ["PBI-05"], "Adesão a medicamento é o problema nº 1 do cuidado domiciliar. ATENÇÃO: depende de um cadastro de medicamentos que não existe no backlog."),
"PBI-34": (3, 2, 2, 2, ["PBI-32"], "Controle de notificação é o que evita a fadiga de alerta — a causa mais comum de desinstalação em apps de monitoramento."),
"PBI-35": (5, 1, 3, 2, ["PBI-28"], "Pedido de socorro pelo próprio idoso. Barato de construir e altíssimo em valor percebido e em confiança."),
"PBI-36": (5, 2, 5, 4, ["PBI-26"], "Para famílias que lidam com demência, sair de casa sozinho é o medo central. É a funcionalidade que sustenta um plano pago."),
"PBI-37": (3, 1, 3, 3, ["PBI-36"], "Refinamento do cerco virtual: cobre o caso em que o idoso não saiu da área, mas parou onde não deveria."),
"PBI-38": (3, 2, 4, 3, ["PBI-36"], "Histórico de trajeto é dado retroativo — exatamente o tipo de funcionalidade que o modelo financeiro reserva ao usuário pagante."),
"PBI-39": (4, 1, 2, 1, ["PBI-26"], "Barato e protege todos os outros alertas: relógio sem bateria transforma o produto inteiro em silêncio."),
"PBI-40": (3, 1, 3, 3, ["PBI-36"], "Confirmação de rotina cumprida — chegou na fisioterapia. Valor real, mas depende do cerco virtual estar de pé."),
}

PESOS = {"VU": 3.0, "OBR": 2.5, "MON": 2.0, "DEP": 2.0}

CRITERIOS = [
    ("VU",  "Valor para o usuário", 3.0,
     "O quanto o item entrega da promessa central do produto: tranquilidade para quem cuida. "
     "Habilitadores como login e menu recebem nota baixa de propósito — eles vêm primeiro porque "
     "outros itens dependem deles, não porque entregam valor. Quem garante essa ordem é o grafo de "
     "dependências, não a nota."),
    ("OBR", "Obrigação legal ou de plataforma", 2.5,
     "Só pontua alto o que CRIA PROBLEMA se não for feito: exigência da LGPD, requisito de "
     "publicação nas lojas de aplicativos ou segurança da conta. Risco criado por fazer o item "
     "(exposição regulatória, dependência de aprovação de terceiros) não entra aqui — está na "
     "coluna Risco a gerenciar."),
    ("MON", "Habilita monetização", 2.0,
     "O quanto o item destrava, sustenta ou defende a decisão de assinar."),
    ("DEP", "Destrava outros itens", 2.0,
     "CALCULADO, não digitado: quantos PBIs ficam bloqueados, direta ou indiretamente, enquanto "
     "este não existir. Convertido para a escala de 1 a 5."),
]

# itens que carregam risco de execucao — nao entram na nota, entram como alerta
RISCOS = {
"PBI-13": "Dados do HealthKit não saem do aparelho do titular: exige o app instalado no iPhone do "
          "próprio idoso, com consentimento dele. Muda o onboarding — ver OBS-03.",
"PBI-17": "Android fragmentado: Health Connect, Samsung Health e camadas de fabricante têm "
          "comportamentos diferentes. Estimar com folga.",
"PBI-21": "Depende de aprovação do Google nas Home APIs. Risco de VIABILIDADE, não só de esforço: "
          "vale uma prova de conceito antes de assumir compromisso de roadmap.",
"PBI-32": "Prometer detecção de queda cria expectativa de confiabilidade e pode enquadrar o app "
          "como software de finalidade médica. Cuidado com a redação da promessa — ver LAC-16.",
"PBI-33": "O bloqueador real é o cadastro de medicamentos, que não existe no backlog (LAC-03). "
          "A posição no ranking pressupõe essa lacuna resolvida antes.",
"PBI-35": "Botão de socorro cria expectativa de resposta. Definir explicitamente o que o app faz e "
          "o que não faz — não é serviço de emergência.",
"PBI-36": "Rastrear pessoa exige base legal e consentimento do próprio titular, não do cuidador "
          "(LAC-07). Também exige permissão de localização contínua, justificada na revisão das lojas.",
"PBI-11": "Se os Avisos Inteligentes incluírem queda ou SOS, a empresa passa a cobrar por "
          "segurança. Decisão sensível — ver OBS-01.",
}

# ---------------------------------------------------------------- lacunas
LACUNAS = [
("LAC-01", "Vínculo entre Cuidador e Cuidado", "Bloqueador", "Crítica",
 "O PBI-02 apenas escolhe o papel na hora do cadastro. Não há nada que ligue a conta do cuidador "
 "à conta do idoso — convite, código de pareamento, aceite. Sem esse vínculo não existe a quem "
 "cuidar, e nenhuma das telas seguintes tem dados para mostrar.",
 "Bloqueia praticamente todo o backlog",
 "Onda 1 — logo após o PBI-02"),
("LAC-02", "Criar grupo de cuidado e convidar cuidadores", "Bloqueador", "Crítica",
 "O menu tem 'Grupos' (PBI-06), os quatro planos vendem número de cuidadores (PBI-09 a 12) e o "
 "PBI-29 garante direitos iguais entre eles. Mas nenhum item cria o grupo, convida alguém ou "
 "processa o aceite do convite.",
 "PBI-06, 09, 10, 11, 12, 29",
 "Onda 1 — antes do PBI-29"),
("LAC-03", "Cadastro e agenda de medicamentos", "Bloqueador", "Crítica",
 "A tela inicial mostra remédios (PBI-05) e o PBI-33 avisa quando um remédio vital é esquecido. "
 "Nada no backlog cadastra o medicamento, define horário, dose ou registra a tomada.",
 "PBI-05, PBI-33",
 "Onda 2 — antes do PBI-05 e do PBI-33"),
("LAC-04", "Cobrança, assinatura e paywall", "Bloqueador", "Crítica",
 "Os PBIs 09 a 12 definem as REGRAS de cada plano, mas nada cobra: não há compra dentro do app, "
 "tela de paywall, upgrade, downgrade, cancelamento, período de teste nem tratamento de "
 "inadimplência. É o item que separa ter usuários de ter receita.",
 "PBI-09, 10, 11, 12",
 "Onda 3 — junto com o PBI-09"),
("LAC-05", "Coleta de localização em segundo plano e permissões", "Bloqueador", "Crítica",
 "Os cinco PBIs de geolocalização consomem uma posição que ninguém coleta. Rastreamento contínuo "
 "exige permissão 'sempre' do sistema, tratamento de economia de bateria e uma justificativa "
 "aceita na revisão das lojas — é trabalho técnico próprio, não um detalhe.",
 "PBI-36, 37, 38, 39, 40",
 "Onda 2 — antes do PBI-36"),
("LAC-06", "Infraestrutura de notificação push", "Bloqueador", "Crítica",
 "Seis PBIs terminam em 'avisa o cuidador'. Não há item que trate registro de token, permissão do "
 "sistema, entrega, repetição quando não há resposta e som que atravessa o modo silencioso — "
 "essencial para um alerta de queda de madrugada.",
 "PBI-23, 32, 33, 34, 39, 40",
 "Onda 1 — antes do PBI-35"),
("LAC-07", "Consentimento do próprio idoso", "Conformidade", "Crítica",
 "O PBI-03 coleta o aceite de quem se cadastra. Mas quem é monitorado é o idoso, e dado de saúde e "
 "localização são dados sensíveis: a LGPD exige consentimento específico e destacado do próprio "
 "titular. Se houver incapacidade, é preciso representação legal formalizada. Monitorar alguém com "
 "base no aceite de um familiar é frágil juridicamente e eticamente.",
 "PBI-03, e todo o módulo de geolocalização",
 "Onda 1 — junto com o PBI-03"),
("LAC-08", "Exportar e excluir dados e conta", "Conformidade", "Alta",
 "Direito do titular pela LGPD (art. 18) e exigência explícita de Apple e Google: app que cria "
 "conta precisa permitir excluí-la de dentro do app. É motivo documentado de reprovação na revisão.",
 "Bloqueia a publicação nas lojas",
 "Onda 1 — antes da primeira submissão às lojas"),
("LAC-09", "Acessibilidade para o público idoso", "Usabilidade", "Alta",
 "Não há um único item sobre tamanho de fonte, contraste, área de toque, leitor de tela ou "
 "simplificação de fluxo. Para um produto cujo usuário final tem 70 ou 80 anos, acessibilidade "
 "não é um extra de usabilidade: é a usabilidade.",
 "Todo o app do Cuidado",
 "Transversal — critério de aceite de toda tela, desde a Onda 1"),
("LAC-10", "Tela Diário", "Escopo faltante", "Média",
 "'Diário' é um dos cinco botões do menu (PBI-06) e não tem nenhum PBI que o descreva. O que "
 "aparece nele? Registro de sintomas, humor, eventos do dia, anotações do cuidador?",
 "PBI-06",
 "Definir escopo antes da Onda 2"),
("LAC-11", "Tela Loja / marketplace", "Escopo faltante", "Média",
 "'Loja' também é um dos cinco botões e não tem PBI. É a mesma loja de dispositivos que o modelo "
 "financeiro projeta como receita de comissão a partir de 2027 — precisa existir como escopo.",
 "PBI-06",
 "Onda 5 — junto com a estratégia de marketplace"),
("LAC-12", "Observabilidade e confirmação de entrega de alerta", "Confiabilidade", "Alta",
 "Não há como saber se um alerta de queda foi entregue. Em produto de segurança isso não é métrica "
 "de produto, é requisito: falha silenciosa em alerta crítico é o pior modo de falha possível.",
 "PBI-32, 33, 35",
 "Onda 2 — junto com o PBI-32"),
("LAC-13", "Comportamento offline e falha de sincronização", "Confiabilidade", "Média",
 "O PBI-08 mostra a mensagem 'sem internet', mas nada define o que o app faz: enfileira, tenta de "
 "novo, avisa que o dado está desatualizado? Um cuidador vendo batimentos de duas horas atrás sem "
 "saber disso é pior do que não ver nada.",
 "PBI-08, PBI-05, PBI-26",
 "Onda 2 — junto com o PBI-26"),
("LAC-14", "Onboarding do idoso sem smartphone", "Escopo faltante", "Alta",
 "Parte relevante do público-alvo não tem celular próprio ou não sabe operá-lo. Todo o fluxo atual "
 "pressupõe que o idoso tem conta, aparelho e consegue concluir um cadastro. Qual é o caminho "
 "alternativo — configuração feita pelo cuidador, aparelho dedicado, só o relógio?",
 "PBI-01, 02, 28, 35",
 "Decidir antes da Onda 1 — muda o onboarding inteiro"),
("LAC-15", "Central de ajuda e suporte", "Escopo faltante", "Média",
 "Nenhum item trata de dúvida, primeiro uso ou problema. Em app de assinatura, suporte é alavanca "
 "direta de retenção, e o público-alvo é o que mais precisa de ajuda guiada.",
 "Retenção",
 "Onda 3"),
("LAC-16", "Posicionamento regulatório dos alertas de saúde", "Conformidade", "Alta",
 "Alerta de queda, alerta de medicamento vital e SOS podem enquadrar o app como software com "
 "finalidade médica perante a ANVISA, a depender de como forem descritos. A forma como a promessa "
 "é redigida na loja e dentro do app muda o enquadramento. Vale uma consulta jurídica antes do "
 "lançamento, não depois.",
 "PBI-32, 33, 35",
 "Antes do lançamento — consulta jurídica")
]

# ---------------------------------------------------------------- observacoes
OBS = [
("OBS-01", "Alerta de segurança atrás de paywall merece uma decisão consciente",
 "O PBI-11 coloca os Avisos Inteligentes no plano Premium. Se isso incluir o alerta de queda "
 "(PBI-32) ou o SOS (PBI-35), a empresa passa a cobrar por segurança: um idoso cai e o alerta não "
 "dispara porque a família está no plano gratuito. O risco reputacional é assimétrico — um único "
 "caso vira notícia. Recomendo manter queda e SOS no gratuito e monetizar histórico, número de "
 "cuidadores, relatórios e geolocalização avançada. Isso também protege a marca no exato momento "
 "em que ela mais precisa de confiança."),
("OBS-02", "O salto entre Free e Essencial é pequeno demais",
 "Hoje a diferença entre os dois é de 2 para 3 cuidadores (PBI-09 e PBI-10). É pouco para "
 "sustentar uma assinatura mensal. O modelo financeiro assume que a funcionalidade paga é o "
 "histórico de dados — que o usuário gratuito não tem. Vale alinhar as regras dos planos com "
 "essa premissa: gratuito vê o agora, pagante vê a evolução."),
("OBS-03", "Apple Health não sai do aparelho do idoso",
 "Os PBIs 13 a 16 falam em 'conectar o Apple Watch do idoso'. Na prática, os dados de saúde do "
 "HealthKit ficam no iPhone do próprio titular e só saem de lá por um app instalado ali, com "
 "consentimento dele. Ou seja: o idoso precisa de iPhone e do app instalado — não basta o "
 "cuidador instalar. Isso muda o onboarding, muda o custo de aquisição (são dois downloads por "
 "família) e reforça a lacuna LAC-14."),
("OBS-04", "A integração com Google Home tem risco de viabilidade, não só de esforço",
 "Os PBIs 21 a 23 dependem de aprovação do Google para acessar dados de casa de terceiros, com "
 "processo e restrições próprias. Antes de assumir compromisso de roadmap, vale uma prova de "
 "conceito curta só para confirmar que o acesso de leitura pretendido é concedido."),
("OBS-05", "Multi-idoso é decisão de arquitetura para tomar agora, mesmo entregando depois",
 "O plano Família (PBI-12) permite até 4 idosos na mesma conta. Modelar a relação entre cuidador "
 "e cuidado como muitos-para-muitos desde o início custa pouco; transformar depois um modelo "
 "um-para-um custa caro e mexe em tudo. Recomendo decidir a modelagem já na primeira onda e "
 "deixar a venda do plano para quando fizer sentido comercialmente."),
("OBS-06", "Metade da duplicação iOS/Android é evitável",
 "Os pares 14/18, 15/19 e 16/20 são a mesma regra de negócio escrita duas vezes. Se as metas, o "
 "registro de água e a lógica de comemoração ficarem no servidor, e o aplicativo cuidar apenas da "
 "coleta e da exibição, o segundo lado custa uma fração do primeiro. Vale como diretriz técnica "
 "antes de começar o PBI-13."),
("OBS-07", "Fadiga de alerta é o maior risco de retenção deste produto",
 "Cerco virtual, tempo parado, bateria fraca, rotina, casa, queda, remédio: são muitas fontes de "
 "notificação convergindo para o mesmo celular. Sem hierarquia entre elas, o cuidador silencia "
 "tudo — e aí o alerta que importa também não chega. O PBI-34 trata disso e por isso está ranqueado "
 "acima do que seu tamanho sugeriria."),
("OBS-08", "Falta o começo da jornada, não o fim",
 "As seis lacunas classificadas como bloqueadoras — vínculo, grupo, medicamentos, cobrança, "
 "localização e push — são todas de base. O backlog descreve muito bem o que o usuário vê e pouco "
 "do que precisa existir para que ele veja. É o padrão típico de backlog escrito a partir de telas, "
 "e a correção é barata agora e cara depois."),
]
