// Fonte_Regua — abre o arquivo da régua de esforço (Regua_Esforco_NN.xlsx),
// se ele existir na pasta dos mapeamentos. Se não existir, devolve null e o
// modelo segue funcionando com a régua em branco.
// Esta é a consulta que deixa o "canal aberto": o time preenche o Excel,
// atualiza o Power BI, e as horas passam a aparecer. Sem mexer em código.
let
    Tentativa = try
        let
            Origem = SharePoint.Contents(pSiteSharePoint, [ApiVersion = 15]),
            fnEntrar = (tbl as table, nome as text) =>
                Table.SelectRows(tbl, each
                    Comparer.OrdinalIgnoreCase(Text.Trim([Name]), Text.Trim(nome)) = 0){0}[Content],
            Biblioteca = fnEntrar(Origem, pBiblioteca),
            Partes = List.Select(List.Transform(Text.Split(pPastaMapeamentos, "/"), Text.Trim), each _ <> ""),
            Pasta = List.Accumulate(Partes, Biblioteca, (e, p) => fnEntrar(e, p)),
            Arquivo = Table.SelectRows(Pasta, each
                Comparer.OrdinalIgnoreCase(Text.Trim([Name]), Text.Trim(pArquivoRegua)) = 0),
            Conteudo = if Table.RowCount(Arquivo) = 0 then null else Arquivo{0}[Content],
            Livro = if Conteudo = null then null else Excel.Workbook(Conteudo, null, true)
        in  Livro
    otherwise null,

    // lê uma aba do arquivo pelo nome; null se não existir
    fnAba = (nome as text) as nullable table =>
        if Tentativa = null then null
        else let
            a = Table.SelectRows(Tentativa, each [Kind] = "Sheet" and
                    Comparer.OrdinalIgnoreCase(Text.Trim([Item]), nome) = 0)
        in  if Table.RowCount(a) = 0 then null
            else fnUtil[NormalizaCabecalhos](
                    Table.PromoteHeaders(a{0}[Data], [PromoteAllScalars = true])),

    Saida = [Livro = Tentativa, Aba = fnAba]
in
    Saida
