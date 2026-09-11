// =====================================================================
// fnUtil — funções utilitárias compartilhadas
// Crie UMA consulta em branco chamada exatamente  fnUtil  e cole isto.
// Uso: fnUtil[Data](valor) , fnUtil[Texto](valor) , etc.
// =====================================================================
let
    // ---- Limpeza de texto: remove NBSP, quebras de linha, espaços duplos ----
    Texto = (v as any) as nullable text =>
        let
            t0 = if v = null then null else Text.From(v),
            t1 = if t0 = null then null else
                 Text.Replace(Text.Replace(Text.Replace(Text.Replace(t0,
                     Character.FromNumber(160), " "), "#(cr)", " "), "#(lf)", " "), "#(tab)", " "),
            t2 = if t1 = null then null else Text.Trim(t1),
            t3 = if t2 = null then null else
                 List.Accumulate({1..5}, t2, (s, _) => Text.Replace(s, "  ", " ")),
            t4 = if t3 = null or t3 = "" then null else t3
        in  t4,

    // ---- Padroniza rótulos: MAIÚSCULA sem acento duplicado, para agrupar ----
    Chave = (v as any) as nullable text =>
        let t = Texto(v) in if t = null then null else Text.Upper(t),

    // ---- Título: Primeira Letra Maiúscula (para exibição) ----
    Titulo = (v as any) as nullable text =>
        let t = Texto(v) in if t = null then null else Text.Proper(Text.Lower(t)),

    // ---- Conversão de data à prova de bala -------------------------------
    // Aceita: data real, datetime, número (serial Excel), texto dd/MM/yyyy,
    // dd-MM-yyyy, dd.MM.yyyy, dd/MM.yyyy (erro de digitação real na base),
    // yyyy-MM-dd. Descarta anos fora de 2000..2040 (lixo tipo 1913 e 5039).
    Data = (v as any) as nullable date =>
        let
            bruto = if v = null then null else v,
            porTipo =
                if bruto = null then null
                else if Value.Is(bruto, type date) then bruto
                else if Value.Is(bruto, type datetime) then DateTime.Date(bruto)
                else if Value.Is(bruto, type datetimezone) then DateTime.Date(DateTimeZone.RemoveZone(bruto))
                else if Value.Is(bruto, type number) then
                    (if bruto >= 36526 and bruto <= 51136   // 2000-01-01 .. 2040-01-01
                     then Date.From(#date(1899,12,30) + #duration(Number.RoundDown(bruto),0,0,0))
                     else null)
                else null,
            comoTexto = if porTipo <> null then null else Texto(bruto),
            limpo = if comoTexto = null then null else
                    Text.Replace(Text.Replace(comoTexto, ".", "/"), "-", "/"),
            partes = if limpo = null then null else
                     List.Select(Text.Split(limpo, "/"), each Text.Trim(_) <> ""),
            numeros = if partes = null then null else
                      List.Transform(partes, each try Number.From(Text.Trim(Text.Start(_, 4))) otherwise null),
            valido  = if numeros = null then false else
                      (List.Count(numeros) >= 3 and not List.Contains(numeros, null)),
            porTexto =
                if not valido then null
                else let
                    a = numeros{0}, b = numeros{1}, c = numeros{2},
                    // yyyy/MM/dd  ou  dd/MM/yyyy
                    tentativa = if a > 31 then (try #date(a, b, c) otherwise null)
                                          else (try #date(c, b, a) otherwise null)
                in tentativa,
            final = porTipo ?? porTexto,
            saida = if final = null then null
                    else if Date.Year(final) < 2000 or Date.Year(final) > 2040 then null
                    else final
        in  saida,

    // ---- Número à prova de bala (aceita "1.234,56", "R$ 297", "138.82") ----
    Numero = (v as any) as nullable number =>
        let
            porTipo = if v = null then null
                      else if Value.Is(v, type number) then v
                      else null,
            txt = if porTipo <> null then null else Texto(v),
            // mantém apenas dígitos, vírgula, ponto e sinal negativo
            cru = if txt = null then null
                  else Text.Select(txt, {"0".."9", ",", ".", "-"}),
            temVirgula = cru <> null and Text.Contains(cru, ","),
            temPonto   = cru <> null and Text.Contains(cru, "."),
            qtdPontos  = if cru = null then 0
                         else List.Count(List.Select(Text.ToList(cru), each _ = ".")),
            // pt-BR "1.234,56"  -> ponto = milhar, vírgula = decimal
            // "1.234.567"       -> pontos = milhar
            // "138.82"          -> ponto = decimal
            padronizado =
                if cru = null then null
                else if temVirgula and temPonto then Text.Replace(Text.Replace(cru, ".", ""), ",", ".")
                else if temVirgula then Text.Replace(cru, ",", ".")
                else if qtdPontos > 1 then Text.Replace(cru, ".", "")
                else cru,
            porTexto = if padronizado = null or padronizado = "" or padronizado = "-" then null
                       else try Number.From(padronizado, "en-US") otherwise null
        in  porTipo ?? porTexto,

    // ---- Normaliza nomes de coluna (tira \n, espaços duplos, trim) ------
    NormalizaCabecalhos = (t as table) as table =>
        let
            nomes = Table.ColumnNames(t),
            limpos = List.Transform(nomes, each Texto(_) ?? "Coluna"),
            unicos = List.Accumulate(
                List.Positions(limpos), {},
                (acc, i) =>
                    let n = limpos{i},
                        n2 = if List.Contains(acc, n) then n & "_" & Text.From(i) else n
                    in acc & {n2}),
            renom = Table.RenameColumns(t, List.Zip({nomes, unicos}))
        in  renom,

    // ---- Garante que as colunas existam (cria como null se faltarem) ----
    GaranteColunas = (t as table, cols as list) as table =>
        let
            faltantes = List.Difference(cols, Table.ColumnNames(t)),
            completo = List.Accumulate(faltantes, t,
                (s, c) => Table.AddColumn(s, c, each null))
        in  completo,

    // ---- Seleciona só as colunas desejadas, tolerando ausências ---------
    SelecionaColunas = (t as table, cols as list) as table =>
        Table.SelectColumns(GaranteColunas(t, cols), cols),

    Saida = [
        Texto = Texto, Chave = Chave, Titulo = Titulo,
        Data = Data, Numero = Numero,
        NormalizaCabecalhos = NormalizaCabecalhos,
        GaranteColunas = GaranteColunas,
        SelecionaColunas = SelecionaColunas
    ]
in
    Saida
