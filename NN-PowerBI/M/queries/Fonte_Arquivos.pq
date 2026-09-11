// =====================================================================
// Fonte_Arquivos — navega no SharePoint e devolve a lista de planilhas
// de mapeamento ativo. Uma linha por arquivo .xlsx da pasta.
// =====================================================================
let
    Origem = SharePoint.Contents(pSiteSharePoint, [ApiVersion = 15]),

    // entra numa subpasta pelo nome, ignorando maiúsc./minúsc.
    fnEntrar = (tbl as table, nome as text) as table =>
        let
            achado = Table.SelectRows(tbl, each
                        Comparer.OrdinalIgnoreCase(Text.Trim([Name]), Text.Trim(nome)) = 0),
            conteudo =
                if Table.RowCount(achado) = 0
                then error Error.Record("Pasta não encontrada",
                        "Não existe a pasta/biblioteca '" & nome & "' neste nível do SharePoint.",
                        "Níveis disponíveis: " & Text.Combine(tbl[Name], " | "))
                else achado{0}[Content]
        in  conteudo,

    Biblioteca = fnEntrar(Origem, pBiblioteca),

    Partes = List.Select(
                List.Transform(Text.Split(pPastaMapeamentos, "/"), Text.Trim),
                each _ <> ""),

    Pasta = List.Accumulate(Partes, Biblioteca, (estado, parte) => fnEntrar(estado, parte)),

    SoArquivos = Table.SelectRows(Pasta, each
        [Content] <> null
        and Text.EndsWith(Text.Lower([Name]), ".xlsx")
        and not Text.StartsWith([Name], "~$")),

    ComResponsavel = Table.AddColumn(SoArquivos, "Arquivo", each [Name], type text),

    // Nome do responsável deduzido do arquivo (fallback caso a coluna venha vazia)
    ComNomeArquivo = Table.AddColumn(ComResponsavel, "Responsável (arquivo)", each
        let
            semExt = Text.BeforeDelimiter([Name], ".", {0, RelativePosition.FromEnd}),
            semPrefixo = if Text.Contains(Text.Lower(semExt), "mapeamento")
                         then Text.AfterDelimiter(semExt, "_")
                         else semExt,
            comEspaco = Text.Trim(Text.Replace(Text.Replace(semPrefixo, "_", " "), "-", " "))
        in  if comEspaco = "" then semExt else Text.Upper(comEspaco), type text),

    Final = Table.SelectColumns(ComNomeArquivo,
                {"Content", "Arquivo", "Responsável (arquivo)", "Date modified"},
                MissingField.UseNull)
in
    Final
