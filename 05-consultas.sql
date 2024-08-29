# Consultas 

/* a) Consulta para listar todas as doenças e seus respectivos dados. A consulta deve retornar id da doença, seu 
nome, número CID, e o tipo do patógeno. A sequência em que as colunas serão apresentadas deve manter 
essa ordem e as linhas organizadas em ordem alfabética em relação ao nome da doença.*/

SELECT d.id, d.nome_tecnico, d.CID, p.tipo FROM doença AS d
JOIN patogeno AS p ON d.id_patogeno = p.id
ORDER BY d.nome_tecnico ASC;

/* b) Consulta para listar os sintomas de uma doença específica. A consulta deve retornar o nome do sintoma e 
sua taxa de ocorrência, nessa ordem de colunas, e de forma que as linhas sejam ordenadas pela taxa de 
ocorrência em que sintomas mais frequentes devem ser posicionados acima dos sintomas menos 
frequentes (em caso de dois ou mais sintomas com a mesma taxa de ocorrência, deve-se seguir com a 
ordenação pela ordem alfabética em relação ao nome do sintoma).*/

SELECT a.doença_id, s.nome, a.frequencia FROM apresenta AS a
JOIN doença AS d ON a.doença_id = d.id
JOIN sintomas AS s ON s.id = a.sintoma_id
WHERE a.`doença_id` = 1
ORDER BY
    CASE 
        WHEN a.frequencia = 'muito comum' THEN 1
        WHEN a.frequencia = 'comum' THEN 2
        WHEN a.frequencia = 'pouco comum' THEN 3
        ELSE 4
    END,
    s.nome ASC;

/* c) Consulta para listar todas as doenças e seus respectivos sintomas. A consulta deve retornar id da doença, 
seu nome, e os seus sintomas (juntamente com a taxa de ocorrência). A sequência em que as colunas serão 
apresentadas deve manter essa ordem. As linhas devem ser organizadas em ordem alfabética em relação 
ao nome da doença. Cada doença deve ser apresentada em uma única linha e, para doenças com múltiplos 
sintomas, eles devem ser disponibilizados em uma única coluna separados por vírgula. Os sintomas devem 
ser ordenados do muito comum ao muito raro. Para cada sintoma, a sua taxa de ocorrência deve vir entre 
parênteses, logo em seguida ao nome do sintoma (por exemplo, “Febre (muito comum), Diarreia (raro), 
Dor no corpo (muito raro)”). */

SELECT d.id, d.nome_tecnico, 
GROUP_CONCAT(s.nome, '(', a.frequencia, ')' ORDER BY FIELD(a.frequencia, 'muito comum', 'comum', 'pouco comum', 'raro', 'muito raro')) AS sintoma 
FROM apresenta AS a
JOIN doença AS d ON a.doença_id = d.id
JOIN sintomas AS s ON a.sintoma_id = s.id
GROUP BY d.id
ORDER BY d.nome_tecnico;

/* d) Consulta para calcular o número de doenças cadastradas para cada tipo de patógeno. Devem ser 
apresentados o tipo do patógeno (vírus, bactéria, fungo, ...) e a quantidade de doenças cadastradas no 
sistema que são causadas pelo respectivo tipo de patógeno. As colunas devem seguir a ordem especificada 
e as linhas devem ser organizadas em ordem decrescente em relação à quantidade de doenças, seguida 
pela ordem alfabética em relação ao tipo do patógeno.*/

SELECT p.tipo, COUNT(d.id) AS quantidade_doencas_cadastradas
FROM patogeno p
JOIN doença d ON p.id = d.id_patogeno
GROUP BY p.tipo
ORDER BY quantidade_doencas_cadastradas DESC, p.tipo ASC;

/* e) Consulta para obter algumas estatísticas sobre os dados armazenados no sistema. A consulta deverá 
apresentar o número de doenças cadastradas, o número de sintomas cadastrados, o número médio de 
sintomas por doença, o menor número de sintomas de uma doença, o maior número de sintomas de uma 
doença. As colunas devem ser apresentadas nessa ordem e as linhas devem ser organizadas em ordem 
crescente considerando a mesma ordem das colunas. */

SELECT COUNT(*) AS numero_doencas FROM doença;
SELECT COUNT(*) AS numero_sintomas FROM sintomas;
SELECT 
    AVG(doenca_sintomas.sintomas_por_doenca) AS media_sintomas_por_doenca,
    MIN(doenca_sintomas.sintomas_por_doenca) AS menor_numero_sintomas,
    MAX(doenca_sintomas.sintomas_por_doenca) AS maior_numero_sintomas
FROM (
    SELECT COUNT(a.sintoma_id) AS sintomas_por_doenca
    FROM doença d
    LEFT JOIN apresenta a ON d.id = a.doença_id
    GROUP BY d.id
) AS doenca_sintomas;

/* f) Consulta com estatísticas sobre os sintomas. A consulta deve apresentar o nome do sintoma, o número 
total de doenças que apresenta o sintoma, o número de doenças em que o sintoma é muito comum, 
comum, pouco comum, raro e muito raro. As colunas devem ser apresentadas nesta ordem e as linhas 
devem ser organizadas, em ordem decrescente, em relação ao número total de doenças, em seguida pela 
taxa de ocorrência (do muito comum ao muito raro) e, por fim, por ordem alfabética em relação ao nome 
do sintoma. */
    
SELECT 
    s.nome AS nome_sintoma,
    COUNT(DISTINCT a1.doença_id) AS total,
    COUNT(DISTINCT a2.doença_id) AS muito_comum,
    COUNT(DISTINCT a3.doença_id) AS comum,
    COUNT(DISTINCT a4.doença_id) AS pouco_comum,
    COUNT(DISTINCT a5.doença_id) AS raro,
    COUNT(DISTINCT a6.doença_id) AS muito_raro
FROM 
    sintomas s
LEFT JOIN 
    apresenta a1 ON s.id = a1.sintoma_id
LEFT JOIN 
    apresenta a2 ON s.id = a2.sintoma_id AND a2.frequencia = 'muito comum'
LEFT JOIN 
    apresenta a3 ON s.id = a3.sintoma_id AND a3.frequencia = 'comum'
LEFT JOIN 
    apresenta a4 ON s.id = a4.sintoma_id AND a4.frequencia = 'pouco comum'
LEFT JOIN 
    apresenta a5 ON s.id = a5.sintoma_id AND a5.frequencia = 'raro'
LEFT JOIN 
    apresenta a6 ON s.id = a6.sintoma_id AND a6.frequencia = 'muito raro'
GROUP BY 
    s.nome
ORDER BY 
    total DESC,
    muito_comum DESC,
    comum DESC,
    pouco_comum DESC,
    raro DESC,
    muito_raro DESC,
    s.nome ASC;
    
/* g) Consulta para listar todas as doenças que possuem um determinado conjunto de sintomas. Devem ser 
apresentados o id da doença e o seu nome (mantendo as colunas nesta ordem e as linhas organizadas em 
ordem alfabética em relação ao nome da doença). Para essa questão, considere o seguinte conjunto de 
sintomas “Febre” e “Diarreia”. */

SELECT d.id, d.nome_tecnico AS Doença
FROM doença AS d 
JOIN apresenta AS a ON d.id = a.doença_id
JOIN sintomas AS s ON s.id = a.sintoma_id
WHERE s.nome IN ('Febre', 'Diarreia')
GROUP BY d.id, d.nome_tecnico
HAVING COUNT(DISTINCT s.nome) = 2
ORDER BY d.nome_tecnico ASC;

/* h) Consulta para listar as doenças mais prováveis para uma lista de sintomas analisada. A consulta deve 
retornar o id da doença e o seu nome. Para essa consulta, deve-se considerar um esquema de pontuações 
baseados nos sintomas, calculado da seguinte forma: 
1. Cada sintoma é atribuído a uma taxa de ocorrência. Essas taxas de ocorrência são convertidas em 
pesos numéricos: muito comum = 5; comum = 4; pouco comum = 3; raro = 2; muito raro = 1. 
2. Cada doença inicia com uma pontuação igual a 0 (zero). Para cada sintoma que uma doença tem 
em comum em relação à lista de sintomas avaliada, a pontuação da doença é incrementada pelo 
peso correspondente à taxa de ocorrência do sintoma. 
3. Para cada sintoma presente na lista e que uma doença não tenha em sua relação de sintomas, a 
pontuação da doença é decrementada em 1 ponto.  
4. As doenças são ordenadas em ordem decrescente em relação ao total de pontos obtidos.*/

SELECT d.id, d.nome_tecnico AS Doença,
    SUM(
        CASE 
            WHEN s.nome IN ('Fadiga', 'Tosse', 'Febre', 'Diarreia') THEN
                CASE a.frequencia 
                    WHEN 'muito comum' THEN 5
                    WHEN 'comum' THEN 4
                    WHEN 'pouco comum' THEN 3
                    WHEN 'raro' THEN 2
                    WHEN 'muito raro' THEN 1
                    ELSE -1
                END
            ELSE -1
        END
    )-1 AS Peso_Total  #< 3 você soma, > 3 você subtrai#
FROM doença AS d
LEFT JOIN apresenta AS a ON d.id = a.doença_id
LEFT JOIN sintomas AS s ON s.id = a.sintoma_id
GROUP BY d.id, d.nome_tecnico
ORDER BY Peso_Total DESC;