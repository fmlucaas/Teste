// Unidade Referência — cópia DESCONECTADA da lista de unidades de negócio.
// Não tem relacionamento com nada, de propósito.
// Serve ao gráfico "Franquias de Atuação": ele precisa mostrar TODAS as
// unidades mesmo quando o filtro da página está numa unidade só — é esse
// contraste que dá a leitura "esta BU representa X% do que NN avaliou".
let
    Fonte = #"Unidade de Negócio",
    Renomeado = Table.RenameColumns(Fonte, {{"Unidade de Negócio", "Unidade"}})
in
    Renomeado
